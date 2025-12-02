from time import time
import matplotlib.pyplot as plt
import numpy as np


def reader(filepath):
    with open(filepath, mode="r", encoding="utf-8") as f:
        while True:
            line = f.readline()

            if not line:
                break

            yield line


def mapper(filepath):
    for line in reader(filepath):
        x, y = line.split()
        yield float(x), float(y)


def reducer(points):
    N = 0
    sumX, sumY, sumXY, sumX2 = 0, 0, 0, 0

    for point in points:
        x, y = point
        sumX += x
        sumY += y
        sumXY += x*y
        sumX2 += x**2
        N += 1

        plt.scatter(x, y, color="k")

    b1 = (N*sumXY - sumX*sumY)/(N*sumX2 - sumX**2)
    b0 = (sumY - b1*sumX)/N

    X = np.arange(0, 20)

    plt.plot(X, b0*X + b1)

    plt.show()

    return b1, b0


def main():
    filepath = "xy.txt"

    b1, b0 = reducer(mapper(filepath))


if __name__ == "__main__":
    start_time = time()
    main()
    print("Execute time:", time() - start_time)
