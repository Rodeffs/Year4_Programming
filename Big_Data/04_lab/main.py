from argparse import ArgumentParser

from repos import DocRepo, PLRepo, WordRepo, DocLinkRepo
from fill_repos import fill_repos
from tf_idf import tf_idf
from page_rank import page_rank
from pregel import pregel
from result import result


default_urls = [
        "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "https://www.python.org/",
        "https://www.geeksforgeeks.org/courses",
        "https://github.com/python/pythondotorg/issues",
        "https://www.youtube.com/geeksforgeeksvideos",
        "https://github.com/",
        "https://archlinux.org/",
        "https://flathub.org/en",
        "https://kantiana.ru/",
        "https://vk.com/ikbfu"
        ]


def arguments():
    parser = ArgumentParser()
    parser.add_argument("query", nargs='+', help="the search query, at least one word must be entered")
    parser.add_argument("-d", required=False, type=float, default=0.85, help="the damping factor for PageRank algorithm, default value is 0.85")
    parser.add_argument("-c", required=False, type=int, default=20, help="the amount of cycles for PageRank algorithm, default value is 20")
    parser.add_argument("--urls", nargs='*', default=default_urls, help="the urls to search from, the default urls are in the main.py file")
    parser.add_argument("--daat", required=False, action="store_true", help="use the document-at-a-time approach instead of the default term-at-a-time approach")
    parser.add_argument("--pregel", required=False, action="store_true", help="use the pregel library instead of the default MapReduce")
    parser.add_argument("--logs", required=False, action="store_true", help="output the logs for bug fixes")
    args = parser.parse_args()

    if args.d > 1 or args.d < 0 or args.c < 0:
        raise ValueError("Error, damping factor must be within [0, 1] and cycle count must be a positive integer")

    return args


def main():
    args = arguments()
    doc_repo = DocRepo()
    word_repo = WordRepo()
    pl_repo = PLRepo()
    doc_link_repo = DocLinkRepo()


    fill_repos(doc_repo, word_repo, pl_repo, doc_link_repo, args.query, args.urls)  # заполняем наши репозитории


    tf_idf(doc_repo, word_repo, pl_repo, "daat" if args.daat else "taat")  # выполняем tf-idf


    if args.pregel:  # выполнение PageRank
        pregel(doc_repo, doc_link_repo, args.d, args.c)

    else:
        page_rank(doc_repo, doc_link_repo, args.d, args.c)


    search_result = result(doc_repo, pl_repo)  # финальный вывод


    if len(search_result) == 0:
        print("\nNo sites contait this query")

    else:
        print("\nBest results:\n")
        for link, value in search_result:
            print(link)
    

    if args.logs:  # если нужны логи для отладки
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
