import json
from app.rag.vectorstores.vector_store import VectorStore
from app.rag.models.chunk import Chunk
from app.rag.models.search_results import SearchResult
from app.rag.similarity.similarity import Similarity
from app.database.database import Database

class SQLiteVectorStore(VectorStore):
    """
    Implémentation persistante du VectorStore stockant les chunks et embeddings dans SQLite.
    """
    def __init__(self, database: Database, similarity: Similarity):
        self.database = database
        self.similarity = similarity
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        """Crée la table des chunks si elle n'existe pas encore."""
        with self.database.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS document_chunks (
                    id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    document_title TEXT,
                    content TEXT NOT NULL,
                    embedding TEXT NOT NULL,
                    parent_content TEXT
                )
            """)
            conn.commit()

    def add(self, chunk: Chunk) -> None:
        """Ajoute un chunk et son embedding sérialisé en JSON dans SQLite."""
        if chunk.embedding is None:
            raise ValueError("Impossible d'ajouter un chunk sans embedding.")

        embedding_json = json.dumps(chunk.embedding)

        with self.database.get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO document_chunks 
                (id, document_id, document_title, content, embedding, parent_content)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                chunk.id,
                chunk.document_id,
                chunk.document_title,
                chunk.content,
                embedding_json,
                chunk.parent_content
            ))
            conn.commit()

    def search(self, embedding: list[float], k: int = 5) -> list[SearchResult]:
        """Récupère tous les chunks de SQLite, calcule la similarité et retourne le top K."""
        with self.database.get_connection() as conn:
            cursor = conn.execute("SELECT id, document_id, document_title, content, embedding, parent_content FROM document_chunks")
            rows = cursor.fetchall()

        results = []
        for row in rows:
            chunk_id, doc_id, doc_title, content, embedding_json, parent_content = row
            chunk_embedding = json.loads(embedding_json)

            score = self.similarity.score(embedding, chunk_embedding)

            chunk = Chunk(
                id=chunk_id,
                content=content,
                embedding=chunk_embedding,
                document_id=doc_id,
                document_title=doc_title,
                parent_content=parent_content
            )

            results.append(SearchResult(chunk=chunk, score=score))

        results.sort(key=lambda x: x.score, reverse=True)

        return results[:k]

    def clear(self) -> None:
        """Vide la table des chunks (requis par l'interface VectorStore)."""
        with self.database.get_connection() as conn:
            conn.execute("DELETE FROM document_chunks")
            conn.commit()