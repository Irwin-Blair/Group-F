import numpy as np
import matplotlib.pyplot
import findiff

t = np.array([0,1,2,3,4,5])

def differentiation(t,n):
    dt = t[i]-t[i-1]
    dfdt = FinDiff(0,dt,n)
    return dfdt

for i in range(len(t)):
    print(differentiation(t,1))