from app.memory.memory import (
    add_message,
    get_history
)

from app.llm.client import stream_chat


class ChatService:


    def __init__( self,llm,conversation_manager):
        self.llm = llm
        self.conversation_manager = conversation_manager

    def stream_response(self,conversation_id,message):

        conversation = (
            self.conversation_manager.get(
                conversation_id
            )
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