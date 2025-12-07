from dataclasses import dataclass, field

# Posting List (PL) это своего рода таблица связей слово-документ, где к каждому слову есть ссылка на документ, где оно встрачается и сколько раз

@dataclass
class pl:
    word_id: int
    doc_id: int
    count: int = field(init=False, default=0)  # по дефолту 0, меняется по мере подсчёта
