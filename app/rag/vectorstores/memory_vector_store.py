from app.rag.vectorstores.vector_store import VectorStore

class MemoryVectorStore(VectorStore):

    def __init__(
        self,
        similarity
    ):
        self.similarity = similarity 
        self.chunks = []


    def add(self, chunks) : 
        self.chunks.extend(chunks)

    def clear(self):
        self.chunks.clear()

    def search (self, embedding, k=5) : 
        scores = []
        for chunk in self.chunks : 
            score = self.similarity.score(embedding, chunk.embedding)
            scores.append((score, chunk))

        scores.sort(reverse = True, key = lambda item: item[0])
        return [chunk for _, chunk in scores[:k]]