####################################################################################################################################
# imports
####################################################################################################################################
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi import UploadFile, File
import shutil
import os

from app.core.container import router
from app.core.container import chat_service
from app.core.container import chat_service_with_retriever # Pour utiliser le RAG
from app.core.container import conversation_service
from app.core.container import database
from app.core.container import indexer # Pour indexer le fichier uploadé à la volée

from app.api.schemas import ConversationResponse

from app.rag.loaders.pdf_loader import PDFLoader
from app.rag.loaders.markdown_loader import MarkdownLoader
from app.rag.loaders.text_loader import TextLoader

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
    # On utilise maintenant le ChatServiceWithRetriever pour exploiter les documents !
    return StreamingResponse(
        chat_service_with_retriever.stream_response(
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

@router.post("/chat/upload-temp-document")
async def upload_temporary_document(file: UploadFile = File(...)):
    """
    Permet d'uploader un fichier temporairement, de l'indexer immédiatement 
    dans le VectorStore persistant pour que le LLM puisse l'utiliser.
    """
    temp_dir = "data/temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Choix du loader selon l'extension
    if file.filename.endswith(".pdf"):
        loader = PDFLoader()
    elif file.filename.endswith(".md"):
        loader = MarkdownLoader()
    else:
        loader = TextLoader()
        
    document = loader.load(file_path)
    
    # Indexation immédiate dans SQLite
    indexer.index(document)
    
    return {"status": "success", "filename": file.filename, "message": "Document indexé avec succès pour cette session."}