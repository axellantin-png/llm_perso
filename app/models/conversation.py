from dataclasses import dataclass, field
from uuid import uuid4

from app.models.message import Message


@dataclass
class Conversation:

    id: str = field(default_factory=lambda: str(uuid4()))

    messages: list[Message] = field(default_factory=list)

    title: str = "Nouvelle conversation"