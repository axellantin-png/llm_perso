from dataclasses import dataclass
from datetime import datetime


@dataclass
class GenerationMetrics:

    model: str 

    provider: str

    message_count: int

    input_characters: int

    output_characters: int

    input_tokens: int

    output_tokens: int

    generation_time: float

    tokens_per_second: float

    timestamp: datetime 

    def __post_init__(self):

        self.tokens_per_second = (
            self.output_tokens / self.generation_time
            if self.generation_time > 0
            else 0
        )