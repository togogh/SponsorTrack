from .base_generator import BaseGenerator
from huggingface_hub import InferenceClient
from backend.core.settings import generator_settings
import re
import json
from backend.logs.config import get_logger

logger = get_logger(__name__)


class HuggingFaceGenerator(BaseGenerator):
    def __init__(self, model, provider: str = "auto"):
        super().__init__(model)
        self.provider: str = provider

    @property
    def client(self) -> InferenceClient:
        client = InferenceClient(
            provider=self.provider,
            api_key=generator_settings.HF_TOKEN,
        )
        return client

    async def queue_message(self, role, message):
        self.messages.append(
            {
                "role": role,
                "content": message,
            }
        )

    async def generate_response(self):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )
        response = completion.choices[0].message
        role = response.role
        content = response.content
        await self.queue_message(role, content)

    async def extract_sponsor_info(self, prompt):
        await self.queue_message("user", prompt)
        await self.generate_response()
        response = self.messages[-1]["content"]
        logger.info(f"Generator response: {response}")
        pattern = r"```json\s*\n(\[.*?\])\s*```"
        match = re.search(pattern, response, re.DOTALL)
        if match:
            json_str = match.group(1)
            data = json.loads(json_str)
            return data
        else:
            raise ValueError("No JSON found.")
