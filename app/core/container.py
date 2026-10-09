from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.database.database import Database
from app.rag.vectorstores.sqlite_vector_store import SQLiteVectorStore
from app.rag.embeddings.ollama_embeddings import OllamaEmbedding
from app.rag.chunkers.fixed_chunker import FixedChunker
from app.rag.services.document_indexer import DocumentIndexer
from app.rag.loaders.text_loader import TextLoader
from app.rag.services.document_service import DocumentService
from app.services.chat_service import ChatService
from app.repositories.sqlite_repository import SQLiteRepository
from app.llm.ollama_client import OllamaClient
from app.services.conversation_service import ConversationService
from app.tokenizers.simple_tokenizer import SimpleTokenizer
from app.rag.similarity.cosine_similarity import CosineSimilarity
from app.rag.retrievers.vector_retriever import VectorRetriever
from app.services.chat_service_with_retriever import ChatServiceWithRetriever

router = APIRouter()

database = Database()
database.initialize()

repository = SQLiteRepository(database)

llm = OllamaClient()

# Changement majeur : on utilise maintenant la persistance !
vector_store = SQLiteVectorStore(database=database, similarity=CosineSimilarity())

embedding = OllamaEmbedding()

chunker = FixedChunker(chunk_size=500, embedding=embedding)  # J'ai mis 500 pour que le RAG ait du sens (5 c'était très petit !)

tokenizer = SimpleTokenizer()

indexer = DocumentIndexer(
    chunker,
    embedding,
    vector_store
)

loader = TextLoader()

conversation_service = ConversationService(
    repository
)

# Création du retriever vectoriel
retriever = VectorRetriever(vector_store=vector_store, embedding=embedding)

# chat-service avec RAG (injection corrigée avec conversationService au lieu de conversation_service)
chat_service_with_retriever = ChatServiceWithRetriever(
    llm=llm,
    repository=repository,
    conversationService=conversation_service,
    tokenizer=tokenizer,
    retriever=retriever
)

# chat-service sans le RAG
chat_service = ChatService(
    OllamaClient(),
    repository,
    conversation_service,
    tokenizer
)

document_service = DocumentService(
    TextLoader(),
    indexer
)