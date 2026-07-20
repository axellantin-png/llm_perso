import numpy as np
from app.rag.similarity.similarity import Similarity


class CosineSimilarity(Similarity):

    def score(
        self,
        vector1: list[float],
        vector2: list[float]
    ) -> float:

        v1 = np.array(vector1)
        v2 = np.array(vector2)

        return np.dot(v1, v2) / (
            np.linalg.norm(v1) * np.linalg.norm(v2)
        )