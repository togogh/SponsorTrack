from backend.core.settings import generator_settings
from backend.core.types import Generator
from .hf_generator import HuggingFaceGenerator


def get_generator(generator: Generator = None):
    if generator is None:
        generator = generator_settings.GENERATOR
    match generator:
        case Generator.HF:
            return HuggingFaceGenerator(
                provider=generator_settings.PROVIDER, model=generator_settings.MODEL
            )
        case None:
            return None
