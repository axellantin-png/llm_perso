class FakeVectorStore:

    def __init__(self):

        self.saved = []

    def add(
        self,
        chunks
    ):

        self.saved.extend(chunks)