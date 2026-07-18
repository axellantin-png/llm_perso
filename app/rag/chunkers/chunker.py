from abc import ABC, abstractmethod
from app.rag.models.document import Document
from app.rag.models.chunk import Chunk

class Chunker(ABC):

    @abstractmethod
    def split(
        self,
        document: Document
    ) -> list[Chunk]:
        pass