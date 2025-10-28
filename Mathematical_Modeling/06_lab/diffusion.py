import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from math import log


def Ut0(x):
    return x*(10-x)**2


def Ux0(t):
    return 0


def Ux1(t):
    return 0


def D(x):
    return x+1


def f(x):
    return 11-x


def explicit_method(a, b, c, d, h, T):
    x = np.arange(a, b + h, h)
    t = np.arange(c, d + T, T)
    height, width = len(t), len(x)

    U = np.zeros((height, width))

    for j in range(height):
        for i in range(width):
            if i == 0:
                U[j][i] = Ux0(t[j])

            elif i == width - 1:
                U[j][i] = Ux1(t[j])

            elif j == 0:
                U[j][i] = Ut0(x[i])

            else:
                l = D(x[i])*T/(h**2)
                U[j][i] = (l*U[j-1][i+1] + (1-2*l)*U[j-1][i] + l*U[j-1][i-1] + 5*T) / (1+T*f(x[i]))

    return [x, t, U]


def implicit_method(a, b, c, d, h, T):
    x = np.arange(a, b + h, h)
    t = np.arange(c, d + T, T)
    height, width = len(t), len(x)

    U = np.zeros((height, width))

    for j in range(height):  # граничные условия
        U[j][0] = Ux0(t[j])
        U[j][width-1] = Ux1(t[j])

    for i in range(1, width-1):  # начальные условия
        U[0][i] = Ut0(x[i])

    # Далее метод прогонки

    for j in range(1, height):
        # Сначала находим прогоночные коэф. альфа и бета

        alpha = np.zeros(width-1)
        beta = np.zeros(width-1)
        beta[0] = U[j][0]  # ВАЖНО! Иначе всё неправильно

        for i in range(1, width-1):
            l = D(x[i])*T/(h**2)

            A = l
            B = -1 - 2*l - f(x[i])*T
            C = l
            F = -U[j-1][i] - 5*T

            alpha[i] = -A / (C*alpha[i-1] + B)
            beta[i] = (F - C*beta[i-1]) / (C*alpha[i-1] + B)

        # Потом, начиная с конца, находим все значения U[j][i]

        for i in range(width-2, 0, -1):
            U[j][i] = alpha[i]*U[j][i+1] + beta[i]

    return [x, t, U]

   
def plot3d(points):
    ax = plt.figure().add_subplot(projection="3d")
    X, T = np.meshgrid(points[0], points[1])
    
    ax.plot_surface(X, T, points[2], cmap=cm.magma)
    ax.set_xlabel("x")
    ax.set_ylabel("t")
    ax.set_zlabel("U(x, t)")

    plt.show()


def experiment(x_min, x_max, t_min, t_max, h, T, method): # численный эксперимент для проверки аппроксимации
    U1 = method(x_min, x_max, t_min, t_max, h, T)[2]
    U2 = method(x_min, x_max, t_min, t_max, h, T/2)[2]
    U3 = method(x_min, x_max, t_min, t_max, h, T/4)[2]

    U4 = method(x_min, x_max, t_min, t_max, h, T/16)[2]
    U5 = method(x_min, x_max, t_min, t_max, h/2, T/16)[2]
    U6 = method(x_min, x_max, t_min, t_max, h/4, T/16)[2]

    print("Фиксированный момент времени t:")
    t_fixed = int(input())

    print("Фиксированная координата x:")
    x_fixed = int(input())

    x, t, val1, val2, val3, val4, val5, val6 = [], [], [], [], [], [], [], []
    max_diff_T1, max_diff_T2, max_diff_h1, max_diff_h2 = 0, 0, 0, 0

    width = int((x_max - x_min)/h)
    height = int((t_max - t_min)/T)

    for j in range(height+1):
        for i in range(width+1):
            max_diff_T1 = max(abs(U1[j][i]-U2[2*j][i]), max_diff_T1)
            max_diff_T2 = max(abs(U2[2*j][i]-U3[4*j][i]), max_diff_T2)
            max_diff_h1 = max(abs(U4[16*j][i]-U5[16*j][2*i]), max_diff_h1)
            max_diff_h2 = max(abs(U5[16*j][2*i]-U6[16*j][4*i]), max_diff_h2)

            if i == int((x_fixed-x_min)/h):
                t.append(t_min+j*T)
                val1.append(U1[j][i])
                val2.append(U2[2*j][i])
                val3.append(U3[4*j][i])

            if j == int((t_fixed-t_min)/T):
                x.append(x_min+i*h)
                val4.append(U4[16*j][i])
                val5.append(U5[16*j][2*i])
                val6.append(U6[16*j][4*i])
        
    approx_T = log(max_diff_T1/max_diff_T2)/log(2)
    approx_h = log(max_diff_h1/max_diff_h2)/log(2)

    fig, axs = plt.subplots(1, 2)

    axs[0].plot(t, val1, color="r", label="Разбиение T", marker=".")
    axs[0].plot(t, val2, color="g", label="Разбиение T/2", marker=".")
    axs[0].plot(t, val3, color="b", label="Разбиение T/4", marker=".")
    axs[0].legend()
    axs[0].set_xlabel("t")
    axs[0].set_ylabel("U")
    axs[0].set_title(f"Порядок аппроксимации для T = {approx_T}")
    axs[0].grid()

    axs[1].plot(x, val4, color="m", label="Разбиение h", marker=".")
    axs[1].plot(x, val5, color="y", label="Разбиение h/2", marker=".")
    axs[1].plot(x, val6, color="c", label="Разбиение h/4", marker=".")
    axs[1].legend()
    axs[1].set_xlabel("x")
    axs[1].set_ylabel("U")
    axs[1].set_title(f"Порядок аппроксимации для h = {approx_h}")
    axs[1].grid()

    print("Порядок аппроксимации для T:", approx_T)
    print("Порядок аппроксимации для h:", approx_h)

    plt.show()


def main():
    x_min, x_max = 0, 10
    t_min, t_max = 0, 1

    print("Количество разбиений по x:")
    width = int(input())

    h = (x_max - x_min)/width
    T = h**2 / (22 - 0.5*h**2)  # из условия устойчивости

    print("Что вывести? (1-4)\n1). Явный метод\n2). Неявный метод\n3). Проверка аппроксимации явного метода\n4). Проверка аппроксимации неявного метода")
    select = input()

    if select == "1":
        plot3d(explicit_method(x_min, x_max, t_min, t_max, h, T))

    elif select == "2":
        plot3d(implicit_method(x_min, x_max, t_min, t_max, h, T))

    elif select == "3":
        experiment(x_min, x_max, t_min, t_max, h, T, explicit_method)

    elif select == "4":
        experiment(x_min, x_max, t_min, t_max, h, T, implicit_method)

    else:
        print("Нет такой опции")


if __name__ == "__main__":
    main()
