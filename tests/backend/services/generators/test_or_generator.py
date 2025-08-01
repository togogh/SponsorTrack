from backend.services.generators.or_generator import OpenRouterGenerator
from backend.core.settings import generator_settings
from backend.core.types import Generator
from openai import OpenAI, BadRequestError
import pytest


async def test_or_generator():
    if generator_settings.GENERATOR != Generator.OR:
        pytest.skip("OR Generator not selected, skipping...")

    generator = OpenRouterGenerator("test")
    assert isinstance(generator.client, OpenAI)

    await generator.queue_message("user", "random")
    assert len(generator.messages) == 1

    with pytest.raises(BadRequestError):
        await generator.generate_response()

    generator = OpenRouterGenerator(model="google/gemma-2-9b-it:free")
    assert isinstance(generator.client, OpenAI)

    await generator.queue_message("user", "random")
    await generator.generate_response()
    response = generator.messages[-1]["content"]
    assert len(response) > 0
    assert isinstance(response, str)

    prompt = "Please respond with a list object enclosed in a ```json``` markdown code block."
    response = await generator.extract_sponsor_info(prompt)
    assert isinstance(response, list)
    assert len(response) > 0
