from argparse import ArgumentParser

from repos import DocRepo, PLRepo, WordRepo, DocLinkRepo
from fill_repos import fill_repos


def main():
    default_urls = [
            "https://en.wikipedia.org/wiki/Python_(programming_language)",
            "https://www.python.org/",
            "https://en.wikipedia.org/wiki/High-level_programming_language",
            "https://en.wikipedia.org/wiki/Machine_learning",
            "https://github.com/python/pythondotorg/issues",
            "https://github.com/"
            ]

    parser = ArgumentParser()
    parser.add_argument("query", nargs='+', help="the search query, at least one word must be entered")
    parser.add_argument("--urls", nargs='*', default=default_urls, help="the urls to search from, the default urls are in the main.py file")
    parser.add_argument("--daat", required=False, action="store_true", help="use the document-at-a-time approach instead of the default term-at-a-time approach")
    parser.add_argument("--pregel", required=False, action="store_true", help="use the pregel library instead of the default MapReduce")
    args = parser.parse_args()

    doc_repo = DocRepo()
    word_repo = WordRepo()
    pl_repo = PLRepo()
    doc_link_repo = DocLinkRepo()

    fill_repos(doc_repo, word_repo, pl_repo, doc_link_repo, args.query, args.urls)  # заполняем наши репозитории

    print("\nDocs:")
    for doc in doc_repo.get_all():
        print(doc)

    print("\nWords:")
    for word in word_repo.get_all():
        print(word)

    print("\nPosting lists:")
    for pl in pl_repo.get_all():
        print(pl)

    print("\nDoc links:")
    for link in doc_link_repo.get_all():
        print(link)


if __name__ == "__main__":
    main()
