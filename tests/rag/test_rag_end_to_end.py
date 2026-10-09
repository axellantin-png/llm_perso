import pytest
from app.rag.models.document import Document
from app.rag.services.document_indexer import DocumentIndexer
from app.rag.vectorstores.memory_vector_store import MemoryVectorStore
from app.rag.similarity.cosine_similarity import CosineSimilarity
from app.rag.retrievers.vector_retriever import VectorRetriever
from tests.fake_class.fake_embedding import FakeEmbedding
from tests.fake_class.fake_vectore_store import FakeVectorStore # ou utiliser le memory store avec fake embedding

def test_rag_pipeline_end_to_end():
    # 1. Préparation des composants de test (on peut utiliser FakeEmbedding pour s'affranchir d'Ollama pendant les tests unitaires purs)
    embedding = FakeEmbedding()
    vector_store = MemoryVectorStore(similarity=CosineSimilarity())
    
    # 2. Indexation d'un document fictif
    doc = Document(id="doc-1", content="Le projet llm_local est un assistant personnel local. Il utilise Ollama pour exécuter un modèle de langage.")
    
    # Simulation du chunking et indexation manuelle ou via DocumentIndexer
    # (Supposons que vous indexez le document)
    from app.rag.chunkers.fixed_chunker import FixedChunker
    chunker = FixedChunker(chunk_size=10, embedding=embedding)
    chunks = chunker.chunk(doc)
    
    for chunk in chunks:
        vector_store.add(chunk)
        
    # 3. Création du retriever
    retriever = VectorRetriever(vector_store=vector_store, embedding=embedding)
    
    # 4. Test de récupération
    results = retriever.retrieve("Quel système est utilisé pour le projet ?")
    
    assert len(results) > 0
    # Vérification que le contenu récupéré est pertinent
    found_content = " ".join([r.chunk.content for r in results])
    assert "llm_local" in found_content or "Ollama" in found_content