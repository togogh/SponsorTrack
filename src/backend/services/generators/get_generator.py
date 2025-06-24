from backend.core.settings import generator_settings
from .hf_generator import HuggingFaceGenerator


def get_generator():
    match generator_settings.GENERATOR:
        case "HF":
            return HuggingFaceGenerator(generator_settings.PROVIDER, generator_settings.MODEL)
        case None:
            return None
