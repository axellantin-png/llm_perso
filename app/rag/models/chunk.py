from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Chunk:

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    content: str = ""

    embedding: list[float] | None = None

    document_id: str | None = None

    document_title: str | None = None

    # Nouveaux champs optionnels pour le pattern Parent-Child
    parent_id: str | None = None

    parent_content: str | None = None