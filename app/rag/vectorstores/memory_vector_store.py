from app.rag.vectorstores.vector_store import VectorStore
from app.rag.models.search_results import SearchResult 
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

    def search(self, embedding, k=5):

        results = []

        for chunk in self.chunks:

            score = self.similarity.score(
                embedding,
                chunk.embedding
            )

            results.append(
                SearchResult(
                    chunk=chunk,
                    score=score
                )
            )

        results.sort(
            key=lambda result: result.score,
            reverse=True
        )

        return results[:k]