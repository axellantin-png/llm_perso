import pytest
from app.rag.models.document import Document
from app.rag.chunkers.fixed_chunker import FixedChunker
from app.rag.embeddings.ollama_embeddings import OllamaEmbedding
from app.rag.vectorstores.memory_vector_store import MemoryVectorStore
from app.rag.similarity.cosine_similarity import CosineSimilarity
from app.rag.similarity.dot_product_similarity import DotProductSimilarity
from app.rag.similarity.hybride_similarity import HybridSimilarity
from app.rag.retrievers.vector_retriever import VectorRetriever
from app.rag.services.document_indexer import DocumentIndexer

def test_compare_all_similarities_on_large_document():
    """
    Test comparatif approfondi entre Cosinus, Produit Scalaire et Hybride.
    """
    try:
        embedding = OllamaEmbedding()
    except Exception as e:
        pytest.skip(f"Ollama n'est pas disponible : {e}")

    large_content = (
        "Chapitre 1 : Introduction à l'architecture. "
        "Le projet llm_local repose sur une architecture modulaire en Python. "
        "Les services communiquent entre eux via des interfaces clairement définies pour garantir la maintenabilité. "
        "Chapitre 2 : Persistance et Base de données. "
        "SQLite est utilisé pour stocker l'historique des conversations ainsi que les métadonnées des messages échangés avec les utilisateurs. "
        "Chapitre 3 : Moteur d'Inférence. "
        "L'inférence des modèles de langage locaux est déléguée à Ollama, qui tourne en arrière-plan sur la machine de développement, "
        "en exploitant pleinement l'accélération matérielle disponible (GPU Metal sur Apple Silicon). "
        "Chapitre 4 : Moteur RAG et Recherche. "
        "Le système RAG implémenté from scratch permet de segmenter les documents en chunks, de générer des embeddings vectoriels "
        "via nomic-embed-text, et d'effectuer une recherche par similarité cosinus pour retrouver le contexte pertinent."
    )

    doc = Document(id="doc-architecture-complete", content=large_content)
    query = "Quel composant gère l'inférence des modèles de langage locaux ?"

    # On met une taille de chunk plus grande (350) pour contenir l'information complète
    chunker = FixedChunker(chunk_size=350, embedding=embedding)

    # --- 1. Cosinus ---
    vs_cosine = MemoryVectorStore(similarity=CosineSimilarity())
    indexer_cosine = DocumentIndexer(chunker=chunker, embedding=embedding, vector_store=vs_cosine)
    indexer_cosine.index(doc)
    retriever_cosine = VectorRetriever(vector_store=vs_cosine, embedding=embedding)
    results_cosine = retriever_cosine.retrieve(query, k=1)

    # --- 2. Produit Scalaire ---
    vs_dot = MemoryVectorStore(similarity=DotProductSimilarity())
    indexer_dot = DocumentIndexer(chunker=chunker, embedding=embedding, vector_store=vs_dot)
    indexer_dot.index(doc)
    retriever_dot = VectorRetriever(vector_store=vs_dot, embedding=embedding)
    results_dot = retriever_dot.retrieve(query, k=1)

    # --- 3. Hybride ---
    hybrid_sim = HybridSimilarity(semantic_weight=0.7, lexical_weight=0.3)
    all_chunks = vs_cosine.chunks
    query_embedding = embedding.embed(query)
    
    best_hybrid_result = None
    best_hybrid_score = -1.0
    
    for chunk in all_chunks:
        score = hybrid_sim.score(
            query_embedding, 
            chunk.embedding, 
            text_a=query, 
            text_b=chunk.content
        )
        if score > best_hybrid_score:
            best_hybrid_score = score
            best_hybrid_result = chunk

    # Affichage du comparatif détaillé
    print("\n" + "="*60)
    print(f" QUESTION : {query}")
    print("="*60)
    print(f"[Cosinus]       Score: {results_cosine[0].score:.4f}")
    print(f"                Extrait: {results_cosine[0].chunk.content}")
    print("-" * 60)
    print(f"[Produit Scal.] Score: {results_dot[0].score:.4f}")
    print(f"                Extrait: {results_dot[0].chunk.content}")
    print("-" * 60)
    print(f"[Hybride]       Score: {best_hybrid_score:.4f}")
    print(f"                Extrait: {best_hybrid_result.content if best_hybrid_result else 'N/A'}")
    print("="*60)

    # VÉRITABLES ASSERTIONS COMPARATIVES ET DE PERTINENCE
    
    # 1. Le cosinus et le produit scalaire doivent tous les deux remonter le chunk contenant "Ollama"
    assert "Ollama" in results_cosine[0].chunk.content, "Le cosinus doit trouver le bon chunk"
    assert "Ollama" in results_dot[0].chunk.content, "Le produit scalaire doit trouver le bon chunk"
    assert best_hybrid_result is not None and "Ollama" in best_hybrid_result.content, "L'hybride doit trouver le bon chunk"

    # 2. Comparaison structurelle des métriques : 
    # Sur des vecteurs normalisés (comme nomic-embed-text), le score Cosinus et le Produit Scalaire doivent être extrêmement proches
    assert abs(results_cosine[0].score - results_dot[0].score) < 0.01, (
        "Le cosinus et le produit scalaire devraient donner des scores quasi identiques avec des embeddings normalisés."
    )

    # 3. L'hybride combine sémantique et mots, son score pondéré intègre la dimension lexicale
    assert best_hybrid_score > 0.3, "Le score hybride doit refléter une pertinence globale significative."