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


def plot(t, prey, predator, r, f, q, a):
    fig, axs = plt.subplots(1, 2)

    # Число хищников и жертв в зависимости от времени
    
    axs[0].plot(t, prey, color="b", label="Жертвы")
    axs[0].plot(t, predator, color="r", label="Хищники")
    axs[0].set_xlabel("t")
    axs[0].set_ylabel("Число")

    axs[0].legend(loc="upper right")
    axs[0].grid()

    x_min, x_max = np.min(predator), np.max(predator)
    y_min, y_max = np.min(prey), np.max(prey)

    X = np.linspace(0, x_max)
    Y = np.linspace(0, y_max)

    X, Y = np.meshgrid(X, Y)

    U = predator_growth(f, q, a, X, Y)
    V = prey_growth(r, a, X, Y)

    # Направления на траекториях

    axs[1].streamplot(X, Y, U, V, color="b")
    
    # Изоклины и особые точки

    critical = [(0, 0), (r/a, q/(f*a))]

    axs[1].plot((0, x_max), (critical[0][1], critical[0][1]), color="k")
    axs[1].plot((critical[0][0], critical[0][0]), (0, y_max), color="k")
    axs[1].plot((0, x_max), (critical[1][1], critical[1][1]), color="k")
    axs[1].plot((critical[1][0], critical[1][0]), (0, y_max), color="k")

    axs[1].scatter(critical[0][0], critical[0][1], color="r")
    axs[1].scatter(critical[1][0], critical[1][1], color="r")

    # Фазовая диаграмма

    axs[1].plot(predator, prey, color="g", label="Фазовая диаграмма", lw=3)

    axs[1].set_xlabel("Число хищников")
    axs[1].set_ylabel("Число жертв")
    axs[1].legend(loc="upper right")

    plt.show()


def main():
    r = 5
    a = 0.1
    q = 2
    prey_start = 100
    predator_start = 6

    t_max = 1
    t_count = 1000

    print("Параметр f:")
    f = float(input())

    t, prey, predator = runge(r, f, q, a, predator_start, prey_start, t_count, t_max)

    plot(t, prey, predator, r, f, q, a)


if __name__ == "__main__":
    main()
