import numpy as np


def calculate_magnetization(lattice: np.ndarray) -> int:
    """Calculates total magnetization of the lattice."""
    return np.sum(lattice)

def get_neighbor_sum(lattice: np.ndarray, coords: tuple) -> int:
    """Calculates nearest-neighbor spin sum using periodic boundary conditions."""
    N = len(lattice)
    if len(coords) == 2:
        i, j = coords
        return (lattice[(i + 1) % N, j] +
                lattice[(i - 1 + N) % N, j] +
                lattice[i, (j + 1) % N] +
                lattice[i, (j - 1 + N) % N])
    elif len(coords) == 3:
        i, j, k = coords
        return (lattice[i, j, (k + 1) % N] +
                lattice[i, j, (k - 1 + N) % N] +
                lattice[i, (j + 1) % N, k] +
                lattice[i, (j - 1 + N) % N, k] +
                lattice[(i + 1) % N, j, k] +
                lattice[(i - 1 + N) % N, j, k])
    else:
        raise ValueError("Only 2D and 3D coordinates are supported.")

def calculate_hamiltonian(lattice: np.ndarray, J: float = 1.0, H: float = 0.0) -> float:
    """Calculates total energy (Hamiltonian) of the system."""
    dim = lattice.ndim
    N = len(lattice)
    total_energy = 0.0

    if dim == 2:
        for i in range(N):
            for j in range(N):
                s = lattice[i, j]
                total_energy += -J * s * get_neighbor_sum(lattice, (i, j))
    elif dim == 3:
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    s = lattice[i, j, k]
                    total_energy += -J * s * get_neighbor_sum(lattice, (i, j, k))

    # Double counting correction for nearest-neighbor bonds
    return (total_energy / 2.0) - (H * calculate_magnetization(lattice))

def calculate_thermodynamics(energy_list: list, mag_list: list, T: float) -> tuple:
    """Computes average energy, magnetization, specific heat (Cv), and susceptibility (Chi)."""
    E_avg = float(np.mean(energy_list))
    E2_avg = float(np.mean(np.array(energy_list) ** 2))
    
    M_avg = float(np.mean(mag_list))
    M2_avg = float(np.mean(np.array(mag_list) ** 2))

    # Cv = (<E^2> - <E>^2) / T^2
    specific_heat = (E2_avg - (E_avg ** 2)) / (T ** 2)
    
    # Chi = (<M^2> - <M>^2) / T
    susceptibility = (M2_avg - (M_avg ** 2)) / T

    return E_avg, M_avg, specific_heat, susceptibility