class BaseGenerator:
    def __init__(self, model: str):
        self.messages: list[str] = []
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
