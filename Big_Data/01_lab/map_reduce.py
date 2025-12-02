import re
import pandas as pd
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
df_entry = "phrase"
df_value = "value"


def mapper(df):
    entries, values = [], []
    word_combination = 2  # считаем за темы пары слов больше 2
    map_value = 1

    for index, row in df.iterrows():
        line = re.sub(r"\s*\n\s*", ' ', row.iloc[0].lower())  # убрать переносы на след. строку, а lower() преобразует всё в нижний регистр

        for combination in re.split(regexp, line):
            if combination is None:
                continue

            combination = combination.strip()

            if len(re.split(r"\s+", combination)) >= word_combination:
                entries.append(combination)
                values.append(map_value)

    return pd.DataFrame({df_entry: entries, df_value: values})


def reducer(df):
    return df.groupby([df_entry], as_index=False).sum()


def reader(filepath, chunksize):
    with pd.read_csv(filepath, chunksize=chunksize) as chunks:  # читаем файл по несколько строчек за раз, чтобы не хранить всё в памяти
        for chunk in chunks:
            yield chunk


def map_reduce(filepath, chunksize):
    final_result = pd.DataFrame({df_entry: pd.Series(dtype="str"), df_value: pd.Series(dtype="int")})

    chunks_done = 0

    for chunk in reader(filepath, chunksize):
        print("Chunks processed =", chunks_done, end="\r")
        chunk_result = mapper(chunk)
        final_result = pd.concat([final_result, chunk_result], ignore_index=True)
        chunks_done += chunksize

    print("\nMapping done, reducing...")

    return reducer(final_result).sort_values(by=[df_value], ascending=False)


def main():
    # Dataset: https://www.kaggle.com/datasets/beta3logic/3m-academic-papers-titles-and-abstracts

    filepath = "/home/owner/Downloads/Big_Data/cleaned_papers.csv"
    result = map_reduce(filepath, 10000)
    result.to_csv("output.csv", sep=";", index=False)


if __name__ == "__main__":
    start_time = time()
    main()
    print("Execute time:", time() - start_time)
