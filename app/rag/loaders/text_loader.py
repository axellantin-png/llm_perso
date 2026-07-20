from app.rag.loaders.document_loader import DocumentLoaders
from app.rag.models.document import Document
from pathlib import path 

class TextLoader(DocumentLoaders) : 


    def load(self, path:str) : 
        with open(path, encoding="utf8") as file:
            content = file.read()

        title = Path(path).stem
        document = document = Document(
            owner_id="all",
            title= title,
            content= content
        )
        return document
