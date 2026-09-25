from app.llm.prompts.system import SYSTEM_PROMPT
from app.monitoring.generation_metrics import GenerationMetrics
import time 
from datetime import datetime


class ChatServiceWithRetriever:

    def stream_response (self, conversation_id, message):

        conversation = self.conversationService.get(conversation_id)

        self.conversationService.add_user_message(message = message, conversation = conversation)

        results = self.retriever.retrieve(
                    message
                )
        
        context = "\n\n".join(
            result.chunk.content
            for result in results
        )

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        if context:

            messages.append(
                {
                    "role": "system",
                    "content":
                        f"Contexte :\n\n{context}"
                }
            )


        messages.extend(
            [
                {
                    "role": m.role,
                    "content": m.content
                }
                for m in conversation.messages
            ]
        )

        input_text = "\n".join( message["content"] for message in messages)

        input_tokens = self.tokenizer.count(input_text) 


        full_response = ""


        start = time.perf_counter()

        for token in self.llm.stream_chat(messages):

            full_response += token

            yield token

        generation_time = time.perf_counter() - start

        output_tokens = self.tokenizer.count(full_response)

        input_characters = len(input_text)

        output_characters = len(full_response)

        message_count = len(messages) -1

        metrics = GenerationMetrics(
            model=self.llm.model, 
            provider = self.llm.provider, 
            message_count = message_count,
            input_characters = input_characters, 
            output_characters = output_characters, 
            input_tokens = input_tokens, 
            output_tokens = output_tokens, 
            generation_time = generation_time,
            tokens_per_second = 0,
            timestamp = datetime.now()
        )
        
        print(metrics)

        self.conversationService.add_assistant_message(
            conversation,
            full_response
        )


    def stream_response_without_metrics  (self, conversation_id, message):

        conversation = self.conversationService.get(conversation_id)

        self.conversationService.add_user_message(message = message, conversation = conversation)

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        results = self.retriever.retrieve(
                            message
                        )
                
        context = "\n\n".join(
            result.chunk.content
            for result in results
        )

        if context:
        
            messages.append(
                {
                    "role": "system",
                    "content":
                        f"Contexte :\n\n{context}"
                }
            )


        messages.extend(
            [
                {
                    "role": m.role,
                    "content": m.content
                }
                for m in conversation.messages
            ]
        )

        full_response = ""

        for token in self.llm.stream_chat(messages):

            full_response += token

            yield token

        self.conversationService.add_assistant_message(
            conversation,
            full_response
        )
        
    
        

