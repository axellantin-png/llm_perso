from abc import ABC, abstractmethod

class Similarity(ABC):

    @abstractmethod
    def score(
        self,
        vector1,
        vector2
    ) -> float:
        pass