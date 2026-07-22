from app.rag.models.document import Document
from app.rag.chunkers.fixed_chunker import FixedChunker


def test_split_document():

    document = Document(
        owner_id="Axel",
        title="Test",
        content="abcdefghij"
    )

    chunker = FixedChunker(
        chunk_size=4
    )

    chunks = chunker.split(document)

    assert len(chunks) == 3

    assert chunks[0].content == "abcd"
    assert chunks[1].content == "efgh"
    assert chunks[2].content == "ij"