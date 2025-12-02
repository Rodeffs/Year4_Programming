import re
import os
from sortedcontainers import SortedList  # чтобы в массив сразу вставлять отсортированно
from concurrent.futures import ThreadPoolExecutor  # для многопоточности
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


regexp = re.compile(regular_expression())  # прекомпиляция регулярного выражения для ускорения
wordexp = re.compile(r"\s+")
input_dir = "/home/owner/Downloads/Big_Data/datasets/"
output_dir = "/home/owner/Downloads/Big_Data/output/"
final_filepath = "/home/owner/Downloads/Big_Data/final_stats.txt"


def mapper(filepath):
    word_combination = 2  # считаем за темы пары слов больше 2
    map_value = 1
    mapped = SortedList()

    with open(filepath, mode="r", encoding="utf-8") as file:
        for line in file:
            for combination in regexp.split(line):
                if combination is None:
                    continue

                combination = combination.strip()

                if len(wordexp.split(combination)) >= word_combination:
                    mapped.add((combination, map_value))

    return mapped


def reducer(entries):
    prev_comb = None
    buffer = 0

    for combination, value in entries:
        if combination != prev_comb and prev_comb is not None:
            yield prev_comb, buffer
            buffer = 0

        prev_comb = combination
        buffer += value

    yield prev_comb, buffer


def writer(filepath, entries):
    with open(filepath, mode="w", encoding="utf-8") as file:
        for combination, value in entries:
            line = str(combination) + ";" + str(value) + "\n"
            file.write(line)


def worker(filepath):
    filename = filepath.split("/")[-1]

    print(filename, "MAP START")
    entries = mapper(filepath)

    print(filename, "MAP DONE, REDUCE START")
    writer(output_dir + filename, reducer(entries))  # записываем в файлы, чтобы не хранить в памяти

    print(filename, "REDUCE DONE")
     

def map_reduce():
    files = [os.path.join(input_dir, file) for file in os.listdir(input_dir)]

    with ThreadPoolExecutor(max_workers=16) as pool:  # разпараллеливаем
        pool.map(worker, files)

#    files = [os.path.join(output_dir, file) for file in os.listdir(output_dir)]

#    writer(result)


def main():
    # Dataset: https://www.kaggle.com/datasets/beta3logic/3m-academic-papers-titles-and-abstracts
    # Use splitter.py first to split the dataset into smaller datasets for parallel mapping

    map_reduce()


if __name__ == "__main__":
    start_time = time()
    main()
    print("Execute time:", time() - start_time)
