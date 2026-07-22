from app.tokenizers.tokenizer import Tokenizer


class SimpleTokenizer(Tokenizer):

    def count(self, text: str) -> int:

        return len(text.split())