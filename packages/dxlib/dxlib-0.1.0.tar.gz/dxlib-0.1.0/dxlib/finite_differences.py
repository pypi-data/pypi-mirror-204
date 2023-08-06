import numpy as np
import matplotlib.pyplot as plt


def finite_differences(x, y, delta=0.05):
    range_x = x[:-1]
    finite_difference = np.diff(y) / delta

    plt.plot(range_x, finite_difference, '--', label='Approximation')
    plt.legend()
    plt.show()

    return finite_difference

