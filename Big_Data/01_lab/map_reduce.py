import re
import pandas as pd
from time import time
from concurrent.futures import ThreadPoolExecutor


def word_expression():  # регулярное выражения для деления по словам (эти слова не учитываются, т.к. они не несут смысловой нагрузки)
    ignored_words = ["'", "our", "than", "then", "however", "but", "was", "were", "which", "there", "this", "that", "thus", "we", "is", "where", "have", "has", "been", "since", "such", "another", "also", "often", "can", "could", "its", "via", "will", "hence", "should", "would", "shall", "what", "although", "these", "those", "do", "does", "did", "else", "if", "while", "when", "who", "due", "because", "finally", "their", "they", "either", "neither", "nor", "according", "therefore", "how", "both", "moreover", "furthermore", "why", "consider", "his", "her", "he", "she", "further", "introduce", "employ", "introduces", "considers", "enable", "enables", "allow", "called", "provide", "provides", "cannot", "allowing", "though"]

    word_regexp = r"(?<![a-z-])(?:"

    for i in range(len(ignored_words)):
        word_regexp += ignored_words[i]

        if i != len(ignored_words) - 1:
            word_regexp += '|'

        else:
            word_regexp += r")(?![a-z-])"

    return word_regexp


punc_regexp = r"([^a-z^-^\s^'])"
word_regexp = word_expression()

df_entry = "phrase"
df_value = "value"


def mapper(df):
    entries, values = [], []
    map_value = 1

    # Сначала делим строку на подстроки по знакам препинания

    sentances = []

    for index, row in df.iterrows():
        line = row.iloc[0].lower()  # lower нужен, чтобы не обращать внимания на регистр
        line = re.sub(r"\s*\n\s*", ' ', line)  # убрать переносы на след. строку

        sentances += re.split(punc_regexp, line)  

    # Потом эти подстроки ещё раз делим, но теперь уже по игнорируемым словам

    phrases = []

    for sentance in sentances:
        phrases += re.split(word_regexp, sentance)
    
    # Удаляем пробелы в начале и в конце фраз и игнорируем пустые строки

    for phrase in phrases:
        phrase = phrase.strip()

        if len(re.split(r"\s+", phrase)) > 1:  # считаем за темы пары слов больше 2
            entries.append(phrase)
            values.append(map_value)

    return pd.DataFrame({df_entry: entries, df_value: values})


def reducer(df):
    return df.groupby([df_entry], as_index=False).sum()


def reader(filepath, chunksize):
    with pd.read_csv(filepath, chunksize=chunksize) as chunks:  # читаем файл по несколько строчек за раз, чтобы не хранить всё в памяти
        for chunk in chunks:
            yield chunk


def worker(df):
    return reducer(mapper(df))


def map_reduce(filepath, chunksize, processes):
    final_result = pd.DataFrame({df_entry: pd.Series(dtype="str"), df_value: pd.Series(dtype="int")})

    chunks_done = 0

    with ThreadPoolExecutor(max_workers=processes) as executor:
        for chunk in reader(filepath, chunksize):
            print("Chunks processed =", chunks_done, end="\r")
            chunk_result = executor.submit(worker, chunk).result()
            final_result = pd.concat([final_result, chunk_result], ignore_index=True)
            chunks_done += chunksize

    return reducer(final_result).sort_values(by=[df_value], ascending=False)


def main():
    # Dataset: https://www.kaggle.com/datasets/beta3logic/3m-academic-papers-titles-and-abstracts

    filepath = "/home/owner/Education/Work/Big_Data/cleaned_papers.csv"
    result = map_reduce(filepath, 1000, 16)
    result.to_csv("output.csv", sep=";", index=False)


if __name__ == "__main__":
    start_time = time()
    main()
    print("\nExecute time:", time() - start_time)
