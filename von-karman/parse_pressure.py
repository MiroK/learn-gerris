import matplotlib.pyplot as plt
import numpy as np

front = np.loadtxt('probeFRONT.dat').T
t_f, p_f, pmac_f = front[[0, 4, 5]]

back = np.loadtxt('probeBACK.dat').T
t_b, p_b, pmac_b = back[[0, 4, 5]]

assert np.linalg.norm(t_f - t_b) < 1E-10

t = t_f
dp = p_f - p_b
dpmac = pmac_f - pmac_b

plt.figure()
plt.plot(t, dp, label='P')
plt.plot(t, dpmac, label='PMAC')
plt.legend(loc='best')
plt.show()
