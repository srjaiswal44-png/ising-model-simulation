import numpy as np


def initialize_lattice(size: int, dimension: int = 3, ordered: bool = False) -> np.ndarray:
    """
    Parameters:
    size: Integer --> number of atom sites, if 3 dimensional, then a cubic  lattice wiht (size x size x size) total atoms,
    dimension: Integer --> can take only two values 2 or 3, represent the dimension; square or a cubic lattice,
    ordered: Boolean --> if true: all the spins are alligned and it is one, else: random spins.
    """
    """
    Initializes an dimension-dimensional spin lattice.
    +1 represents spin-up, -1 represents spin-down.
    """

    if dimension not in (2, 3):
        raise ValueError("Dimension must be 2 or 3.")
    
    shape = (size,) * dimension
    if ordered:
        return np.ones(shape, dtype=int)
    else:
        return 2 * np.random.randint(0, 2, size=shape) - 1