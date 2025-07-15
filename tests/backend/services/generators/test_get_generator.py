from backend.services.generators.get_generator import get_generator
from backend.core.types import Generator
from backend.services.generators.hf_generator import HuggingFaceGenerator


async def test_get_generator():
    try:
        get_generator("HF")
    except Exception:
        ValueError

    generator = get_generator()
    assert isinstance(generator, HuggingFaceGenerator)

    generator = get_generator(Generator.HF)
    assert isinstance(generator, HuggingFaceGenerator)

    generator = get_generator(Generator.NONE)
    assert generator is None
