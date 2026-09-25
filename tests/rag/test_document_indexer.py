from app.rag.services.document_indexer import DocumentIndexer
from app.rag.chunkers.fixed_chunker import FixedChunker
from app.rag.models.document import Document
from tests.fake_class.fake_embedding import FakeEmbedding
from tests.fake_class.fake_vectore_store import FakeVectorStore

def test_indexer() : 

    ## definitions des elements du test
    embedding= FakeEmbedding()
    chunker = FixedChunker(chunk_size=5, embedding= embedding)
    store = FakeVectorStore()
    indexer = DocumentIndexer(chunker= chunker, embedding = embedding , vector_store= store)
    document = Document(
        owner_id="Axel",
        title="Test",
        content="abcdefghij"
    )

    # test en lui même
    indexer.index(document)
    assert len(store.saved) == 4
    assert store.saved[0].embedding == [1,2,3]