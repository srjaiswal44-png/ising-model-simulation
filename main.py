import argparse
import os

import numpy as np

from src.monte_carlo import run_simulation
from src.visualization import plot_simulation_results


def parse_args():
    parser = argparse.ArgumentParser(description="Monte Carlo Simulation of the Ising Model")
    
    parser.add_argument("--size", type=int, default=5, help="Lattice size N (N x N or N x N x N)")
    parser.add_argument("--dim", type=int, choices=[2, 3], default=3, help="Dimension of lattice (2 or 3)")
    parser.add_argument("--ordered", action="store_true", help="Initialize lattice in an ordered state (+1)")
    parser.add_argument("--J", type=float, default=1.0, help="Interaction strength J")
    parser.add_argument("--H", type=float, default=0.0, help="External magnetic field strength H")
    parser.add_argument("--eq-steps", type=int, default=1000, help="Equilibration Metropolis steps per T")
    parser.add_argument("--meas-steps", type=int, default=1000, help="Measurement Metropolis steps per T")
    parser.add_argument("--t-min", type=float, default=0.1, help="Minimum temperature")
    parser.add_argument("--t-max", type=float, default=10.1, help="Maximum temperature")
    parser.add_argument("--t-step", type=float, default=0.2, help="Temperature step size")
    parser.add_argument("--save-plot", type=str, default=None, help="Custom output filename/path for plot")

    return parser.parse_args()

def generate_plot_filename(args) -> str:
    """Generates a parameter-based filename without timestamps."""
    filename = f"ising_{args.dim}d_N{args.size}_J{args.J}_H{args.H}_eq{args.eq_steps}_meas{args.meas_steps}.png"
    return os.path.join("plots", filename)

def main():
    args = parse_args()

    # Determine plot save path
    if args.save_plot is None:
        plot_save_path = generate_plot_filename(args)
    else:
        plot_save_path = args.save_plot

    temperatures = np.arange(args.t_min, args.t_max, args.t_step)

    print("=" * 60)
    print("Starting Ising Model MCMC Simulation...")
    print(f"Lattice: {args.size}^{args.dim} | J: {args.J} | H: {args.H}")
    print(f"Equilibration Steps: {args.eq_steps} | Measurement Steps: {args.meas_steps}")
    print(f"Plot save path: {plot_save_path}")
    print("=" * 60)

    energy, magnetization, specific_heat, susceptibility = run_simulation(
        size=args.size,
        dimension=args.dim,
        ordered=args.ordered,
        J=args.J,
        H=args.H,
        temperatures=temperatures,
        equilibrium_steps=args.eq_steps,
        measurement_steps=args.meas_steps
    )

    print("\nSimulation complete! Generating plots...")
    plot_simulation_results(
        temperatures=temperatures,
        energy=energy,
        magnetization=magnetization,
        specific_heat=specific_heat,
        susceptibility=susceptibility,
        size=args.size,
        save_path=plot_save_path
    )

if __name__ == "__main__":
    main()