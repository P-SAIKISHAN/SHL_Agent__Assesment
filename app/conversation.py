class ConversationState:
    def __init__(self, messages):
        self.messages = messages

    def latest_user_message(self):
        for msg in reversed(self.messages):
            if msg.role == "user":
                return msg.content
        return ""