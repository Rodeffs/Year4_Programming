import re
import multiprocessing
from time import time


def punctuation_expression():
    # Регулярное выражение для деления по знакам препинания

    punctuation = [r'\.', ',', ':', ';', r'\?', '!', r'\(', r'\)', r'\[', r'\]', r'\{', r'\}', r'\n', r'\*', r"(?<![A-Za-z0-9])-(?![A-Za-z0-9])", r"e\.g\.", r"i\.e\.", r"(?<![A-Za-z0-9])/(?![A-Za-z0-9])", r"(?<![A-Za-z0-9])'(?![A-Za-z0-9])"]

    punc_regexp = r"(?:"

    for i in range(len(punctuation)):
        punc_regexp += punctuation[i]

        if i != len(punctuation) - 1:
            punc_regexp += '|'

        else:
            punc_regexp += ')'

    return punc_regexp


def word_expression():
    # Регулярное выражения для деления по словам (эти слова не учитываются, т.к. они не несут смысловой нагрузки)

    ignored_words = ["a", "an", "the", "and", "or", "as", "of", "in", "on", "yet", "our", "than", "then", "however", "at", "but", "was", "were", "which", "there", "this", "that", "thus", "we", "to", "for", "is", "are", "where", "have", "has", "been", "since", "with", "such", "another", "also", "by", "often", "can", "could", "so", "from", "its", "via", "will", "hence", "should", "would", "shall", "what", "although", "these", "those", "do", "does", "did", "under", "above", "else", "if", "while", "when", "who", "based", "way", "very", "many", "much", "due", "because", "onto", "into", "out", "finally", "their", "they", "may", "might", "up", "down", "either", "neither", "nor", "within", "according", "others", "about", "therefore", "no", "not", "towards", "beyond", "behind", "over", "how", "both", "without", "other", "another", "more", "most", "moreover", "be", "furthermore", "why", "paper", "focuses", "well", "must", "consider", "using", "used", "commonly", "some", "given", "among", "able", "present", "his", "her", "he", "she", "obtained", "makes", "give", "make", "further", "use", "introduce", "employ", "uses", "show", "allows", "gives", "introduces", "considers", "through", "take", "takes", "enable", "enables", "allow", "every", "each", "called", "provide", "provides", "cannot", "allowing", "even", "though"]

    word_regexp = r"(?<![A-Za-z0-9_-])(?:"

    for i in range(len(ignored_words)):
        word_regexp += ignored_words[i]

        if i != len(ignored_words) - 1:
            word_regexp += '|'

        else:
            word_regexp += r")(?![A-Za-z0-9_-])"

    return word_regexp


punc_regexp = punctuation_expression()
word_regexp = word_expression()


def read_by_row(filepath, column_marker, column_separator, row_separator):
    with open(filepath, mode="r", encoding="utf-8") as f:
        row = ""
        column_started = False

        while True:
            char = f.read(1)  # читаем посимвольно, затем конкатенируем

            if not char:
                break

            if char == column_marker:  
                column_started = not column_started

            elif char == column_separator and not column_started:
                row += ". "

            elif char == row_separator and not column_started:
                yield row
                row = ""

            else:
                row += char

        yield row


def splitter(input_string):  # делим строку по словам, используя регулярное выражение
    string = input_string.lower()  # чтобы не нужно было следить за регистром

    sentances = re.split(punc_regexp, string)  # деление строки на подстроки по знакам препинания (без пробела)

    split_phrases = []

    for sentance in sentances:
        if sentance == '':
            continue

        split_sentance = re.split(word_regexp, sentance)

        # Удаляем пробелы в начале и в конце фраз и игнорируем пустые строки

        for i in range(len(split_sentance)):
            if len(split_sentance[i]) > 0 and split_sentance[i][0] == ' ':
                split_sentance[i] = split_sentance[i][1:]

            if len(split_sentance[i]) > 0 and split_sentance[i][-1] == ' ':
                split_sentance[i] = split_sentance[i][:-1]

            if len(split_sentance[i]) > 0:
                split_phrases.append(split_sentance[i])
        
    return split_phrases


def mapper(row):
    row_split = splitter(row)

    for entry in row_split:
        yield entry, 1


def shuffler(entries):
    buffer = []
    last_entry = None

    for entry, value in entries:
        if last_entry == entry or last_entry == None:
            buffer.append(value)

        else:
            yield last_entry, buffer
            buffer = [value]
            
        last_entry = entry

    yield last_entry, buffer


def reducer(entries):
    for entry, value in entries:
        yield entry, sum(value)


def worker(entry):
    mapped = sorted(list(mapper(entry)), key= lambda x: x[0])
    shuffled = list(shuffler(mapped))
    reduced = sorted(list(shuffled), key=lambda x: x[1], reverse=True)
    

def parallel(file_by_line):
    proc_count = multiprocessing.cpu_count()
    stop = False
    cur_row = 1

    while True:
        if stop:
            break

        processes = []

        for proc in range(proc_count):
            entry = next(file_by_line)

            if not entry:
                stop = True
                break

            print("Cur row =", cur_row, end="\r")

            processes.append(multiprocessing.Process(target=worker, args=([entry])))

        for proc in processes:
            proc.start()


        for proc in processes:
            proc.join()

        cur_row += 1


def main():
    # Dataset: https://www.kaggle.com/datasets/beta3logic/3m-academic-papers-titles-and-abstracts

    filepath = "/home/owner/Education/Work/Big_Data/cleaned_papers.csv"
    column_marker = '"'  # в данном датасете значения в столбцах выделены кавычками, потому всё, что в них, добавляем как есть
    column_separator = ','
    row_separator = '\n'

    # Выполнение алгоритма

    file_by_line = read_by_row(filepath, column_marker, column_separator, row_separator)

    next(file_by_line)  # пропускаем первую строку, т.к. в ней только название столбцов

    parallel(file_by_line)


if __name__ == "__main__":
    start_time = time()
    main()
    print("\nExecute time:", time() - start_time)
