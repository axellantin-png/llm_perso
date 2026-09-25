from app.rag.retrievers.vector_retriever import VectorRetriever
from app.rag.models.search_results import SearchResult
from app.rag.models.chunk import Chunk

class FakeEmbedding:


    def embed(self, text):

        return [0.1, 0.2, 0.3]



class FakeVectorStore:


    def search(
        self,
        embedding,
        k=5
    ):

        chunk = Chunk(
            content="contenu test",
            embedding=[0.1,0.2,0.3]
        )


        return [
            SearchResult(
                chunk=chunk,
                score=0.95
            )
        ]

def test_vector_retriever_returns_results():

    embedding_model = FakeEmbedding()

    vector_store = FakeVectorStore()


    retriever = VectorRetriever(
        embedding_model,
        vector_store
    )


    results = retriever.retrieve(
        "question test"
    )


    assert len(results) == 1

    assert results[0].chunk.content == "contenu test"


class FakeVectorStore2:

    def __init__(self):

        self.last_k = None


    def search(
        self,
        embedding,
        k=5
    ):

        self.last_k = k

        return []


def test_vector_retriever_passes_limit():

    store = FakeVectorStore2()

    retriever = VectorRetriever(
        FakeEmbedding(),
        store
    )


    retriever.retrieve(
        "question",
        k=3
    )


    assert store.last_k == 3