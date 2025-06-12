from sponsortrack.old_backend.generators.base_generator import BaseGenerator
from huggingface_hub import InferenceClient
import os


class HuggingFaceGenerator(BaseGenerator):
    def connect_client(self, provider="novita"):
        client = InferenceClient(
            provider=provider,
            api_key=os.getenv("HF_TOKEN"),
        )
        self.client = client

    def queue_message(self, role, message):
        self.messages.append(
            {
                "role": role,
                "content": message,
            }
        )

    def generate_response(self, model="deepseek-ai/DeepSeek-V3-0324"):
        completion = self.client.chat.completions.create(
            model=model,
            messages=self.messages,
        )
        response = completion.choices[0].message
        role = response.role
        content = response.content
        self.queue_message(role, content)
