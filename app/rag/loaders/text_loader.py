from app.rag.loaders.document_loader import DocumentLoader
from app.rag.models.document import Document
from pathlib import Path 

class TextLoader(DocumentLoader) : 


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
    

    def load_with_owner(self, path:str, owner_id) : 
        with open(path, encoding="utf8") as file:
            content = file.read()

        title = Path(path).stem
        document = document = Document(
            owner_id=owner_id,
            title= title,
            content= content
        )
        return document
