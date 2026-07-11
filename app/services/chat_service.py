from app.memory.memory import (
    add_message,
    get_history
)

from app.memory.memory import get_history


class ChatService:


    def __init__( self,llm,repository):
        self.llm = llm
        self.repository = repository

    def stream_response(self,conversation_id,message):

        conversation = self.repository.get(
            conversation_id
        )


        conversation.add_message(
            "user",
            message
        )


        messages = [
            {
                "role": m.role,
                "content": m.content
            }
            for m in conversation.messages
        ]


        full_response = ""


        for token in self.llm.stream_chat(messages):

            full_response += token

            yield token


        conversation.add_message(
            "assistant",
            full_response
        )