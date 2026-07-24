from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.core.container import router
from app.core.container import database
from app.core.container import vector_store
from app.core.container import embedding
from app.core.container import indexer
from app.core.container import TextLoader
from app.core.container import document_service 

class DocumentRequest(BaseModel):

    path: str



@router.post("/documents")
def import_document(request: DocumentRequest):

    document_service.import_document(
        request.path
    )

    return {
        "status": "ok"
    }