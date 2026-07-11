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