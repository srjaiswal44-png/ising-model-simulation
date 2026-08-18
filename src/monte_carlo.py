import numpy as np

from src.lattice import initialize_lattice
from src.physics import (calculate_hamiltonian, calculate_magnetization,
                         calculate_thermodynamics, get_neighbor_sum)


def metropolis_step(lattice: np.ndarray, temperature: float, J: float = 1.0, H: float = 0.0) -> np.ndarray:
    """Performs N^dim spin-flip attempts using the Metropolis algorithm."""
    N = len(lattice)
    dim = lattice.ndim
    num_sweeps = N ** dim

    for _ in range(num_sweeps):
        if dim == 2:
            i, j = np.random.randint(0, N), np.random.randint(0, N)
            spin = lattice[i, j]
            neighbor_sum = get_neighbor_sum(lattice, (i, j))
        else:
            i, j, k = np.random.randint(0, N), np.random.randint(0, N), np.random.randint(0, N)
            spin = lattice[i, j, k]
            neighbor_sum = get_neighbor_sum(lattice, (i, j, k))

        dE = (2 * J * spin * neighbor_sum) + (2 * H * spin)

        # Accept flip if energy decreases or based on Boltzmann probability
        if dE <= 0 or np.random.rand() <= np.exp(-dE / temperature):
            if dim == 2:
                lattice[i, j] *= -1
            else:
                lattice[i, j, k] *= -1

    return lattice

def run_simulation(size: int, dimension: int, ordered: bool, J: float, H: float, 
                   temperatures: np.ndarray, equilibrium_steps: int, measurement_steps: int):
    """Runs full MCMC simulation across temperature range and computes thermodynamic quantities."""
    lattice = initialize_lattice(size=size, dimension=dimension, ordered=ordered)

    energy_list, mag_list, specific_heat_list, susceptibility_list = [], [], [], []

    for T in temperatures:
        # 1. Equilibrate system
        for _ in range(equilibrium_steps):
            lattice = metropolis_step(lattice, temperature=T, J=J, H=H)

        # 2. Measurement steps
        E_step_list, M_step_list = [], []
        for _ in range(measurement_steps):
            lattice = metropolis_step(lattice, temperature=T, J=J, H=H)
            E_step_list.append(calculate_hamiltonian(lattice, J=J, H=H))
            M_step_list.append(calculate_magnetization(lattice))

        # 3. Calculate thermodynamics at temperature T
        E_avg, M_avg, C_v, chi = calculate_thermodynamics(E_step_list, M_step_list, T)

        energy_list.append(E_avg)
        mag_list.append(M_avg)
        specific_heat_list.append(C_v)
        susceptibility_list.append(chi)

    return energy_list, mag_list, specific_heat_list, susceptibility_list