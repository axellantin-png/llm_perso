from app.llm.prompts import SYSTEM_PROMPT
from app.models.conversation import Conversation

conversation = Conversation()


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