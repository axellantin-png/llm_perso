from app.llm.prompts.system import SYSTEM_PROMPT
from app.monitoring.generation_metrics import GenerationMetrics
import time 
from datetime import datetime


class ChatServiceWithRetriever:

    def stream_response (self, conversation_id, message):

        avec_sources = False

        conversation = self.conversationService.get(conversation_id)

        self.conversationService.add_user_message(message = message, conversation = conversation)

        # 1. Récupération des résultats via le retriever
        results = self.retriever.retrieve(message)
        
        # 2. Construction du contexte et collecte des sources
        context_parts = []
        sources = set()

        for result in results:
            # Si le chunk a un parent, on privilégie le parent pour donner plus de confort au LLM
            text_to_use = result.chunk.parent_content if result.chunk.parent_content else result.chunk.content
            context_parts.append(text_to_use)
            source_name = getattr(result.chunk, "document_id", "Document inconnu")
            sources.add(source_name)


        context = "\n\n".join(context_parts)
        

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

        if (not(avec_sources)) : 
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
        else : 

            # Formatage des sources à ajouter à la fin de la réponse assistant
            sources_text = "\n\n**Sources :**\n" + "\n".join(f"- {src}" for src in sources)
            
            # Si vous souhaitez l'injecter dans le message sauvegardé en base :
            full_response_with_sources = full_response + sources_text

            output_tokens = self.tokenizer.count(full_response_with_sources)

            input_characters = len(input_text)

            output_characters = len(full_response_with_sources)

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
                full_response_with_sources
            )


    def stream_response_without_metrics  (self, conversation_id, message):

        avec_sources = False 

        conversation = self.conversationService.get(conversation_id)

        self.conversationService.add_user_message(message = message, conversation = conversation)

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        # 1. Récupération des résultats via le retriever
        results = self.retriever.retrieve(message)
        
        # 2. Construction du contexte et collecte des sources
        context_parts = []
        sources = set()

        for result in results:
            # Si le chunk a un parent, on privilégie le parent pour donner plus de confort au LLM
            text_to_use = result.chunk.parent_content if result.chunk.parent_content else result.chunk.content
            context_parts.append(text_to_use)
            source_name = getattr(result.chunk, "document_id", "Document inconnu")
            sources.add(source_name)

        context = "\n\n".join(context_parts)

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

        if (not(avec_sources)) : 
            self.conversationService.add_assistant_message(
                conversation,
                full_response
            )
        else :
            # Formatage des sources à ajouter à la fin de la réponse assistant
            sources_text = "\n\n**Sources :**\n" + "\n".join(f"- {src}" for src in sources)
            
            # Si vous souhaitez l'injecter dans le message sauvegardé en base :
            full_response_with_sources = full_response + sources_text

            self.conversationService.add_assistant_message(
                            conversation,
                            full_response_with_sources
                        )
        
    
        

