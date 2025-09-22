def mapping(A, B):
    row_count_A, col_count_A = len(A), len(A[0])
    row_count_B, col_count_B = len(B), len(B[0])
    
    # Индексом будет строка и столбец получившейся матрицы C

    for row_A in range(row_count_A):
        for col_A in range(col_count_A):
            for col_B in range(col_count_B):
                yield ((row_A, col_B), ('A', col_A, A[row_A][col_A]))

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
