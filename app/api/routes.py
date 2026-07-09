from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.chat_service import ChatService

router = APIRouter()

service = ChatService()


class ChatRequest(BaseModel):
    message: str


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

@router.post("/conversation")
def create_conversation():

    conversation = manager.create()

    return {
        "id": conversation.id
    }