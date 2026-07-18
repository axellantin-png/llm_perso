from abc import ABC, abstractmethod

class Chunker(ABC):

    @abstractmethod
    def split(
        self,
        document: Document
    ) -> list[Chunk]:
        pass