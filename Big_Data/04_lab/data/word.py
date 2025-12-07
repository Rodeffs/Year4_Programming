from dataclasses import dataclass  # просто для упрощения кода


@dataclass
class word:
    word_id: int
    word_str: str
    weight: int
