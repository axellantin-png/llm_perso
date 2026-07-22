# petit message parceque ca me stress qu'il n'y ai rien ici


class DocumentIndexer:

    def __init__(
        self,
        chunker,
        embedding,
        vector_store
    ):
        self.chunker = chunker
        self.embedding = embedding 
        self.vector_store = vector_store

    def index(self, document) : 
        chunks = self.chunker.split(document)
        for chunk in chunks :

            chunk.embedding = self.embedding.embed(
                chunk.content
            )

            self.vector_store.add(chunks)