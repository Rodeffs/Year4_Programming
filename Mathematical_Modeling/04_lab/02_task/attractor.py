from random import uniform
from math import log, floor
from argparse import ArgumentParser
import png


def attractor(matrixes, vectors, x_target, y_target, iter_count):
    points = []

    x = x_target
    y = y_target

    proj_count = len(matrixes)

    for j in range(iter_count):
        i = int(uniform(0, proj_count))

        a, b, c, d = matrixes[i][0][0], matrixes[i][0][1], matrixes[i][1][0], matrixes[i][1][1]
        e, f = vectors[i][0], vectors[i][1]

        x_new = a*x + b*y + e
        y_new = c*x + d*y + f

        x = x_new
        y = y_new

        points.append((x, y))

    return points


def create_png(points, filename):
    x_max = max(points, key=lambda x: x[0])[0]
    x_min = min(points, key=lambda x: x[0])[0]

    y_max = max(points, key=lambda y: y[1])[1]
    y_min = min(points, key=lambda y: y[1])[1]

    dim_x = x_max - x_min
    dim_y = y_max - y_min

    # Т.к. координаты могут быть не целыми, а пиксели всегда должны быть целыми, то нужно округлить. Если координаты не целые, то домножим на 1000 и запишем в пиксели. Иначе - оставляем как есть
    
    mult = 1

    if min(dim_x, dim_y) < 1:
        mult = 1000

    dim = int(max(dim_x, dim_y)*mult)+1

    image_data = [[1 for i in range(dim)] for j in range(dim)]

    pixel_count = 0

    for point in points:
        x = int((point[0] - x_min)*mult)  # сдвиг нужен, чтобы не было отрицательных координат
        y = int((point[1] - y_min)*mult)

        if image_data[y][x] == 1:
            pixel_count += 1

        image_data[y][x] = 0

    image = png.from_array(image_data, "L;1")  # L;1 - greyscale with bitdepth 1
    image.save(filename)

    size = log(pixel_count) / log(dim)

    return size


def parse():
    parser = ArgumentParser()

    parser.add_argument("-x", required=True, type=int, help="the x coordinate for the root of fractal")
    parser.add_argument("-y", required=True, type=int, help="the y coordinate for the root of fractal")
    parser.add_argument("-i", required=True, type=int, help="the number of iterations")

    return parser.parse_args()


def main():
    matrixes = [
            [[0.223, 1.036],
             [0.744, -0.124]],

            [[-0.971, 0.052],
             [0.316, 0.504]],

            [[-0.340, -0.852],
             [-0.124, 0.856]]
            ]

    vectors = [
            [28.586, 49.567],

            [20.525, 29.918],

            [-49.663, -69.656]
            ]

    args = parse()

    points = attractor(matrixes, vectors, args.x, args.y, args.i)

    size = create_png(points, f"{args.i}_iterations.png")

    print("Fractal size =", size)


if __name__ == "__main__":
    main()
