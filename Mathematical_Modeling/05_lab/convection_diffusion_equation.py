import matplotlib.pyplot as plt
from math import ceil, log, exp, sqrt


def f(x, t):
    return 7.4


def V(x):
    return x+2


def Ut0(x):
    return max(0, (4-x)*(x-9))


def Ux0(t):
    return 1/200000*t*(t-20)**2


def U_1(x, t):  # решение, определяемое начальным условием
    y = (x+2)*exp(-t)
    return max(0, (6-y)*(y-11)) + 7.4*t


def U_2(x, t):  # решение, определяемое граничным условием
    y = log(2/(x+2))
    return 1/200000*(t+y)*(t+y-20)**2 - 7.4*y


def analytical(width, height, dx, dt):
    points = []

    for j in range(height+1):
        t = j*dt
        
        for i in range(width+1):
            x = i*dx
            U = 0

            # Находим первый интеграл и смотрим на его знак. Когда он положителен, решение определяется начальным условием, а когда он отрицателен - граничным

            first_intergal = x-2*exp(t)+2

            if t == 0:
                U = Ut0(x)

            elif x == 0:
                U = Ux0(t)

            elif first_intergal >= 0:
                U = U_1(x, t)

            else:
                U = U_2(x, t)

            points.append((t, x, U))

    return points

   
def lower_right(width, height, dx, dt):
    U = [[0 for w in range(width+1)] for h in range(height+1)]
    points = []

    for j in range(height+1):
        t = j*dt
        
        for i in range(width+1):
            x = i*dx

            if t == 0:
                U[j][i] = Ut0(x)

            elif x == 0:
                U[j][i] = Ux0(t)

            else:
                U[j][i] = U[j-1][i] + dt*(f(x, t) + V(x)/dx * (U[j-1][i-1] - U[j-1][i]))

            points.append((t, x, U[j][i]))

    return points


def upper_right(width, height, dx, dt):
    U = [[0 for w in range(width+1)] for h in range(height+1)]
    points = []

    for j in range(height+1):
        t = j*dt
        
        for i in range(width+1):
            x = i*dx

            if t == 0:
                U[j][i] = Ut0(x)

            elif x == 0:
                U[j][i] = Ux0(t)

            else:
                U[j][i] = dx/(dx + dt*V(x)) * (dt*f(x, t) + dt*V(x)/dx * U[j][i-1] + U[j-1][i])

            points.append((t, x, U[j][i]))

    return points


def dispersion(approx, exact):
    n = len(approx)
    square_sum = 0

    for i in range(n):
        square_sum += (approx[i][2]-exact[i][2])**2

    return sqrt(square_sum/n)


def plot3d(points):
    ax = plt.figure().add_subplot(projection="3d")
    
    X, Y, Z = [], [], []

    for point in points:
        X.append(point[1])
        Y.append(point[0])
        Z.append(point[2])

    ax.plot(X, Y, Z)
    ax.set_xlabel("x")
    ax.set_ylabel("t")
    ax.set_zlabel("U(x, t)")

    plt.show()


def main():
    # Предполагается, что x_min и t_min равны 0

    x_max, t_max = 10, 100

    print("Сколько шагов разностной схемы по x?")
    width = int(input())

    print("Какой график вывести? (1-4)\n1. Явный угол\n2. Неявный угол\n3. Аналитическое решение\n4. Значения в конкретных точках")
    select = input()

    dx = x_max/width

    # Шаг по времени определяем из условия устойчивости
    
    dt = dx/V(x_max)
    height = ceil(t_max/dt)

    sol1 = lower_right(width, height, dx, dt)
    sol2 = upper_right(width, height, dx, dt)
    sol3 = analytical(width, height, dx, dt)

    if select == "1":
        print("Среднеквадратичное отклонение", dispersion(sol1, sol3))
        plot3d(sol1)

    elif select == "2":
        print("Среднеквадратичное отклонение", dispersion(sol2, sol3))
        plot3d(sol2)

    elif select == "3":
        plot3d(sol3)

    elif select == "4":
        print("Введите значение t")
        T = int(input())

        begin = round(T/dt)
        
        ax = plt.figure().add_subplot()
    
        X = []
        Y1, Y2, Y3 = [], [], []

        for i in range(width+1):
            X.append(sol1[begin + i][1])
            Y1.append(sol1[begin + i][2])
            Y2.append(sol2[begin + i][2])
            Y3.append(sol3[begin + i][2])

        ax.scatter(X, Y1, color="r", label="Явный угол")
        ax.scatter(X, Y2, color="g", label="Неявный угол")
        ax.scatter(X, Y3, color="b", label="Аналитическое решение")

        ax.set_xlabel("x")
        ax.set_ylabel("U")
           
        plt.legend()
        plt.grid()
        plt.show()

    else:
        print("Такого графика нет!")


if __name__ == "__main__":
    main()
