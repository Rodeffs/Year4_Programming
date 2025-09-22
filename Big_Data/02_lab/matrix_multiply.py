def mapping(A, B):
    row_count_A, col_count_B = len(mat), len(mat[0])

    for row in range(row_count):
        for col in range(col_count):
            
            # Для левой матрицы ключом служит её номер строки, а значениями - номер колонки и элемент

            if order == "left":
                yield (row, ('A', col, mat[row][col]))

            # Для правой матрицы ключом служит её номер столбца, а значениями - номер строки и элемент

            else:
                yield (col, ('B', row, mat[row][col]))


def shuffling(mapped_A, mapped_B):
    


def main():
    A = [[6, 9],
         [11, 17]]
    B = [[8, 18],
         [22, 25]]

    mapped_A = list(mapping(A, "left"))
    mapped_B = list(mapping(B, "right"))

    

if __name__ == "__main__":
    main()
