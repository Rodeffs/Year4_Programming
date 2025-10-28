from dataclasses import dataclass, field


@dataclass
class Document:
    doc_id: int
    name: str
    path: str
    length: int = field(init=False, default=0, repr=False)  # default - значение по умолчанию , init - будет ли в конструкторе, repr - будет ли выводится
    weight: int

'''
# То же самое, но более громоздко

class Document:
    def __init__(self, doc_id, name, path, length):
        self.doc_id = doc_id
        self.name = name
        self.path = path
        self.length = length


    def __str__(self):
        return f"doc_id = {self.doc_id}, name = {self.name}, path = {self.path}, length = {self.length}"

    def __eq__(self, other):
        return (self.doc_id == other.doc_id and self.name == other.name and self.path == other.path and self.length == other.length)
'''

@dataclass
class Word:
    word_id: int
    word: str
    weight: int


@dataclass
class PostingList:
    pl_id: int
    word_id: int
    doc_id: int
    tf_idf: float


