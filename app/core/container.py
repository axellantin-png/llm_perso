from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.database.database import Database
from app.rag.vectorstores.memory_vector_store import MemoryVectorStore
from app.rag.embeddings.ollama_embeddings import OllamaEmbedding
from app.rag.chunkers.fixed_chunker import FixedChunker
from app.rag.services.document_indexer import DocumentIndexer
from app.rag.loaders.text_loader import TextLoader
from app.rag.services.document_service import DocumentService
from app.services.chat_service import ChatService
from app.repositories.sqlite_repository import SQLiteRepository
from app.llm.ollama_client import OllamaClient
from app.database.database import Database
from app.services.conversation_service import ConversationService
from app.tokenizers.simple_tokenizer import SimpleTokenizer
from app.rag.similarity.cosine_similarity import CosineSimilarity

router = APIRouter()

database = Database()
database.initialize()

repository = SQLiteRepository(database)

llm = OllamaClient()

vector_store = MemoryVectorStore(similarity=CosineSimilarity())

embedding = OllamaEmbedding()

chunker = FixedChunker(chunk_size=5, embedding= embedding)

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