from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.responses import FileResponse
from pathlib import Path

from .config import MODEL, OLLAMA_URL


app = FastAPI(
    title="Mon LLM local",
    description="API personnelle utilisant Ollama",
    version="0.1"
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return FileResponse(
        Path("app/static/index.html")
    )


@app.post("/chat")
def chat(request: ChatRequest):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": request.message
                }
            ],
            "stream": False
        }
    )

    response.raise_for_status()

    result = response.json()

    return {
        "response": result["message"]["content"]
    }