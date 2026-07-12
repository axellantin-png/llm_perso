from app.services.conversation_service import ConversationService


class ChatService:


    def __init__( self,llm,repository):
        self.llm = llm
        self.repository = repository
        self.conversationService = ConversationService(repository)


    def stream_response_origin(self,conversation_id,message):

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

    def stream_response (self, conversation_id, message):

        conversation = self.conversationService.get(conversation_id)

        self.conversationService.add_user_message(message = message, conversation = conversation)

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

        self.conversationService.add_assistant_message(
            conversation,
            full_response
        )
        
    
        

