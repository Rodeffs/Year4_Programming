def reader(filepath):
    with open(filepath, mode="r", encoding="utf-8") as f:
        while True:
            line = f.readline()

            if not line:
                break

            yield line


def writer(filepath, mat):
    with open(filepath, mode="w", encoding="utf-8") as f:
        row = ""
        prev_row = None

        for elem in mat:
            if prev_row != elem[0] and prev_row is not None:
                row += "\n"
                f.write(row)
                row = str(elem[2]) + " "

            else:
                row += str(elem[2]) + " "

            prev_row = elem[0]

        row += "\n"
        f.write(row)


def mapper(filepath):
    row = 1

    for line in reader(filepath):
        col = 1

        for value in line.split():
            yield row, col, float(value)
            col += 1

        row += 1


def shuffler(mat, mat_type):
    if mat_type == "left":
        return sorted(mat, key=lambda x: (x[0], x[1])) 

    elif mat_type == "right":
        return sorted(mat, key=lambda x: (x[1], x[0]))

    else:
        return mat


def reducer(mat1, mat2):
    left_total_rows = mat1[-1][0]
    left_total_cols = mat1[-1][1]

    right_total_rows = mat2[-1][0]
    right_total_cols = mat2[-1][1]

    if left_total_cols != right_total_rows:
        raise ValueError("The amount of columns in the left matrix doesn't match the amount of rows in the right matrix")
    
    result_val = 0
    i, j = 0, 0

    while True:
        left_row = mat1[i][0]
        left_col = mat1[i][1]
        left_val = mat1[i][2]
        
        right_row = mat2[j][0]
        right_col = mat2[j][1]
        right_val = mat2[j][2]

        result_val += left_val * right_val

        if left_col == left_total_cols:
            if right_col < right_total_cols:
                i -= (left_total_cols - 1)
                j += 1

            else:
                i += 1
                j = 0

            yield left_row, right_col, result_val
            result_val = 0

            if left_row == left_total_rows and right_col == right_total_cols:
                break

        else:
            i += 1
            j += 1


def main():
    filepath1 = "mat1.txt"
    filepath2 = "mat2.txt"
    filepath3 = "result.txt"

    mat1 = list(mapper(filepath1))
    mat2 = list(mapper(filepath2))

    mat1 = shuffler(mat1, "left")
    mat2 = shuffler(mat2, "right")

    mat_result = list(reducer(mat1, mat2))
    writer(filepath3, mat_result)


if __name__ == "__main__":
    main()
