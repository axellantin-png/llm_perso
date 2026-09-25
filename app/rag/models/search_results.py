from dataclasses import dataclass
from app.rag.models.chunk import Chunk


@dataclass
class SearchResult:

    chunk: Chunk

    score: float