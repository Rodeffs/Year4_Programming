from dataclasses import dataclass


@dataclass
class Document:
    id: int
    url: str
    weight: float

@dataclass
class DocumentLink:
    id: int
    id_from: int
    id_to: int
