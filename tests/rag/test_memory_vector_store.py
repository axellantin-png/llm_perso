from app.rag.vectorstores.memory_vector_store import MemoryVectorStore
from app.rag.similarity.cosine_similarity import CosineSimilarity
from app.rag.models.chunk import Chunk



def testSearch() : 

    store = MemoryVectorStore(
        similarity=CosineSimilarity()
    )

    chunk_python = Chunk(
        content="Python",
        embedding=[1,0]
    )

    chunk_paris = Chunk(
        content="Paris",
        embedding=[0,1]
    )

    store.add([chunk_python, chunk_paris])

    results = store.search(
        embedding=[1,0],
        k=1
    )

    assert len(results) == 1
    assert results[0].content == "Python"

def testSearchEmpty(): 

    store = MemoryVectorStore(
        similarity=CosineSimilarity()
    )

    results = store.search(
        embedding=[1,0]
    )

    assert len(results) == 0

def testClear() : 
    store = MemoryVectorStore(
        similarity=CosineSimilarity()
    )

    chunk_python = Chunk(
        content="Python",
        embedding=[1,0]
    )

    chunk_paris = Chunk(
        content="Paris",
        embedding=[0,1]
    )

    store.add([chunk_python, chunk_paris])

    store.clear()

    assert len(store.chunks) == 0

    