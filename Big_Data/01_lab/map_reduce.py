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


def mapper(filepath):
    filename = filepath.split("/")[-1]

    word_combination = 2  # считаем за темы пары слов больше 2
    map_value = 1
    
    print(filename, "MAP START")

    with open(filepath, mode="r", encoding="utf-8") as input_file, open(output_dir + filename, mode="w", encoding="utf-8") as output_file:
        for line in input_file:
            for combination in regexp.split(line):
                if combination is None:
                    continue

                combination = combination.strip()

                if len(wordexp.split(combination)) >= word_combination:
                    output_file.write(combination + ';' + str(map_value) + '\n')  # чтобы не хранить всё это в оперативной памяти

    print(filename, "MAP END")


def reducer(values):
    prev_entry = None
    buffer = 0
    result = SortedList()

    while True:
        entry, value = values.pop()  # чтобы не забивать лишнюю память

        if entry != prev_entry and prev_entry is not None:
            result.add((prev_entry, buffer))
            buffer = 0

        prev_entry = entry
        buffer += value

        if len(values) == 0:
            result.add((prev_entry, buffer))
            return result


def map_reduce():
    result = SortedList()

    # Parallel mapping

    input_files = [os.path.join(input_dir, file) for file in os.listdir(input_dir)]

    with ThreadPoolExecutor() as pool:
        pool.map(mapper, input_files)

    # Sequential reducing (VERY SLOW, NEED OPTIMISATION)

    output_files = [os.path.join(output_dir, file) for file in os.listdir(output_dir)]
    i = 0

    for filepath in output_files:
        i += 1
        print(f"REDUCING {i} OUT OF {len(output_files)}", end='\r')

        with open(filepath, mode="r", encoding="utf-8") as file:
            for line in file:
                entry, value = line.split(';')
                result.add((entry, int(value)))

        result = reducer(result)

    result = reducer(result)

    # Sorting

    print()
    final_result = SortedList()
    i = 1
    N = len(result)
    
    while True:
        entry, value = result.pop()
        print(f"SORTING {i} OUT OF {N}", end='\r')
        final_result.add((-value, entry))  # минус нужен, чтобы сортировалось в обратном порядке
        i += 1

        if len(result) == 0:
            break

    # Writing

    print()
    i = 1
    N = len(final_result)

    with open(output_dir + "final_result.txt", mode="w", encoding="utf-8") as file:
        while True:
            value, entry = final_result.pop()
            print(f"WRITING {i} OUT OF {N}", end='\r')
            file.write(entry + ";" + str(-value) + '\n')
            i += 1

            if len(final_result) == 0:
                break


def main():
    # Dataset: https://www.kaggle.com/datasets/beta3logic/3m-academic-papers-titles-and-abstracts
    # Use splitter.py first to split the dataset into smaller datasets for parallel mapping

    map_reduce()


if __name__ == "__main__":
    start_time = time()
    main()
    print("\nExecute time:", time() - start_time)
