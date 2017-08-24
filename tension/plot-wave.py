import numpy as np
import matplotlib.pyplot as plt


def plot_wave(paths):
    plt.figure()
    for path in paths:
        x, y = np.loadtxt(path).T
        plt.plot(x, y, label=path)
    plt.legend(loc='best')

    plt.show()

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    import sys

    sys.exit(plot_wave(sys.argv[1:]))
