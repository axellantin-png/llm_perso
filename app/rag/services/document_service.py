from app.rag.loaders.text_loader import TextLoader
from app.rag.loaders.markdown_loader import MarkdownLoader
from app.rag.loaders.pdf_loader import PDFLoader



class DocumentService : 


    def __init__(self, loader, indexer):
        self.loader = loader 
        self.indexer = indexer 

    def important_document(self, path):
        document = self.loader.load(path)
        self.indexer.index(document)


    def get_loader_for_file(file_path: str):
        """Factory simple pour retourner le bon loader selon l'extension du fichier."""
        if file_path.endswith(".md"):
            return MarkdownLoader()
        elif file_path.endswith(".pdf"):
            return PDFLoader()
        else:
            return TextLoader()