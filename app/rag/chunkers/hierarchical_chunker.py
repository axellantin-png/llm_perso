from app.rag.chunkers.chunker import Chunker
from app.rag.models.document import Document
from app.rag.models.chunk import Chunk
from app.rag.embeddings.embedding import Embedding
import uuid

class HierarchicalChunker(Chunker):
    def __init__(self, parent_size: int = 1000, child_size: int = 200, embedding: Embedding = None):
        self.parent_size = parent_size
        self.child_size = child_size
        self.embedding = embedding

    def split(self, document: Document) -> list[Chunk]:
        """
        Implémentation de la méthode abstraite 'split' exigée par le contrat Chunker.
        """
        return self.chunk(document)

    def chunk(self, document: Document) -> list[Chunk]:
        content = document.content
        chunks = []

        # 1. Découpage grossier en "Parents"
        parent_texts = [content[i:i + self.parent_size] for i in range(0, len(content), self.parent_size)]

        for parent_text in parent_texts:
            # 2. Découpage fin en "Children" à l'intérieur du parent
            child_texts = [parent_text[j:j + self.child_size] for j in range(0, len(parent_text), self.child_size)]

            for child_text in child_texts:
                if not child_text.strip():
                    continue
                
                # Création de l'embedding pour l'enfant
                child_embedding = self.embedding.embed(child_text) if self.embedding else None

                chunk = Chunk(
                    id=str(uuid.uuid4()),
                    content=child_text,
                    embedding=child_embedding,
                    document_id=document.id,
                    parent_content=parent_text  # On garde le parent attaché
                )
                chunks.append(chunk)

        return chunks