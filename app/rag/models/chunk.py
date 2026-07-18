from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Chunk:

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    document_id: str = ""

    owner_id: str = ""

    index: int = 0

    content: str = ""

    embedding: list[float] | None = None