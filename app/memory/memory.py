from app.llm.prompts import SYSTEM_PROMPT

conversation = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


def add_message(role, content):
    conversation.append(
        {
            "role": role,
            "content": content
        }
    )



def get_history():
    return conversation


def clear_memory():
    conversation.clear()