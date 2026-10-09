import math
from app.rag.similarity.similarity import Similarity

class DotProductSimilarity(Similarity):
    """
    Implémentation de la similarité par Produit Scalaire.
    """
    def score(self, embedding_a: list[float], embedding_b: list[float]) -> float:
        if not embedding_a or not embedding_b or len(embedding_a) != len(embedding_b):
            return 0.0
        
        # Calcul du produit scalaire
        return sum(a * b for a, b in zip(embedding_a, embedding_b))