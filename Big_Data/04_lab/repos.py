from typing import Iterable
from data import Doc, Word, PL, DocLink


class DocLinkRepo:
    def __init__(self) -> None:
        self.__data = []

    def get_all(self) -> Iterable[DocLink]:  # вернуть все ссылки между документами
        for entry in self.__data:
            yield entry

    def get_id_from(self, doc_id) -> Iterable[DocLink]:  # вернуть id документов, на которые ссылается этот документ
        for entry in self.__data:
            if entry.doc_from_id == doc_id:
                yield entry

    def get_id_to(self, doc_id) -> Iterable[DocLink]:  # вернуть id документов, ссылающихся на этот документ
        for entry in self.__data:
            if entry.doc_to_id == doc_id:
                yield entry

    def add(self, doc_link) -> None:  # добавить ссылку
        self.__data.append(doc_link)


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


class PLRepo:
    def __init__(self) -> None:
        self.__data = []

    def get_all(self) -> Iterable[PL]:  # вернуть все posting list
        for entry in self.__data:
            yield entry

    def get_doc_id(self, doc_id) -> Iterable[PL]:  # вернуть все posting list, где есть ссылка на этот документ
        for entry in self.__data:
            if entry.doc_id == doc_id:
                yield entry

    def get_word_id(self, word_id) -> Iterable[PL]:  # вернуть все posting list, где есть ссылка на это слово
        for entry in self.__data:
            if entry.word_id == word_id:
                yield entry

    def get_both_id(self, word_id, doc_id) -> PL | None:  # вернуть posting list с этим словом и документом
        for entry in self.__data:
            if entry.word_id == word_id and entry.doc_id == doc_id:
                return entry

        return None

    def add(self, pl) -> None:  # добавить posting list
        self.__data.append(pl)

    def remove_zero(self) -> None:  # удалить все posting list, где кол-во слов равно 0
        new_data = []

        for entry in self.__data:
            if entry.count > 0:
                new_data.append(entry)

        self.__data = new_data


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

