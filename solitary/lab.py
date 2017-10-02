import matplotlib.pyplot as plt
import numpy as np


g = 9.81  # Gravity
H = 0.3   # Height
d = 1.     # Depth

def eta(x, t):
    c = np.sqrt(g*d*(1+H/d))
    return d + H/(np.cosh(np.sqrt(3*H/4*d**3)*(x-c*t))**2)

print eta(-10, 0), eta(10, 0)

x = np.linspace(-10, 10, 10000)
plt.figure()
plt.plot(x, eta(x, 0))
plt.plot(x, eta(x, 0.2))
plt.show()
