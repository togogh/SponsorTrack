class BaseGenerator:
    def __init__(self):
        self.client = None
        self.messages = []

    def connect_client(self):
        pass

    def queue_message(self):
        pass

    def generate_response(self):
        pass
