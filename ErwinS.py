import numpy as np
import matplotlib.pyplot as plt
from findiff import FinDiff
from scipy.sparse.linalg import inv
from scipy.sparse import eye, diags
import matplotlib.animation as animation

def Simulation(x,v_x,wave_placement):
    plt.rcParams["axes.labelsize"] = 16
    
    print("Please input desired wave placement:")
    print(type(wave_placement))
    # Input parameters
    Nx = len(x)

    
    Nt = 250
    tmin = 0
    tmax = 20
    k = 1 
    
    # Calculate grid, potential, and initial wave function
    x_array = x
    t_array = np.linspace(tmin, tmax, Nt)
    psi = np.exp(-(x_array - wave_placement)**2)
    
    # Calculate finite difference elements
    dt = t_array[1] - t_array[0]
    dx = x_array[1] - x_array[0]
    
    # Convert to a diagonal matrix
    v_x_matrix = diags(v_x)
    
    # Calculate the Hamiltonian matrix
    H = -0.5 * FinDiff(0, dx, 2).matrix(x_array.shape) + v_x_matrix
    
    # Apply boundary conditions to the Hamiltonian
    H[0, :] = H[-1, :] = 0
    H[0, 0] = H[-1, -1] = 1
    
    # Calculate U
    I_plus = eye(Nx) + 1j * dt / 2. * H
    I_minus = eye(Nx) - 1j * dt / 2. * H
    U = inv(I_minus).dot(I_plus)
    
    # Iterate over each time, appending each calculation of psi to a list
    psi_list = []
    for t in t_array:
        psi = U.dot(psi)
        psi[0] = psi[-1] = 0
        psi_list.append(np.abs(psi))
        
    psi_mag_squared = np.abs(psi_list)**2
    
    
    fig, ax = plt.subplots()
    
    ax.set_xlabel("x [arb units]")
    ax.set_ylabel("$|\Psi(x, t)|$", color="C0")
    
    ax_twin = ax.twinx()
    ax_twin.plot(x_array, v_x, color="C1")
    ax_twin.set_ylabel("V(x) [arb units]", color="C1")
    
    line, = ax.plot([], [], color="C0", lw=2)
    ax.grid()
    xdata, ydata = [], []
    
    def run(psi):
        line.set_data(x_array, np.abs(psi)**2)
        return line,
    
    ax.set_xlim(x_array[0], x_array[-1])
    ax.set_ylim(0, 1)
    
    ani = animation.FuncAnimation(fig, run, psi_list, interval=10)
    ani.save("Example.gif", fps=120)