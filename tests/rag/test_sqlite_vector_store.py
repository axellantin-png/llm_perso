import pytest
from app.database.database import Database
from app.rag.models.chunk import Chunk
from app.rag.vectorstores.sqlite_vector_store import SQLiteVectorStore
from app.rag.similarity.cosine_similarity import CosineSimilarity

def test_sqlite_vector_store_persistence(tmp_path):
    """
    Vérifie que les embeddings persistent en base SQLite même après ré-instanciation du store.
    """
    # Utilisation d'une base de test temporaire sur disque via pytest tmp_path
    db_file = tmp_path / "test_assistant.db"
    db = Database(db_path=str(db_file))
    db.initialize()

    similarity = CosineSimilarity()
    
    # 1. Première instance du store : on ajoute un chunk
    store_1 = SQLiteVectorStore(database=db, similarity=similarity)
    
    test_chunk = Chunk(
        id="chunk-persist-test-123",
        content="Ceci est un test de persistance SQLite pour le RAG.",
        embedding=[0.1] * 128, # Embedding factice de dimension 128
        document_id="doc-test-persist"
    )
    store_1.add(test_chunk)

    # 2. Deuxième instance du store (simule un redémarrage de l'application)
    store_2 = SQLiteVectorStore(database=db, similarity=similarity)

    # 3. Recherche : on interroge le nouveau store avec le même embedding
    results = store_2.search(embedding=[0.1] * 128, k=1)

    assert len(results) > 0, "Le store persisté doit retrouver le chunk après redémarrage"
    found = any(r.chunk.id == "chunk-persist-test-123" for r in results)
    assert found, "Le chunk de test persistant doit être retrouvé par le store"
    
    print(f"\n[SQLite VectorStore] Persistance validée avec succès ! Chunk retrouvé : {results[0].chunk.content}")