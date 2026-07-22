from app.models.conversation import Conversation


class ConversationManager:

    def __init__(self):
        self.conversations = {}

    def create(self):
        conversation = Conversation()

        self.conversations[conversation.id] = conversation

        return conversation


    def get(self, conversation_id):

        return self.conversations.get(
            conversation_id
        )


    def delete(self, conversation_id):

        if conversation_id in self.conversations:
            del self.conversations[conversation_id]