from app.rag.chunkers.chunker import Chunker
from app.rag.models.chunk import Chunk



class FixedChunker(Chunker):

    def __init__( self, chunk_size, embedding) :
        self.chunk_size = chunk_size
        self.embedding = embedding

    def split (self, document):
        res = []
        for i in range(0, len(document.content), self.chunk_size):
            content = document.content[i:i+ self.chunk_size]
            chunk = Chunk(
                document_id=document.id,
                content=content, 
                embedding= self.embedding.embed(content)
            )
            res .append(chunk)
        return res 