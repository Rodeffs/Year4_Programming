from repo import DocumentRepository, DocumentLinkRepository
from models import Document, DocumentLink


class FakeDocumentRepository(DocumentRepository):
    def __init__(self):
        self._data = [Document(0, "kantiana.ru", 0.7),
                      Document(1, "google.com", 0.8),
                      Document(2, "linux.org", 0.4),
                      Document(3, "archlinux.org", 0.5),
                      ]


    def get_all(self) -> list[Document]:
        return self._data


    def get_by_id(self, doc_id) -> Document | None:
        for doc in self.get_all():
            if doc_id == doc.id:
                return doc

        return None


class FakeDocumentLinkRepository(DocumentLinkRepository):
    def __init__(self):
        self._data = [DocumentLink(0, 0, 1),
                      DocumentLink(1, 0, 2),
                      DocumentLink(2, 0, 1),
                      DocumentLink(3, 0, 1),
                      DocumentLink(4, 0, 3),

                      DocumentLink(5, 1, 1),
                      DocumentLink(6, 1, 1),
                      DocumentLink(7, 1, 2),
                      DocumentLink(8, 1, 2),


                      DocumentLink(9, 2, 1),
                      DocumentLink(10, 2, 2),
                      DocumentLink(11, 2, 2),
                      DocumentLink(12, 2, 1),
                        

                      DocumentLink(13, 3, 0),
                      DocumentLink(14, 3, 1),
                      DocumentLink(15, 3, 2)]

    def get_all(self) -> list[DocumentLink]:
        return self._data


    def get_docs_to(self, doc_id) -> list[int]:
        ls = []

        for link in self.get_all():
            if link.id_from == doc_id:
                ls.append(link.id_to)

        return ls
