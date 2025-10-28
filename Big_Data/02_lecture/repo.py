from abc import ABC, abstractmethod
from models import Document, DocumentLink


class DocumentRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Document]:
        ...

    @abstractmethod
    def get_by_id(self, doc_id) -> Document | None:
        ...


class DocumentLinkRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[DocumentLink]:
        ...

    @abstractmethod
    def get_docs_to(self, doc_id) -> list[DocumentLink]:
        ...
