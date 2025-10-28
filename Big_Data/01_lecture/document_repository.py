from abc import ABC, abstractmethod
from typing import Iterable

from data import Document


class DocumentRepository(ABC):
    @abstractmethod
    def all(self) -> Iterable[Document]:  # протокол
        ...

    @abstractmethod
    def add(self, document) -> None:
        ...

    @abstractmethod
    def get_by_id(self, doc_id) -> Document | None:
        ...

    @abstractmethod
    def remove(self, document) -> None:
        ...

    @abstractmethod
    def update(self, document) -> None:
        ...

