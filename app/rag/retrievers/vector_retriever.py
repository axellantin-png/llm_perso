from app.rag.retrievers.retriever import Retriever


class VectorRetriever(Retriever):

    def __init__(
        self,
        embedding,
        vector_store
    ):

        self.embedding = embedding
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        k: int = 5
    ):

        query_embedding = self.embedding.embed(
            query
        )

        return self.vector_store.search(
            query_embedding,
            k
        )