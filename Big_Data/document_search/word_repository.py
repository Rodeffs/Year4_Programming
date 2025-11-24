from abc import ABC, abstractmethod
from typing import Iterable

from data import Word

class WordRepository(ABC):
    @abstractmethod
    def all(self) -> Iterable[Word]:  # протокол
        ...

    @abstractmethod
    def add(self, word) -> None:
        ...

    @abstractmethod
    def get_by_id(self, word_id) -> Word | None:
        ...

    @abstractmethod
    def get_by_word(self, word) -> Word | None:
        ...

    @abstractmethod
    def remove(self, document) -> None:
        ...

    @abstractmethod
    def update(self, document) -> None:
        ...

