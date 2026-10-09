from app.rag.loaders.document_loader import DocumentLoader
from app.rag.models.document import Document
import pypdf

class PDFLoader(DocumentLoader):
    """
    Loader pour charger des documents au format PDF (.pdf).
    """
    def load(self, file_path: str) -> Document:
        reader = pypdf.PdfReader(file_path)
        content = ""
        
        # Extraction du texte de toutes les pages du PDF
        for page in reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                content += extracted_text + "\n"
        
        doc_id = file_path.split("/")[-1]
        return Document(id=doc_id, content=content.strip())