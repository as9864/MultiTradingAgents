class Message:
    def __init__(self, sender: str, receiver: str, type: str, content: dict):
        self.sender = sender
        self.receiver = receiver
        self.type = type  # e.g. "request", "response", "feedback"
        self.content = content

    def __repr__(self):
        return f"<{self.type.upper()} from {self.sender} to {self.receiver}>"