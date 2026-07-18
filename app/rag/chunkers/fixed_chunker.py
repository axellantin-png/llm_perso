from app.rag.chunkers.chunker import Chunker
from app.rag.models.chunk import Chunk


class FixedChunker(Chunker):

    def __init__(
        self,
        chunk_size=500
    ):
        self.chunk_size = chunk_size

    def split (self, document):
        for i in range(0, len(document.content), self.chunk_size):
            content = document.content[i:i+ self.chunk_size]
            chunk = Chunk()