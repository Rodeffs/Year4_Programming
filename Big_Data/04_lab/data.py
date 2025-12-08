from dataclasses import dataclass, field


@dataclass
class Doc:
    doc_id: int = field(init=False, default=-1)  # репозиторий сам будет задавать id, так что по дефолту он -1
    url: str
    weight: float
    length: int = field(init=False, default=0)  # сколько всего слов в документе
    links: int = field(init=False, default=0)  # сколько всего внешних ссылок в документе


@dataclass
class PL:  # Posting List (PL) это своего рода таблица связей слово-документ, где к каждому слову есть ссылка на документы, где оно встрачается и сколько раз. Здесь же и будет считаться tf и tf-idf
    word_id: int
    doc_id: int
    count: int = field(init=False, default=0)  # сколько раз слово встретилось в документе
    tf: float = field(init=False, default=0.0)
    tf_idf: float = field(init=False, default=0.0)
    final_rank: float = field(init=False, default=0.0)  # конечный рейтинг, определится page_rank * tf_idf


@dataclass
class Word:
    word_id: int = field(init=False, default=-1)  # репозиторий сам будет задавать id, так что по дефолту он -1
    word_str: str
    doc_count: int = field(init=False, default=0)  # кол-во документов, в которых встретилось это слово
