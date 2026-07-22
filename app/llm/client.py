from abc import ABC, abstractmethod


class LLMClient(ABC):

    @abstractmethod
    def stream_chat(self, messages):
        pass

    @property
    def model(self):
        pass

    @property
    def provider(self):
        pass

