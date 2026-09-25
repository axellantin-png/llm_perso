from abc import ABC, abstractmethod
from app.rag.models.chunk import Chunk

class Retriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        query: str,
        limit: int = 5
    ) -> list[Chunk]:
        pass