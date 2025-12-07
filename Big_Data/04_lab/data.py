from dataclasses import dataclass, field


@dataclass
class Doc:
    doc_id: int = field(init=False, default=-1)  # репозиторий сам будет задавать id, так что по дефолту он -1
    url: str
    weight: float


@dataclass
class PL:  # Posting List (PL) это своего рода таблица связей слово-документ, где к каждому слову есть ссылка на документы, где оно встрачается и сколько раз
    word_id: int
    doc_id: int
    count: int = field(init=False, default=1)  # по дефолту 1, меняется по мере подсчёта


@dataclass
class Word:
    word_id: int = field(init=False, default=-1)  # репозиторий сам будет задавать id, так что по дефолту он -1
    word_str: str
    weight: float = field(init=False, default=0.0)  # дефолтный вес у всех слов 0, потом уже будут задаваться отдельные веса
