from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Document:

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    owner_id: str = ""

    title: str = ""

    content: str = ""

    source: str = ""