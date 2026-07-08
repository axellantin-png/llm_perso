import requests


def ask_llm(message):
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "mistral:latest",
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "stream": False
        }
    )

    return response.json()["message"]["content"]


if __name__ == "__main__":
    answer = ask_llm("Bonjour, qui es-tu ?")
    print(answer)