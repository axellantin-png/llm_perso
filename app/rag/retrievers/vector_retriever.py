from app.rag.retrievers.retriever import Retriever
from app.rag.vectorstores.vector_store import VectorStore
from app.rag.embeddings.embedding import Embedding
from app.rag.models.search_results import SearchResult

class VectorRetriever(Retriever):
    def __init__(self, vector_store: VectorStore, embedding: Embedding):
        self.vector_store = vector_store
        self.embedding = embedding

    def retrieve(self, query: str, k: int = 5) -> list[SearchResult]:
        # 1. Génération de l'embedding de la requête
        query_embedding = self.embedding.embed(query)

        # 2. Recherche vectorielle (on peut demander un peu plus large si on craint d'éliminer des doublons, ex: k * 2)
        raw_results = self.vector_store.search(query_embedding, k=k * 2)

        # 3. Déduplication intelligente des résultats
        seen_contents = set()
        unique_results = []

        for result in raw_results:
            # On nettoie un peu le contenu pour la comparaison (espaces superflus)
            content_key = result.chunk.content.strip()

            if content_key not in seen_contents:
                seen_contents.add(content_key)
                unique_results.append(result)

            # Si on a atteint le nombre k souhaité d'éléments uniques, on s'arrête
            if len(unique_results) >= k:
                break

        return unique_results

