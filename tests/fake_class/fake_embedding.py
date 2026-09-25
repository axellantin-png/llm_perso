class FakeEmbedding:

    def embed(self, text):

        if "python" in text.lower():
            return [1,0]

        if "voiture" in text.lower():
            return [0,1]

        return [0,0]