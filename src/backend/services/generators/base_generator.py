class BaseGenerator:
    def __init__(self, provider, model):
        self.client = None
        self.messages = []
        self.provider = provider
        self.model = model

    async def connect_client(self):
        pass

    async def queue_message(self):
        pass

    async def generate_response(self):
        pass

    async def extract_sponsor_info(self, prompt):
        pass
