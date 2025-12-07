from argparse import ArgumentParser


def main():
    default_dir = "sites/"

    parser = ArgumentParser()
    parser.add_argument("query", nargs='+', help="the search query, at least one word must be entered")
    parser.add_argument("-s", required=False, default=default_dir, help="the directory which contains the sites, by default it's the sites/ directory")
    parser.add_argument("--daat", required=False, action="store_true", help="use the document-at-a-time approach instead of the default term-at-a-time approach")
    parser.add_argument("--pregel", required=False, action="store_true", help="use the pregel library instead of the default MapReduce")

    args = parser.parse_args()



if __name__ == "__main__":
    main()
