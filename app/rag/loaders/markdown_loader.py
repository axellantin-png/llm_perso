from app.rag.loaders.document_loader import DocumentLoader
from app.rag.models.document import Document

class MarkdownLoader(DocumentLoader):
    """
    Loader pour charger des documents au format Markdown (.md).
    """
    def load(self, file_path: str) -> Document:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # On peut extraire un titre ou utiliser le chemin comme ID
        doc_id = file_path.split("/")[-1]
        return Document(id=doc_id, content=content)