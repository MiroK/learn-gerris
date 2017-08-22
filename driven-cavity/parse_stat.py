import matplotlib.pyplot as plt
import numpy as np
import sys
import re

number = re.compile(r'[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?')

data = [map(float, number.findall(line)) for line in open(sys.argv[1], 'r')]
data = np.array(data).T

t, norm1, norm2, normInf = data

plt.figure()
plt.semilogy(t, norm1, label='$|\delta u|_1$')
plt.semilogy(t, norm2, label='$|\delta u|_2$')
plt.semilogy(t, normInf, label='$|\delta u|_{\infty}$')
plt.legend(loc='best')

plt.show()

