import pytest
from app.rag.models.document import Document
from app.rag.chunkers.fixed_chunker import FixedChunker
from app.rag.embeddings.ollama_embeddings import OllamaEmbedding
from app.rag.vectorstores.memory_vector_store import MemoryVectorStore
from app.rag.similarity.cosine_similarity import CosineSimilarity
from app.rag.retrievers.vector_retriever import VectorRetriever
from app.rag.services.document_indexer import DocumentIndexer

def test_rag_end_to_end_with_ollama():
    """
    Test d'intégration end-to-end avec un document plus grand pour valider le RAG.
    """
    try:
        embedding = OllamaEmbedding()
    except Exception as e:
        pytest.skip(f"Ollama n'est pas disponible ou le modèle d'embedding n'est pas chargé : {e}")

    # 1. Initialisation des composants du RAG
    vector_store = MemoryVectorStore(similarity=CosineSimilarity())
    # On choisit une taille de chunk adaptée (ex: 200 caractères)
    chunker = FixedChunker(chunk_size=100, embedding=embedding)
    indexer = DocumentIndexer(chunker=chunker, embedding=embedding, vector_store=vector_store)
    retriever = VectorRetriever(vector_store=vector_store, embedding=embedding)

    # 2. Création d'un document plus long et varié
    doc = Document(
        id="doc-test-riche",
        content=(
            "Introduction au projet : Le projet llm_local est un assistant personnel local développé en Python. "
            "Architecture technique : Il utilise FastAPI pour l'API et SQLite pour la persistance des conversations. "
            "Inférence et Moteur : Pour exécuter le modèle de langage en local, il utilise Ollama. "
            "De plus, le système possède un moteur RAG développé from scratch pour rechercher dans les documents personnels."
        )
    )

    # 3. Indexation du document
    indexer.index(doc)

    # 4. Requête de test ciblée
    query = "Quel outil ou logiciel est utilisé pour exécuter le modèle de langage ?"
    results = retriever.retrieve(query, k=1)

    # 5. Vérifications
    assert len(results) > 0, "Le retriever doit retourner au moins un résultat"
    
    best_chunk_content = results[0].chunk.content
    print(f"\n[RAG Test] Question : {query}")
    print(f"[RAG Test] Chunk trouvé : {best_chunk_content}")
    print(f"[RAG Test] Score de similarité : {results[0].score}")

    assert "Ollama" in best_chunk_content, "Le chunk récupéré doit contenir l'information sur Ollama"