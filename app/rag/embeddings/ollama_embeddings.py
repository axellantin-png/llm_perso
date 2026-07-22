from app.rag.embeddings.embedding import Embedding
import json 
import requests


class OllamaEmbedding(Embedding):

    def __init__(self, model="nomic-embed-text"):
        self.model = model


    def embed(self, text: str) -> list[float]:
        url = "http://localhost:11434/api/embed"
        payload = {
            "model": "nomic-embed-text",  # À remplacer par ton modèle si nécessaire
            "input": text
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            # Optionnel : tu peux laisser cette ligne si tu veux toujours voir le JSON complet
            # print(json.dumps(data, indent=4))
            
            # Ollama renvoie une liste de vecteurs dans la clé 'embeddings' 
            # (un pour chaque texte envoyé dans 'input'). On prend le premier [0].
            return data["embeddings"][0]
            
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête Ollama : {e}")
            return []



embedding = OllamaEmbedding()

vector = embedding.embed(
    "Bonjour"
)

print(len(vector))