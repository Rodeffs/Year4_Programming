import random

def generate_regression_data(filename, num_points = 20, k = 2.0, b = 5.0):
    with open(filename, 'w') as f:
        for i in range(num_points):
            x = round(random.uniform(0, num_points), 2)
            noise = random.uniform(-num_points/2, num_points/2)
            y = round(k * x + b + noise, 2)
            f.write(f"{x} {y}\n")

def main():
    filename = "xy.txt"
    generate_regression_data(filename)


if __name__ == "__main__":
    main()
