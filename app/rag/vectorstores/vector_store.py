from abc import ABC, abstractmethod
from app.rag.models.chunk import Chunk

class VectorStore(ABC):

    @abstractmethod
    def add(
        self,
        chunks: list[Chunk]
    ):
        pass

    @abstractmethod
    def search(
        self,
        embedding: list[float],
        k: int
    ) -> list[Chunk]:
        pass

    @abstractmethod
    def clear(self):
        pass