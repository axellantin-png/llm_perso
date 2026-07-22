

class DocumentService : 


    def __init__(self, loader, indexer):
        self.loader = loader 
        self.indexer = indexer 

    def important_document(self, path):
        document = self.loader.load(path)
        self.indexer.index(document)