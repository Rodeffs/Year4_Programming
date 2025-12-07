from data.doc import doc
from typing import Iterable


class doc_repo:
    def __init__(self) -> None:
        self.data = []

    def get_all(self) -> Iterable[doc]:  # вернуть все документы
        for entry in self.data:
            yield entry

    def get_id(self, doc_id) -> doc | None:  # вернуть документ по id
        for entry in self.data:
            if entry.doc_id == doc_id:
                return entry

        return None

    def get_name(self, name) -> doc | None:  # вернуть документ по имени
        for entry in self.data:
            if entry.name == name:
                return entry

        return None

    def add(self, doc) -> None:  # добавить документ
        self.data.append(doc)

    def remove(self, doc) -> None:  # удалить документ
        try:
            self.data.remove(doc)

        except ValueError:  # если такого документа нет, то ничего не делать
            return
