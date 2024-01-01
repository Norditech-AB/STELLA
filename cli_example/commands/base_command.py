class BaseCommand:
    def __init__(self, client, args):
        self.client = client
        self.args = args

    def execute(self):
        raise NotImplementedError("Each command must implement an execute method.")
