import matplotlib.pyplot as plt
import numpy as np
import os

uv = 6, 7
for root in ('xprof_', 'yprof_'):
    space = {'xprof_': 2, 'yprof_': 1}[root]
    files = [f for f in os.listdir('.') if root in f]

    for velocity in uv:
        plt.figure()
        for f in files:
            data = np.loadtxt(f)
            X = data[:, space]
            Y = data[:, velocity]

            plt.plot(X, Y, label=f, linestyle='none', marker='o')
        plt.legend(loc='best')
plt.show()
