from typing import Iterable

from data import Word
from word_repository import WordRepository

class FakeWordRepository(WordRepository):
    def __init__(self) -> None:
        self.data = [Word(word_id=1, word="Алия", weight=2),
                     Word(word_id=2, word="Иван", weight=1),
                     Word(word_id=3, word="Кристина", weight=2),
                     Word(word_id=4, word="Дарья", weight=2),
                     Word(word_id=5, word="Олег", weight=1),
                     Word(word_id=6, word="Потап", weight=1)]


    def all(self) -> Iterable[Word]:
        for word in self.data:
            yield word

    def get_by_id(self, word_id) -> Word | None:
        for word in self.data:
            if word.word_id == word_id:
                return word

        return None

    def get_by_word(self, word) -> Word | None:
        for w in self.data:
            if w.word == word:
                return word

        return None

    def add(self, word) -> None:
        self.data.append(word)
