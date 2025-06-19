from backend.generators.base_generator import BaseGenerator
from huggingface_hub import InferenceClient
from backend.core.settings import generator_settings


class HuggingFaceGenerator(BaseGenerator):
    def connect_client(self):
        client = InferenceClient(
            provider=self.provider,
            api_key=generator_settings.HF_TOKEN,
        )
        self.client = client

    def queue_message(self, role, message):
        self.messages.append(
            {
                "role": role,
                "content": message,
            }
        )

    def generate_response(self):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )
        response = completion.choices[0].message
        role = response.role
        content = response.content
        self.queue_message(role, content)
