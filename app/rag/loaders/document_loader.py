from abc import ABC, abstractmethod
from app.rag.models.document import Document 

class DocumentLoader(ABC):

    @abstractmethod
    def load(
        self,
        path: str
    ) -> Document:
        pass