from pydantic import BaseModel


class MessageResponse(BaseModel):

    role: str
    content: str



class ConversationResponse(BaseModel):

    id: str
    title: str
    messages: list[MessageResponse]