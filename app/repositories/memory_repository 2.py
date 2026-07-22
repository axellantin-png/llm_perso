from app.models.conversation import Conversation

from app.repositories.conversation_repository import (
    ConversationRepository
)


class MemoryRepository(ConversationRepository):

    def __init__(self):

        self.conversations = {}


    def create(self):

        conversation = Conversation.new()

        self.conversations[
            conversation.id
        ] = conversation

        print("CREATE :", self.conversations)

        return conversation


    def get(self, conversation_id):

        print("GET ID : ", conversation_id)
        print("AVAILABLE : ", self.conversations)

        conversation = self.conversations.get(
            conversation_id
        )

        if conversation is None:
            raise ValueError(
                f"Conversation {conversation_id} not found"
            )

        return conversation


    def delete(self, conversation_id):

        if conversation_id in self.conversations:

            del self.conversations[
                conversation_id
            ]

    def save(self, conversation) : 
        print(conversation)


    def list(self):
        pass


    def rename(self, conversation_id, title):
        pass