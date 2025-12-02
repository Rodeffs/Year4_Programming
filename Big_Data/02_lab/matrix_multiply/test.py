import numpy as np


def reader(filepath):
    with open(filepath, mode="r", encoding="utf-8") as f:
        while True:
            line = f.readline()

            if not line:
                break

            yield line


def mapper(filepath):
    mat = []

    for line in reader(filepath):
        row = []

        for value in line.split():
            row.append(float(value))

        mat.append(row)

    return np.array(mat)


def main():
    filepath1 = "mat1.txt"
    filepath2 = "mat2.txt"

    mat1 = mapper(filepath1)
    mat2 = mapper(filepath2)

    print(mat1@mat2)


if __name__ == "__main__":
    main()
