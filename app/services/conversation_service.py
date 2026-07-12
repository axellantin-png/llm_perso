


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

    def save(self, conversation): # pour le moment elle n'est pas nécéssaire 
        self.repository.save(conversation)

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

    def list_conversations(self):

        return self.repository.list()


    def rename(
        self,
        conversation_id,
        title
    ):
        conversation = self.repository.get(
            conversation_id
        )

        conversation.rename(title)

        self.repository.save(
            conversation
        )

    def delete(self, conversation_id):

        self.repository.delete(
            conversation_id
        )