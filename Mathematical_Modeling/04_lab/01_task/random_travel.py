from random import uniform
from math import log
from argparse import ArgumentParser
import png
from time import time


def random_travel(width, height, x_target, y_target, iter_count):
    plane = [[1 for x in range(width)] for y in range(height)]
    plane[y_target][x_target] = 0

    x_max = width-1
    y_max = height-1

    i = 0

    while i < iter_count:
        print(f"Iteration {i+1}/{iter_count}", end="\r")

        x = int(uniform(0, x_max))
        y = int(uniform(0, y_max))

        if plane[y][x] == 0:
            continue

        freeze = False

        while True:
            if (x < x_max):
                freeze = (plane[y][x+1] == 0)
            
            if (not freeze) and (x > 0):
                freeze = (plane[y][x-1] == 0)

            if (not freeze) and (y < y_max):
                freeze = (plane[y+1][x] == 0)

            if (not freeze) and (y > 0):
                freeze = (plane[y-1][x] == 0)

            if (not freeze) and (x < x_max) and (y < y_max):
                freeze = (plane[y+1][x+1] == 0)

            if (not freeze) and (x < x_max) and (y > 0):
                freeze = (plane[y-1][x+1] == 0)

            if (not freeze) and (x > 0) and (y < y_max):
                freeze = (plane[y+1][x-1] == 0)

            if (not freeze) and (x > 0) and (y > 0):
                freeze = (plane[y-1][x-1] == 0)

            if freeze:
                plane[y][x] = 0
                i += 1
                break

            else:
                movement = uniform(0, 1)

                if movement < 1/6:
                    if y > 0:
                        y -= 1

                    else:
                        y += 1

                elif 1/6 <= movement < 2/6:
                    if y < y_max:
                        y += 1

                    else:
                        y -= 1

                elif 2/6 <= movement < 4/6:
                    if x > 0:
                        x -= 1

                    else:
                        x += 1

                else:
                    if x < x_max:
                        x += 1

                    else:
                        x -= 1
    return plane


def parse():
    parser = ArgumentParser()

    parser.add_argument("-d", required=True, type=int, help="the dimensions of the image, both height and width")
    parser.add_argument("-x", required=True, type=int, help="the x coordinate for the root of fractal")
    parser.add_argument("-y", required=True, type=int, help="the y coordinate for the root of fractal")
    parser.add_argument("-i", required=True, type=int, help="the number of iterations")
    parser.add_argument("-s", action="store_true", help="if used will just calculate the fractal size without generating an image")

    return parser.parse_args()


def main():
    args = parse()

    fractal_size = log(args.i) / log(args.d) # фрактальная размерность по методу коробок, числитель - сколько пикселей покрывает фрактал, знаменатель - обратная величина размера пикселя относительно всего изображения
    print("Fractal size =", fractal_size)

    if args.s:
        return

    start = time()

    fractal = random_travel(args.d, args.d, args.x, args.y, args.i)
    print("\nExecution time:", time()-start)

    image = png.from_array(fractal, "L;1")  # L;1 - greyscale with bitdepth 1
    image.save(f"{args.d}x{args.d}_{args.i}.png")


if __name__ == "__main__":
    main()
