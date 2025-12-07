from typing import Iterable
from data import Doc, Word, PL


class DocLinkRepo:
    def __init__(self) -> None:
        self.__data = []

    def get_all(self) -> Iterable[tuple]:  # вернуть все ссылки между документами
        for entry in self.__data:
            yield entry

    def get_id_from(self, doc_id) -> Iterable[int]:  # вернуть id документов, на которые ссылается этот документ
        for from_id, to_id in self.__data:
            if from_id == doc_id:
                yield to_id

    def get_id_to(self, doc_id) -> Iterable[int]:  # вернуть id документов, ссылающихся на этот документ
        for from_id, to_id in self.__data:
            if to_id == doc_id:
                yield from_id

    def add(self, from_id, to_id) -> None:  # добавить ссылку
        self.__data.append((from_id, to_id))

    def remove(self, from_id, to_id) -> None:  # удалить ссылку
        for entry in self.__data:
            if entry[0] == from_id and entry[1] == to_id:
                self.__data.remove(entry)
                return


class DocRepo:
    def __init__(self) -> None:
        self.__data = []
        self.__last_id = -1

    def get_all(self) -> Iterable[Doc]:  # вернуть все документы
        for entry in self.__data:
            yield entry

    def get_by_id(self, doc_id) -> Doc | None:  # вернуть документ по id
        for entry in self.__data:
            if entry.doc_id == doc_id:
                return entry

        return None

    def get_by_url(self, url) -> Doc | None:  # вернуть документ по ссылке
        for entry in self.__data:
            if entry.url == url:
                return entry

        return None

    def add(self, doc) -> None:  # добавить документ
        self.__last_id += 1
        doc.doc_id = self.__last_id  # автоматически задаём id документу
        self.__data.append(doc)

    def remove(self, doc) -> None:  # удалить документ
        try:
            self.__data.remove(doc)

        except ValueError:  # если такого документа нет, то ничего не делать
            return


class PLRepo:
    def __init__(self) -> None:
        self.data = []

    def get_all(self) -> Iterable[PL]:  # вернуть все posting list
        for entry in self.data:
            yield entry

    def get_doc_id(self, doc_id) -> Iterable[PL]:  # вернуть все posting list, где есть ссылка на этот документ
        for entry in self.data:
            if entry.doc_id == doc_id:
                yield entry

    def get_word_id(self, word_id) -> Iterable[PL]:  # вернуть все posting list, где есть ссылка на это слово
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


class WordRepo:
    def __init__(self) -> None:
        self.__data = []
        self.__last_id = -1

    def get_all(self) -> Iterable[Word]:  # вернуть все слова
        for entry in self.__data:
            yield entry

    def get_by_id(self, word_id) -> Word | None:  # вернуть слово по id
        for entry in self.__data:
            if entry.word_id == word_id:
                return entry

        return None

    def get_by_word(self, word_str) -> Word | None:  # вернуть по слову
        for entry in self.__data:
            if entry.word_str == word_str:
                return entry

        return None

    def add(self, word) -> None:  # добавить слово
        self.__last_id += 1
        word.word_id = self.__last_id  # автоматически задаём id слову
        self.__data.append(word)

    def remove(self, word) -> None:  # удалить слово
        try:
            self.__data.remove(word)

        except ValueError:  # если такого слова нет, то ничего не делать
            return
