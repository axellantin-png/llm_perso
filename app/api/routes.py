from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.chat_service import ChatService
from app.repositories.memory_repository import MemoryRepository
from app.llm.client import OllamaClient


router = APIRouter()


repository = MemoryRepository()

service = ChatService(
    OllamaClient(),
    repository
)


class ChatRequest(BaseModel):
    message: str



@router.post("/conversation")
def create_conversation():

    conversation = repository.create()

    return {
        "id": conversation.id
    }



@router.post("/chat/{conversation_id}")
def chat(
    conversation_id: str,
    request: ChatRequest
):

    return StreamingResponse(
        service.stream_response(
            conversation_id,
            request.message
        ),
        media_type="text/plain"
    )

