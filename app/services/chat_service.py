from app.memory.memory import (
    add_message,
    get_history
)

from app.llm.client import stream_chat


class ChatService:


    def __init__(self, llm):

        self.llm = llm

    def stream_response(self, message):

        add_message(
            "user",
            message
        )

        messages = get_history()

        full_response = ""

        generator = self.llm.stream_chat(messages)

        while True:

            try:

                token = next(generator)

                full_response += token

                yield token

            except StopIteration:

                break

        add_message(
            "assistant",
            full_response
        )