import re
from time import time


def regular_expression():
    ignored_words = ["a", "an", "the", "and", "or", "as", "of", "in", "on", "yet", "our", "than", "then", "however", "at", "but", "was", "were", "which", "there", "this", "that", "thus", "we", "to", "for", "is", "are", "where", "have", "has", "been", "since", "with", "such", "another", "also", "by", "often", "can", "could", "so", "from", "its", "via", "will", "hence", "should", "would", "shall", "what", "although", "these", "those", "do", "does", "did", "under", "above", "else", "if", "while", "when", "who", "based", "way", "very", "many", "much", "due", "because", "onto", "into", "out", "finally", "their", "they", "may", "might", "up", "down", "either", "neither", "nor", "within", "according", "others", "about", "therefore", "no", "not", "towards", "beyond", "behind", "over", "how", "both", "without", "other", "another", "more", "most", "moreover", "be", "furthermore", "why", "paper", "focuses", "well", "must", "consider", "using", "used", "commonly", "some", "given", "among", "able", "present", "his", "her", "he", "she", "obtained", "makes", "give", "make", "further", "use", "introduce", "employ", "uses", "show", "allows", "gives", "introduces", "considers", "through", "take", "takes", "enable", "enables", "allow", "every", "each", "called", "provide", "provides", "cannot", "allowing", "even", "though", "after", "around", "upon", "you", "new"]

    regexp = r"([^a-z^\s^'^-])|(?:^|[^a-z])['-]|['-](?:^|[^a-z])|'*(?<![a-z-])(?:"

    for i in range(len(ignored_words)):
        regexp += ignored_words[i]

        if i != len(ignored_words) - 1:
            regexp += '|'

        else:
            regexp += ")(?![a-z-])'*"

    return regexp

regexp = regular_expression()


def mapper(line):
    word_combination = 2  # считаем за темы пары слов больше 2
    map_value = 1

    for combination in re.split(regexp, line):
        if combination is None:
            continue

        combination = combination.strip()

        if len(re.split(r"\s+", combination)) >= word_combination:
            yield combination, map_value


def shuffler(entries):
    sorted_entries = sorted(entries, key=lambda x: x[0])
    prev_comb = None
    buffer = []

    for combination, value in entries:
        if combination != prev_comb and prev_comb is not None:
            yield prev_comb, buffer
            buffer = []

        prev_comb = combination
        buffer.append(value)

    yield prev_comb, buffer


def reducer(entries):
    for combination, values in entries:
        yield combination, sum(values)


def reader(filepath):
    with open(filepath, mode="r", encoding="utf-8") as file:
        for line in file:
            yield line


def writer(filepath, entries):
    with open(filepath, mode="w", encoding="utf-8") as file:
        for combination, value in entries:
            line = combination + ": " + str(value) + "\n"
            file.write(line)


def map_reduce(filepath):
    mapped = []
    lines_done = 1

    print("Mapping")
    for line in reader(filepath):
        mapped += list(mapper(line))
        print("Processed line", lines_done, end="\r")
        lines_done += 1

    print("\nShuffling")
    shuffled = list(shuffler(mapped))

    print("Reducing")
    reduced = list(reducer(shuffled))

    print("Sorting")
    final_result = sorted(reduced, key=lambda x: x[1])

    return final_result


def main():
    # Dataset: https://www.kaggle.com/datasets/beta3logic/3m-academic-papers-titles-and-abstracts
    # Use splitter.py first, otherwise this dataset is awfully formatted

    filepath = "/home/owner/Downloads/Big_Data/dataset.txt"
    result = map_reduce(filepath)
    writer("output.txt", result)


if __name__ == "__main__":
    start_time = time()
    main()
    print("Execute time:", time() - start_time)
