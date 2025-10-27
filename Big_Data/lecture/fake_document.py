from typing import Iterable

from data import Document
from document_repository import DocumentRepository

class FakeDocumentRepository(DocumentRepository):
    def __init__(self) -> None:
        self.data = [Document(doc_id=1, name="kantiana.ru", path="/", weight=1),
                     Document(doc_id=2, name="rwe.com", path="/", weight=2),
                     Document(doc_id=3, name="wmim.org", path="/", weight=3)]


    def all(self) -> Iterable[Document]:
        for word in self.data:
            yield word

    def get_by_id(self, doc_id) -> Document | None:
        for doc in self.data:
            if doc.doc_id == doc_id:
                return doc

        return None

    def add(self, document) -> None:
        self.data.append(document)

