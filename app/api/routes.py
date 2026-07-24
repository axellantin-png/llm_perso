####################################################################################################################################
# imports
####################################################################################################################################
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.core.container import router
from app.core.container import chat_service
from app.core.container import conversation_service
from app.core.container import database

from app.api.schemas import ConversationResponse



####################################################################################################################################
# pseudo classes 
####################################################################################################################################

class RenameConversationRequest(BaseModel):

    title: str


####################################################################################################################################
# Code
####################################################################################################################################

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
        chat_service.stream_response(
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

@router.delete("/conversation/{conversation_id}")
def delete_conversation(
    conversation_id: str
):

    conversation_service.delete(
        conversation_id
    )

    return {
        "status":"deleted"
    }


