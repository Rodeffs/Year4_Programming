from data.word import word
from typing import Iterable


class word_repo:
    def __init__(self) -> None:
        self.data = []

    def get_all(self) -> Iterable[word]:  # вернуть все слова
        for entry in self.data:
            yield entry

    def get_id(self, word_id) -> word | None:  # вернуть слово по id
        for entry in self.data:
            if entry.word_id == word_id:
                return entry

        return None

    def get_word(self, word_str) -> word | None:  # вернуть по слову
        for entry in self.data:
            if entry.word_str == word_str:
                return entry

        return None

    def add(self, word) -> None:  # добавить слово
        self.data.append(word)

    def remove(self, word) -> None:  # удалить слово
        try:
            self.data.remove(word)

        except ValueError:  # если такого слова нет, то ничего не делать
            return
