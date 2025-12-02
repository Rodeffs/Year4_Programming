import re
import pandas as pd
from time import time


def main():
    df_input = "/home/owner/Downloads/Big_Data/cleaned_papers.csv"

    df = pd.read_csv(df_input)
    i, j = 0, 0
    max_lines = 10000
    file = open(f"/home/owner/Downloads/Big_Data/datasets/dataset{j}.txt", mode="w", encoding="utf-8")

    for row in df.itertuples(index=False):
        line = str(row.title + ". " + row.abstract).lower()  # объединить оба столбца и перевести в нижний регистр
        line = re.sub(r"\s*\n\s*", ' ', line)  # убрать переносы на след. строку
        file.write(line + "\n")
        i += 1

        if i == max_lines:
            file.close()
            i = 0
            j += 1

            print(f"Processed {max_lines*j} lines", end="\r")
            file = open(f"/home/owner/Downloads/Big_Data/datasets/dataset{j}.txt", mode="w", encoding="utf-8")

    file.close()


if __name__ == "__main__":
    start_time = time()
    main()
    print("\nExecute time:", time() - start_time)
