from dataclasses import dataclass, field
from uuid import uuid4

from app.models.message import Message


@dataclass
class Conversation:

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    messages: list[Message] = field(
        default_factory=list
    )

    title: str = "Nouvelle conversation"


    @classmethod
    def from_id(cls, conversation_id: str, title: str = "Conversation existante"):
        """
        Crée une instance de Conversation avec un ID spécifique 
        et une liste de messages vide.
        """
        return cls(
            id=conversation_id,
            title=title
        )


    def add_message(
        self,
        role,
        content
    ):

        self.messages.append(
            Message(
                role,
                content
            )
        )