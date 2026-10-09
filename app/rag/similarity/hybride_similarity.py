from app.rag.similarity.similarity import Similarity
from app.rag.similarity.cosine_similarity import CosineSimilarity

class HybridSimilarity(Similarity):
    """
    Similarité hybride combinant :
    - La similarité sémantique (Cosinus sur les embeddings)
    - La similarité lexicale (Correspondance de mots-clés exacts)
    """
    def __init__(self, semantic_weight: float = 0.7, lexical_weight: float = 0.3):
        self.semantic_similarity = CosineSimilarity()
        self.semantic_weight = semantic_weight
        self.lexical_weight = lexical_weight

    def score(self, embedding_a: list[float], embedding_b: list[float], text_a: str = "", text_b: str = "") -> float:
        """
        Note: Pour être totalement compatible avec l'interface de base de Similarity qui ne prend que 
        les embeddings, nous gérons des arguments optionnels ou un calcul hybride. 
        Si les textes ne sont pas fournis, on se replie sur le pur cosinus.
        """
        # 1. Score sémantique (cosinus)
        semantic_score = self.semantic_similarity.score(embedding_a, embedding_b)

        # Si aucun texte n'est fourni, on ne peut pas faire du lexical pur, on retourne le sémantique
        if not text_a or not text_b:
            return semantic_score

        # 2. Score lexical simple (Jaccard / correspondance de mots)
        lexical_score = self._compute_lexical_score(text_a, text_b)

        # 3. Score combiné pondéré
        final_score = (self.semantic_weight * semantic_score) + (self.lexical_weight * lexical_score)
        return final_score

    def _compute_lexical_score(self, text_a: str, text_b: str) -> float:
        """
        Calcule un score lexical basé sur l'intersection des mots (Jaccard simplifié).
        """
        # Nettoyage et tokenisation basique par mots en minuscules
        words_a = set(text_a.lower().split())
        words_b = set(text_b.lower().split())

        if not words_a or not words_b:
            return 0.0

        intersection = words_a.intersection(words_b)
        union = words_a.union(words_b)

        # Indice de Jaccard
        return len(intersection) / len(union) if union else 0.0