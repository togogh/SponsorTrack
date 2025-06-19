class BaseGenerator:
    def __init__(self, provider, model):
        self.client = None
        self.messages = []
        self.provider = provider
        self.model = model

    def connect_client(self):
        pass

    def queue_message(self):
        pass

    def generate_response(self):
        pass
