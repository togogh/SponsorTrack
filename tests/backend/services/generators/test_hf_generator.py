from backend.services.generators.hf_generator import HuggingFaceGenerator
from huggingface_hub import InferenceClient
from huggingface_hub.errors import RepositoryNotFoundError
from backend.core.settings import generator_settings
from backend.core.types import Generator
import pytest


async def test_hf_generator():
    if generator_settings.GENERATOR != Generator.HF:
        pytest.skip("HF Generator not selected, skipping...")

    generator = HuggingFaceGenerator("test", "test")
    assert isinstance(generator.client, InferenceClient)

    await generator.queue_message("user", "random")
    assert len(generator.messages) == 1

    with pytest.raises(ValueError):
        await generator.generate_response()

    generator = HuggingFaceGenerator("test")
    assert isinstance(generator.client, InferenceClient)

    await generator.queue_message("user", "random")
    assert len(generator.messages) == 1

    with pytest.raises(RepositoryNotFoundError):
        await generator.generate_response()

    generator = HuggingFaceGenerator(model="HuggingFaceTB/SmolLM3-3B")
    assert isinstance(generator.client, InferenceClient)

    await generator.queue_message("user", "random")
    await generator.generate_response()
    response = generator.messages[-1]["content"]
    assert len(response) > 0
    assert isinstance(response, str)

    prompt = "Please respond with any json enclosed in a ```json ``` markdown code block, where the highest level is a list."
    response = await generator.extract_sponsor_info(prompt)
    assert isinstance(response, list)
    assert len(response) > 0
