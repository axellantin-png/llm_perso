from abc import ABC, abstractmethod

from app.models.conversation import Conversation


class ConversationRepository(ABC):

    @abstractmethod
    def create(self) -> Conversation:
        pass


    @abstractmethod
    def get(
        self,
        conversation_id: str
    ) -> Conversation:
        pass


    @abstractmethod
    def delete(
        self,
        conversation_id: str
    ):
        pass

    @abstractmethod
    def save(self, conversation):
        pass

    @abstractmethod
    def list(self):
        pass


    @abstractmethod
    def rename(self, conversation_id, title):
        pass