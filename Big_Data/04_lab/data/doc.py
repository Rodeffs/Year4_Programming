from dataclasses import dataclass, field


@dataclass
class doc:
    doc_id: int
    name: str
    path: str
    length: int = field(init=False, default=0, repr=False)  # default - значение по умолчанию , init - будет ли в конструкторе, repr - будет ли выводится
    weight: int
