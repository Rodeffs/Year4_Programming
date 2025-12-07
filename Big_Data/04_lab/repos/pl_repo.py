from data.pl import pl
from typing import Iterable


class pl_repo:
    def __init__(self) -> None:
        self.data = []

    def get_all(self) -> Iterable[pl]:  # вернуть все posting list
        for entry in self.data:
            yield entry

    def get_doc_id(self, doc_id) -> Iterable[pl]:  # вернуть все posting list, где есть ссылка на этот документ
        for entry in self.data:
            if entry.doc_id == doc_id:
                yield entry

    def get_word_id(self, word_id) -> Iterable[pl]:  # вернуть все posting list, где есть ссылка на это слово
        for entry in self.data:
            if entry.word_id == word_id:
                yield entry

    def add(self, pl) -> None:  # добавить posting list
        self.data.append(pl)

    def remove(self, pl) -> None:  # удалить posting list
        try:
            self.data.remove(pl)

        except ValueError:  # если такого posting list нет, то ничего не делать
            return
