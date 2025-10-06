from random import uniform
from math import log
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


def create_png(points, filename, precision):
    mult = 10**precision  # точность, сколько знаков после запятой рассматривать

    x_max = max(points, key=lambda x: x[0])[0]
    x_min = min(points, key=lambda x: x[0])[0]

    y_max = max(points, key=lambda y: y[1])[1]
    y_min = min(points, key=lambda y: y[1])[1]

    dim_x = (x_max - x_min)*mult
    dim_y = (y_max - y_min)*mult
    
    dim = int(max(dim_x, dim_y))+1

    image_data = [[1 for i in range(dim)] for j in range(dim)]

    for point in points:
        x = int((point[0] - x_min)*mult)
        y = int((point[1] - y_min)*mult)

        image_data[y][x] = 0

    image = png.from_array(image_data, "L;1")  # L;1 - greyscale with bitdepth 1
    image.save(filename)

    return dim


def parse():
    parser = ArgumentParser()

    parser.add_argument("-x", required=True, type=int, help="the x coordinate for the root of fractal")
    parser.add_argument("-y", required=True, type=int, help="the y coordinate for the root of fractal")
    parser.add_argument("-p", required=True, type=int, help="the rounding of floating point")
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

    dim = create_png(points, f"{args.i}_iterations.png", args.p)

    print("Fractal size =", log(args.i) / log(dim))


if __name__ == "__main__":
    main()
