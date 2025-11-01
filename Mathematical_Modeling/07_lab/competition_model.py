import matplotlib.pyplot as plt
import numpy as np


def prey_growth(r, a, predator, prey):
    return r*prey - a*predator*prey


def predator_growth(f, q, a, predator, prey):
    return f*a*predator*prey - q*predator


def runge(r, f, q, a, predator_start, prey_start, t_count, t_max):
    dt = t_max/t_count

    t = np.arange(0, t_max+dt, dt)
    prey = np.zeros(t_count+1, dtype=float)
    predator = np.zeros(t_count+1, dtype=float)

    prey[0] = prey_start
    predator[0] = predator_start

    for i in range(1, t_count+1):
        k1 = prey_growth(r, a, predator[i-1], prey[i-1])*dt
        m1 = predator_growth(f, q, a, predator[i-1], prey[i-1])*dt

        k2 = prey_growth(r, a, predator[i-1] + k1/2, prey[i-1] + m1/2)*dt
        m2 = predator_growth(f, q, a, predator[i-1] + k1/2, prey[i-1] + m1/2)*dt

        k3 = prey_growth(r, a, predator[i-1] + k2/2, prey[i-1] + m2/2)*dt
        m3 = predator_growth(f, q, a, predator[i-1] + k2/2, prey[i-1] + m2/2)*dt

        k4 = prey_growth(r, a, predator[i-1] + k3, prey[i-1] + m3)*dt
        m4 = predator_growth(f, q, a, predator[i-1] + k3, prey[i-1] + m3)*dt

        prey[i] = prey[i-1] + (k1 + 2*k2 + 2*k3 + k4)/6
        predator[i] = predator[i-1] + (m1 + 2*m2 + 2*m3 + m4)/6

    return [t, prey, predator]


def plot(t, prey, predator):
    ax = plt.figure().add_subplot()
    
    ax.plot(t, prey, color="b", label="Жертвы")
    ax.plot(t, predator, color="r", label="Хищники")
    ax.set_xlabel("t")
    ax.set_ylabel("Число")

    ax.legend()
    ax.grid()
    plt.show()


def plot_phase(prey, predator, r, f, q, a, t_count):
    arrow_count = 10
    arrow_length = 2
    step = int(t_count/arrow_count)

    # Изоклины

    for i in range(0, t_count+step, step):
        for j in range(0, t_count+step, step):
            x, y = predator[j], prey[i]

            angle = np.arctan(predator_growth(f, q, a, x, y)/prey_growth(r, a, x, y))
            
            print(angle)

            dx = 0.5*arrow_length*np.cos(angle)
            dy = 0.5*arrow_length*np.sin(angle)

            x0 = x - dx
            y0 = y - dy
            x1 = x + dx
            y1 = y + dy

            plt.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="->", color="k", lw=2))

    plt.plot(predator, prey, color="g", label="Фазовая диаграмма")

    plt.scatter(0, 0, color="r", label="Особая точка 1")
    plt.scatter(r/a, q/(f*a), color="b", label="Особая точка 2")

    plt.xlabel("Число хищников")
    plt.ylabel("Число жертв")
    plt.legend()
    plt.show()


def main():
    r = 5
    a = 0.1
    q = 2
    prey_start = 100
    predator_start = 6

    t_max = 1
    t_count = 100

    print("Параметр f:")
    f = float(input())

    t, prey, predator = runge(r, f, q, a, predator_start, prey_start, t_count, t_max)

    print("Что вывести? (1-2)\n1). График зависимости\n2). Фазовую диаграмму")
    select = input()

    if select == "1":
        plot(t, prey, predator)

    elif select == "2":
        plot_phase(prey, predator, r, f, q, a, t_count)

    else:
        print("Нет такой опции")


if __name__ == "__main__":
    main()
