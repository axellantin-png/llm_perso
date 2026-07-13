from abc import ABC, abstractmethod


class Tokenizer(ABC):

    @abstractmethod
    def count(self, text: str) -> int:
        pass