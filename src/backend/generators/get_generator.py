from backend.core.settings import generator_settings
from backend.generators.hf_generator import HuggingFaceGenerator


def get_generator():
    match generator_settings.GENERATOR:
        case "hf":
            return HuggingFaceGenerator()
        case None:
            return None
