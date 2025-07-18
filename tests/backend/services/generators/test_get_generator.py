from backend.services.generators.get_generator import get_generator
from backend.core.types import Generator
from backend.services.generators.hf_generator import HuggingFaceGenerator
from backend.services.generators.or_generator import OpenRouterGenerator
from backend.services.generators.base_generator import BaseGenerator


async def test_get_generator():
    try:
        get_generator("HF")
    except Exception:
        ValueError

    generator = get_generator()
    assert isinstance(generator, BaseGenerator)

    generator = get_generator(Generator.HF)
    assert isinstance(generator, HuggingFaceGenerator)

    generator = get_generator(Generator.OR)
    assert isinstance(generator, OpenRouterGenerator)

    generator = get_generator(Generator.NONE)
    assert generator is None
