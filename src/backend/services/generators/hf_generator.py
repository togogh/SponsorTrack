from .base_generator import BaseGenerator
from huggingface_hub import InferenceClient
from backend.core.settings import generator_settings
import re
import json


class HuggingFaceGenerator(BaseGenerator):
    async def connect_client(self):
        client = InferenceClient(
            provider=self.provider,
            api_key=generator_settings.HF_TOKEN,
        )
        self.client = client

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
        await self.connect_client()
        await self.queue_message("user", prompt)
        await self.generate_response()
        response = self.messages[-1]["content"]
        match = re.search(r"json\s*(\{.*?\})\s*", response, re.DOTALL)
        if match:
            json_str = match.group(1)
            data = json.loads(json_str)
            return data
        else:
            raise ValueError("No JSON found.")
