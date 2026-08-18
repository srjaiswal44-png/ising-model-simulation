import os

import matplotlib.pyplot as plt


def plot_simulation_results(temperatures, energy, magnetization, specific_heat, susceptibility, size, save_path="plots/simulation_result.png"):
    """Generates a 2x2 subplot of thermodynamic properties and saves the image."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f"Ising Model Simulation (Lattice Size = {size}x{size})", fontsize=16)

    # Energy
    ax1.plot(temperatures, energy, 'o-', color='tab:blue')
    ax1.set_xlabel("Temperature (T)")
    ax1.set_ylabel("Energy")
    ax1.set_title("Average Energy")
    ax1.grid(True)

    # Magnetization
    ax2.plot(temperatures, magnetization, 'o-', color='tab:orange')
    ax2.set_xlabel("Temperature (T)")
    ax2.set_ylabel("Magnetization")
    ax2.set_title("Average Magnetization")
    ax2.grid(True)

    # Specific Heat
    ax3.plot(temperatures, specific_heat, 'o-', color='tab:green')
    ax3.set_xlabel("Temperature (T)")
    ax3.set_ylabel("Specific Heat (Cv)")
    ax3.set_title("Specific Heat")
    ax3.grid(True)

    # Magnetic Susceptibility
    ax4.plot(temperatures, susceptibility, 'o-', color='tab:red')
    ax4.set_xlabel("Temperature (T)")
    ax4.set_ylabel("Magnetic Susceptibility (χ)")
    ax4.set_title("Magnetic Susceptibility")
    ax4.grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Ensure plots output directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    print(f"Plot saved successfully to '{save_path}'")
    plt.show()