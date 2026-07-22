from app.rag.vectorstores.vector_store import VectorStore

class MemoryVectorStore(VectorStore):

    def __init__(self):

        self.chunks = []


    def add(self, chunks) : 
        self.chunks.extend(chunks)

    def search () : 
        