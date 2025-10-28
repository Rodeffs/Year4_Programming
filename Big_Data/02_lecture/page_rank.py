from typing import Iterator

from fakes import FakeDocumentRepository, FakeDocumentLinkRepository

n_rolls = 50

document_repo = FakeDocumentRepository()
document_link_repo = FakeDocumentLinkRepository()

def roll() -> None:
    for doc in document_repo.get_all():
        all_links = document_link_repo.get_docs_to(doc.id)
        weight = doc.weight
        
        for doc_id, rank in mapper(doc.id, (weight, all_links)):
            ...


def mapper(doc_id, data) -> Iterator[int, float]:
    rank, ids = data

    yield doc_id, 0

    if len(ids) > 0:
        for i in ids:
            yield i, rank / len(ids)

    else:
        all_docs = document_repo.get_all()

        for cur_doc in all_docs:
            yield cur_doc.id, rank / len(all_docs)


def reducer(doc_id, ranks):
    all_docs = document_repo.get_all()
    value = (1 - alpha) * sum(ranks) + alpha / len(all_docs)

    return doc_id, value


def main():
    for i in range(n_rolls):
        roll()


if __name__ == "__main__":
    main()
