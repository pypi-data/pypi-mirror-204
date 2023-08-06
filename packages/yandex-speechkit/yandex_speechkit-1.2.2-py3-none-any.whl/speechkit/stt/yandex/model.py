import grpc
import uuid
from typing import List, Tuple
from pydub import AudioSegment

from yandex.cloud.ai.stt.v3 import stt_pb2, stt_service_pb2_grpc

from ...common.apis import YandexModel
from ...common.utils import get_yandex_credentials

from ..recognizer import RecognitionConfig, RecognitionModel
from ..transcription import Transcription, Word
from .config import YandexRecognitionConfig, AudioProcessingType


class YandexRecognizer(RecognitionModel, YandexModel):
    def __init__(
        self,
        endpoint: str = 'stt.api.cloud.yandex.net:443',
        use_ssl: bool = True,
        custom_headers: List[Tuple[str, str]] = None,
        **kwargs,
    ):
        RecognitionModel.__init__(self, YandexRecognitionConfig())
        YandexModel.__init__(self, endpoint, use_ssl, custom_headers)

        while True:
            try:
                grpc.channel_ready_future(self._channel).result(timeout=10)
                break
            except grpc.FutureTimeoutError:
                print('Recognition service is temporarily unavailable')

    @staticmethod
    def __gen_requests(
        pcm: bytes,
        sample_rate: int,
        sample_width: int,
        recognition_config: YandexRecognitionConfig
    ):
        if recognition_config.language is not None:
            language_restriction = stt_pb2.LanguageRestrictionOptions(
                restriction_type=stt_pb2.LanguageRestrictionOptions.WHITELIST,
                language_code=[recognition_config.language],
            )
        else:
            language_restriction = stt_pb2.LanguageRestrictionOptions(
                restriction_type=stt_pb2.LanguageRestrictionOptions.LANGUAGE_RESTRICTION_TYPE_UNSPECIFIED
            )

        if recognition_config.audio_processing_type == AudioProcessingType.Stream:
            audio_processing_type = stt_pb2.RecognitionModelOptions.REAL_TIME
        else:
            audio_processing_type = stt_pb2.RecognitionModelOptions.FULL_DATA

        recognize_options = stt_pb2.StreamingOptions(
            recognition_model=stt_pb2.RecognitionModelOptions(
                model=recognition_config.model,
                audio_format=stt_pb2.AudioFormatOptions(
                    raw_audio=stt_pb2.RawAudio(
                        audio_encoding=stt_pb2.RawAudio.LINEAR16_PCM,
                        sample_rate_hertz=sample_rate,
                        audio_channel_count=1,
                    )
                ),
                text_normalization=stt_pb2.TextNormalizationOptions(
                    text_normalization=stt_pb2.TextNormalizationOptions.TEXT_NORMALIZATION_ENABLED,
                    profanity_filter=False,
                    literature_text=True,
                ),
                language_restriction=language_restriction,
                audio_processing_type=audio_processing_type,
            )
        )

        yield stt_pb2.StreamingRequest(session_options=recognize_options)

        chunk_duration = 0.2
        chunk_size = int(sample_rate * sample_width * chunk_duration)

        for i in range(0, len(pcm), chunk_size):
            yield stt_pb2.StreamingRequest(chunk=stt_pb2.AudioChunk(data=pcm[i : i + chunk_size]))

    def _transcribe_single_channel(
        self,
        channel: int,
        pcm: bytes,
        sample_rate: int,
        sample_width: int,
        recognition_config: YandexRecognitionConfig
    ) -> Transcription:
        assert sample_width == 2

        req_id = str(uuid.uuid4())
        stub = stt_service_pb2_grpc.RecognizerStub(self._channel)

        try:
            yandex_creds = get_yandex_credentials()
            if yandex_creds.api_key is not None:
                authorization_header = f'Api-Key {yandex_creds.api_key}'
            else:
                authorization_header = f'Bearer {yandex_creds.iam_token}'

            metadata = [
                ('authorization', authorization_header),
                ('x-client-request-id', req_id),
                *self._custom_headers
            ]

            if recognition_config.data_logging:
                metadata.append(('x-data-logging-enabled', 'true'))

            it = stub.RecognizeStreaming(
                self.__gen_requests(pcm, sample_rate, sample_width, recognition_config),
                metadata=metadata
            )

            raw_recognitions, normalized_recognitions, words = [], [], []
            for r in it:
                if r.HasField('final'):
                    if len(r.final.alternatives) != 0:
                        raw_recognitions.append(r.final.alternatives[0].text)
                        for word in r.final.alternatives[0].words:
                            words.append(Word(word.text, word.start_time_ms, word.end_time_ms))
                if r.HasField('final_refinement'):
                    alternatives = r.final_refinement.normalized_text.alternatives
                    if len(alternatives) != 0:
                        normalized_recognitions.append(alternatives[0].text)
            return Transcription(
                raw_text=' '.join(raw_recognitions),
                normalized_text=' '.join(normalized_recognitions),
                words=words,
                channel=str(channel),
            )
        except grpc._channel._Rendezvous as err:
            print(f'Failed to recognize audio, request_id={req_id}. Error code {err._state.code}, message: {err._state.details}')
            raise err
        except Exception as err:
            print(f'Failed to recognize audio, request_id={req_id}. Error: {err}')
            raise err

    def _transcribe_impl(
        self,
        audio: AudioSegment,
        recognition_config: RecognitionConfig
    ) -> List[Transcription]:
        if not isinstance(recognition_config, YandexRecognitionConfig):
            recognition_config = YandexRecognitionConfig(**recognition_config.__dict__)

        transcriptions = []
        for channel, content in enumerate(audio.split_to_mono()):
            transcriptions.append(
                self._transcribe_single_channel(
                    channel,
                    content.raw_data,
                    audio.frame_rate,
                    audio.sample_width,
                    recognition_config
                )
            )
        return transcriptions
