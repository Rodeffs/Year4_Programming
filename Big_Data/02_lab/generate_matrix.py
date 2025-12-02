from random import uniform
from time import time
from argparse import ArgumentParser


def writer(filepath, width, height, minval, maxval):
    with open(filepath, mode="w", encoding="utf-8") as f:
        row = ""
        i = 1
        maximum = width*height

        for y in range(height):
            for x in range(width):
                print(f"Generating value {i} out of {maximum}", end="\r")

                row += str(round(uniform(minval, maxval), 2))
                i += 1

                if x != width - 1:
                    row += " "

            f.write(row + "\n")
            row = ""

def main():
    parser = ArgumentParser()

    parser.add_argument("-x", required=True, type=int, help="the width of the matrix")
    parser.add_argument("-y", required=True, type=int, help="the height of the matrix")
    parser.add_argument("-a", required=True, type=float, help="the minimum random value")
    parser.add_argument("-b", required=True, type=float, help="the maximum random value")
    parser.add_argument("-o", required=True, help="the output file")

    args = parser.parse_args()
    writer(args.o, args.x, args.y, args.a, args.b)


if __name__ == "__main__":
    start_time = time()
    main()
    print("\nExecute time:", time() - start_time)
