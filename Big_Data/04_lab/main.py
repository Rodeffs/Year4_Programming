from argparse import ArgumentParser

from repos import DocRepo, PLRepo, WordRepo, DocLinkRepo
from fill_repos import fill_repos


def main():
    default_urls = []

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

    fill_repos(doc_repo, word_repo, pl_repo, doc_link_repo, args.query, args.urls)

    print("Repos are now filled")


if __name__ == "__main__":
    main()
