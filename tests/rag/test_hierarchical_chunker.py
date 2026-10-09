import pytest
from app.rag.models.document import Document
from app.rag.chunkers.hierarchical_chunker import HierarchicalChunker
from app.rag.vectorstores.memory_vector_store import MemoryVectorStore
from app.rag.similarity.cosine_similarity import CosineSimilarity
from app.rag.retrievers.vector_retriever import VectorRetriever
from app.rag.services.document_indexer import DocumentIndexer
from tests.fake_class.fake_embedding import FakeEmbedding

def test_hierarchical_chunker_and_parent_child_retrieval():
    """
    Test que le HierarchicalChunker crée bien des enfants liés à leurs parents,
    et que le retriever les remonte avec succès.
    """
    # Utilisation d'un FakeEmbedding pour un test rapide et indépendant d'Ollama
    embedding = FakeEmbedding()
    vector_store = MemoryVectorStore(similarity=CosineSimilarity())
    
    # Configuration : parent large (ex: 300 caractères), enfant précis (ex: 100 caractères)
    chunker = HierarchicalChunker(parent_size=300, child_size=100, embedding=embedding)
    indexer = DocumentIndexer(chunker=chunker, embedding=embedding, vector_store=vector_store)
    retriever = VectorRetriever(vector_store=vector_store, embedding=embedding)

    # Document structuré
    doc_content = (
        "Chapitre 1 : Introduction générale. "
        "Le projet llm_local est un assistant personnel intelligent et local. "
        "Il intègre un moteur RAG sophistiqué basé sur des embeddings vectoriels et des architectures de type parent-child. "
        "Chapitre 2 : Détails techniques. "
        "L'utilisation de petits blocs enfants permet une précision accrue lors de la recherche vectorielle."
    )
    doc = Document(id="doc-hierarchical", content=doc_content)

    # Indexation
    indexer.index(doc)

    # Requête de test ciblant un concept présent dans le Chapitre 1 (puisque le FakeEmbedding prend le premier)
    query = "assistant personnel intelligent"
    results = retriever.retrieve(query, k=1)

    assert len(results) > 0, "Le retriever doit retourner un résultat"
    
    chunk = results[0].chunk
    
    print(f"\n[Parent-Child Test] Enfant trouvé (recherche) : {chunk.content}")
    print(f"[Parent-Child Test] Parent associé (contexte LLM) : {chunk.parent_content}")

    # Vérifications structurelles
    assert chunk.content is not None, "L'enfant doit avoir un contenu"
    assert chunk.parent_content is not None, "Le parent doit être attaché au chunk"
    assert chunk.content in chunk.parent_content, "Le contenu de l'enfant doit faire partie du parent"
    assert "assistant" in chunk.content.lower() or "llm_local" in chunk.content.lower()