


class ConversationService:

    def __init__(self, repository):
        self.repository = repository

    def create(self):
        return self.repository.create()

    def get(self, conversation_id):
        conversation = self.repository.get(
            conversation_id
        )
        return conversation

    def save(self):
        return

    def add_user_message(self, conversation, message):
        conversation.add_message(
            "user",
            message
        )
        self.repository.save(conversation)

    def add_assistant_message(self, conversation, message):
        conversation.add_message(
            "assistant",
            message
        )
        self.repository.save(conversation)