from abc import ABC, abstractmethod
from typing import Iterable

from data import PostingList

class PostingListRepository(ABC):
    @abstractmethod
    def all(self) -> Iterable[PostingList]:
        ...

    @abstractmethod
    def get_by_doc_id(self, doc_id) -> Iterable[PostingList]:
        ...

    @abstractmethod
    def get_by_word_id(self, word_id) -> Iterable[PostingList]:
        ...

    @abstractmethod
    def add(self, posting) -> None:
        ...

    @abstractmethod
    def remove(self, posting) -> None:
        ...

    @abstractmethod
    def update(self, posting) -> None:
        ...
