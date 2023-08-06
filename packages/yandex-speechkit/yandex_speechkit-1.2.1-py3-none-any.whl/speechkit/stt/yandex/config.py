from dataclasses import dataclass
from ..recognizer import RecognitionConfig, AudioProcessingType


@dataclass
class YandexRecognitionConfig(RecognitionConfig):
    model: str = None
    language: str = None
    audio_processing_type: AudioProcessingType = AudioProcessingType.Full
