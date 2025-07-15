class BaseGenerator:
    def __init__(self, model: str, provider: str = "auto"):
        self.messages: list[str] = []
        self.provider: str = provider
        self.model: str = model

    @property
    def client(self):
        pass

    async def queue_message(self):
        pass

    async def generate_response(self):
        pass

    async def extract_sponsor_info(self, prompt):
        pass
