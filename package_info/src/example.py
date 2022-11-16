import numpy as np
from scipy.sparse.linalg import inv, eigs
from scipy.sparse import csc_matrix, eye, diags
import matplotlib.pyplot as plt
from findiff import FinDiff

#setting up a grid
x = np.linspace(-5,5,100)
t = np.linspace(0,5,100)
dt = t[1] - t[0]



#using Hamiltonian to create matrix
H = -0.5 * FinDiff(0, x[1] - x[0], 2).matrix(x.shape) + diags(0.5*x**2)

H[0, :] = H[-1, :] = 0
H[0, 0] = H[-1, -1] = 1

I_plus = csc_matrix(eye(len(x)) + 1j * dt / 2. * H)
I_minus = csc_matrix(eye(len(x)) - 1j * dt / 2. * H)
U = inv(I_minus).dot(I_plus)

psi = np.exp(-(x+2)**2) / np.sqrt(np.pi)


fig = plt.figure()
ax = fig.gca()
ax.set_xlabel('x')
ax.set_ylabel(r'$|\psi|$')
ax.grid()

for it, t in enumerate(t):
    psi = U.dot(psi)
    psi[0] = psi[-1] = 0
    if it % 4 == 1:
        ax.plot(x, abs(psi))