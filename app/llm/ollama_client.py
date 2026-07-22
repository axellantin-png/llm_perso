import json
import requests

from app.config import MODEL, OLLAMA_URL

from app.llm.client import LLMClient

class OllamaClient(LLMClient):

    def stream_chat(self, messages):

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "stream": True
            },
            stream=True
        )

        response.raise_for_status()

        full_response = ""

        for line in response.iter_lines():

            if not line:
                continue

            data = json.loads(line)

            if "message" not in data:
                continue

            token = data["message"]["content"]

            full_response += token

            yield token

        return full_response
    
    @property
    def model(self):
        return MODEL

    @property
    def provider(self):
        return OLLAMA_URL
