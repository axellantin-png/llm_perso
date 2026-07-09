from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.chat_service import ChatService

router = APIRouter()

service = ChatService()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(request: ChatRequest):

    return StreamingResponse(
        service.stream_response(
            request.message
        ),
        media_type="text/plain"
    )