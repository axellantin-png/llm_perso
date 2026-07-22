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
    def new(cls):
        return cls()


    @classmethod
    def from_database(cls, id: str, title: str = "Conversation existante"):
        """
        Crée une instance de Conversation avec un ID spécifique 
        et une liste de messages vide.
        """
        return cls(
            id=id,
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

    def rename(self, title) : 
        self.title = title
