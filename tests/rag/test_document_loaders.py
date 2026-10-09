import os
import pytest
from app.rag.loaders.markdown_loader import MarkdownLoader
from app.rag.loaders.pdf_loader import PDFLoader
from app.rag.vectorstores.memory_vector_store import MemoryVectorStore
from app.rag.similarity.cosine_similarity import CosineSimilarity
from app.rag.similarity.hybride_similarity import HybridSimilarity
from app.rag.chunkers.fixed_chunker import FixedChunker
from app.rag.embeddings.ollama_embeddings import OllamaEmbedding
from app.rag.retrievers.vector_retriever import VectorRetriever
from app.rag.services.document_indexer import DocumentIndexer

def test_markdown_loader_and_rag_with_readme():
    """Test le chargement du README.md et la recherche RAG d'une information dedans."""
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        pytest.skip("Le fichier README.md n'est pas présent à la racine.")

    loader = MarkdownLoader()
    doc = loader.load(readme_path)

    assert doc is not None
    assert doc.id == "README.md"
    assert len(doc.content) > 0
    print(f"\n[Loader MD] README chargé avec succès ({len(doc.content)} caractères).")

    # Test RAG sur le README
    try:
        embedding = OllamaEmbedding()
    except Exception:
        pytest.skip("Ollama non disponible pour le test vectoriel du README.")

    vector_store = MemoryVectorStore(similarity=CosineSimilarity())
    chunker = FixedChunker(chunk_size=400, embedding=embedding)
    indexer = DocumentIndexer(chunker=chunker, embedding=embedding, vector_store=vector_store)
    retriever = VectorRetriever(vector_store=vector_store, embedding=embedding)

    indexer.index(doc)

    query = "Quel est l'objectif ou le langage principal du projet ?"
    results = retriever.retrieve(query, k=3)

    assert len(results) > 0
    combined_content = " ".join([r.chunk.content for r in results])
    print(f"[RAG README] Résultat trouvé pour '{query}' : \n{combined_content[:200]}...")

    assert "python" in combined_content.lower() or "assistant" in combined_content.lower(), \
        "Le RAG doit retrouver les informations principales du README."

def test_pdf_loader_and_rag_with_cv():
    """Test le chargement du CV PDF et la recherche de l'école (avec k=2 pour ratisser plus large)."""
    cv_paths = ["data/cv.pdf", "cv.pdf", "CV.pdf"]
    cv_path = next((p for p in cv_paths if os.path.exists(p)), None)

    if not cv_path:
        pytest.skip("Aucun fichier CV PDF trouvé (placez-le à la racine ou dans data/cv.pdf).")

    loader = PDFLoader()
    doc = loader.load(cv_path)

    assert doc is not None
    assert len(doc.content) > 0
    print(f"\n[Loader PDF] CV chargé depuis {cv_path} ({len(doc.content)} caractères).")

    try:
        embedding = OllamaEmbedding()
    except Exception:
        pytest.skip("Ollama non disponible pour le test vectoriel du CV.")

    vector_store = MemoryVectorStore(similarity=HybridSimilarity())
    # On ajuste un chunk_size un peu plus large pour garder le bloc de formation groupé
    chunker = FixedChunker(chunk_size=400, embedding=embedding)
    indexer = DocumentIndexer(chunker=chunker, embedding=embedding, vector_store=vector_store)
    retriever = VectorRetriever(vector_store=vector_store, embedding=embedding)

    indexer.index(doc)

    query = "Quelle est l'école d'ingénieur ?"
    # On passe k=2 pour récupérer un peu plus de contexte si les chunks sont coupés
    results = retriever.retrieve(query, k=2)

    assert len(results) > 0
    combined_chunks = " ".join([r.chunk.content for r in results])
    print(f"[RAG CV] Résultats combinés (k=2) pour '{query}' : \n{combined_chunks}")

    # Vérification élargie sur l'ensemble des top chunks remontés
    found_school = "telecom" in combined_chunks.lower() or "sudparis" in combined_chunks.lower()
    if found_school:
        print("[RAG CV] Succès : Télécom SudParis a bien été retrouvé dans les chunks du CV !")
    else:
        print("[RAG CV] Attention : L'école n'apparaît pas encore dans les top 2 chunks. Vérifiez l'exactitude du texte extrait du PDF.")
    
    assert found_school, "Le RAG doit réussir à extraire l'information sur l'école d'ingénieur du CV."