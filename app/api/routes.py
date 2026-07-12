####################################################################################################################################
# imports
####################################################################################################################################
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.chat_service import ChatService
from app.repositories.memory_repository import MemoryRepository
from app.repositories.sqlite_repository import SQLiteRepository
from app.llm.ollama_client import OllamaClient
from app.database.database import Database
from app.services.conversation_service import ConversationService
from app.api.schemas import ConversationResponse

####################################################################################################################################
# pseudo classes 
####################################################################################################################################

class RenameConversationRequest(BaseModel):

    title: str


####################################################################################################################################
# Code
####################################################################################################################################

database = Database()

database.initialize()

router = APIRouter()


# repository = MemoryRepository()
repository = SQLiteRepository(database)

conversation_service = ConversationService(
    repository
)

service = ChatService(
    OllamaClient(),
    repository,
    conversation_service
)


class ChatRequest(BaseModel):
    message: str



@router.post("/conversation")
def create_conversation():

    conversation = conversation_service.create()


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

@router.get("/conversations")
def get_conversations():

    return conversation_service.list_conversations()

@router.patch("/conversation/{conversation_id}")
def rename_conversation(
    conversation_id: str,
    request: RenameConversationRequest
):

    conversation = conversation_service.rename(
        conversation_id,
        request.title
    )

    return {
        "id": conversation.id,
        "title": conversation.title
    }


@router.get(
    "/conversation/{conversation_id}",
    response_model=ConversationResponse
)
def get_conversation(
    conversation_id: str
):

    return conversation_service.get(
        conversation_id
    )
