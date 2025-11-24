def mapping(A, B):
    row_count_A, col_count_A = len(A), len(A[0])
    row_count_B, col_count_B = len(B), len(B[0])
    
    # Индексом будет строка и столбец получившейся матрицы C

    for row_A in range(row_count_A):
        for col_A in range(col_count_A):
            for col_B in range(col_count_B):
                yield ((row_A, col_B), (col_A, A[row_A][col_A]))

    for col_B in range(col_count_B):
        for row_B in range(row_count_B):
            for row_A in range(row_count_A):
                yield ((row_A, col_B), (row_B, B[row_B][col_B]))


def sorting(mapped):
    by_row = sorted(mapped, key=lambda x: x[0][0])

    prev_row = None
    same_row = []

    for coord, value in by_row:
        if coord[0] != prev_row:
            if prev_row is not None:
                for elem in sorted(same_row, key=lambda x: x[0][1]):
                    yield elem

                same_row = []

            prev_row = coord[0]

        same_row.append((coord, value))

    for elem in sorted(same_row, key=lambda x: x[0][1]):
        yield elem


def shuffling(sorted_list):
    prev_coord = (None, None)
    same_coord = []

    for coord, value in sorted_list:
        if coord[0] != prev_coord[0] or coord[1] != prev_coord[1]:
            if prev_coord[0] is not None and prev_coord[1] is not None:
                yield (prev_coord, sorted(same_coord, key=lambda x: x[0]))

                same_coord = []

            prev_coord = coord

        same_coord.append(value)

    yield (prev_coord, sorted(same_coord, key=lambda x: x[0]))


def reducing(shuffled_list):
    for coord, value in shuffled_list:
        elem = 0

        for i in range(0, len(value)-1, 2):
            elem += value[i][1]*value[i+1][1]

        yield(coord, elem)


def main():
    A = [[6, 9, 88],
         [11, 17, 105]]
    B = [[8, 18],
         [22, 25],
         [54, 79]
         ]

    mapped_list = list(mapping(A, B))
    sorted_list = list(sorting(mapped_list))
    shuffled_list = list(shuffling(sorted_list))
    C = list(reducing(shuffled_list))

    print(C)
    
    
if __name__ == "__main__":
    main()
