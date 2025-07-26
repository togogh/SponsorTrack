from backend.core.settings import generator_settings
from backend.core.types import Generator
from .base_generator import BaseGenerator
from .hf_generator import HuggingFaceGenerator
from .or_generator import OpenRouterGenerator


def get_generator(generator: Generator = None) -> BaseGenerator | None:
    if generator is None:
        generator = generator_settings.GENERATOR
    match generator:
        case Generator.HF:
            return HuggingFaceGenerator(
                provider=generator_settings.PROVIDER, model=generator_settings.MODEL
            )
        case Generator.OR:
            return OpenRouterGenerator(model=generator_settings.MODEL)
        case None:
            return None
