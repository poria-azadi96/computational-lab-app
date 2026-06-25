import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# 1. Stochastic Particle Dynamics Function inside Mineral Micropores
def run_vent_simulation(num_particles, num_steps, thermophoresis_drift, diffusion_noise, grid_size=100):
    """
    Simulates Brownian motion combined with thermal drift (Soret Effect).
    Tracks how thermal gradients overcome entropy to accumulate matter.
    """
    # Initialize particle positions randomly within the pore matrix
    x_positions = np.random.uniform(0, grid_size, num_particles)
    y_positions = np.random.uniform(0, grid_size, num_particles)
    concentration_history = []

    # Execute stochastic iteration loops
    for step in range(num_steps):
        # Gaussian noise representing random thermal fluctuations
        x_noise = np.random.normal(0, diffusion_noise, num_particles)
        y_noise = np.random.normal(0, diffusion_noise, num_particles)
        
        # Apply thermophoretic directional drift toward the cold boundary (positive x)
        x_positions += x_noise + thermophoresis_drift
        y_positions += y_noise
        
        # Enforce physical boundary constraints of the mineral cavern
        x_positions = np.clip(x_positions, 0, grid_size)
        y_positions = np.clip(y_positions, 0, grid_size)
        
        # Calculate fraction of molecules accumulated in the cold trap zone (x > 80)
        trapped_particles = np.sum(x_positions > 80)
        concentration_ratio = (trapped_particles / num_particles) * 100
        concentration_history.append(concentration_ratio)
        
    return concentration_history

# --- STREAMLIT UI LAYOUT ---
st.subheader("Hydrothermal Vent Micro-Pore Thermophoresis Simulator")

# Sidebar controllers for thermodynamic constraints tuning
st.sidebar.markdown("### Environmental Gradients")
drift = st.sidebar.slider("Thermophoretic Drift Intensity (Soret Factor)", 0.0, 1.0, 0.3, 0.05)
noise = st.sidebar.slider("Molecular Diffusion Noise (Brownian Motion)", 0.1, 2.0, 1.0, 0.1)

st.sidebar.markdown("### System Scale")
particles_count = st.sidebar.slider("Total Initial Precursor Particles", 200, 2000, 1000, 100)
simulation_steps = st.sidebar.slider("Total Temporal Steps", 100, 1000, 400, 50)

# 2. Run stochastic engine
history = run_vent_simulation(particles_count, simulation_steps, drift, noise)

# 3. Visual Rendering Setup
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor('#0e1117')
ax.set_facecolor('#0e1117')

# Plotting the real-time localized concentration curve
ax.plot(history, color='#00ffff', linewidth=2.5, label='Trapped Precursors (%)')

# Aesthetic parameter configurations
ax.set_title("Molecular Accumulation Trajectory in Cold Zone", color='white', fontsize=14)
ax.set_xlabel("Time Steps", color='white')
ax.set_ylabel("Concentration Ratio inside Trap Zone (%)", color='white')
ax.grid(alpha=0.2, linestyle='--')
ax.legend(facecolor='#0e1117', edgecolor='gray', labelcolor='white')

ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')
ax.tick_params(colors='white')

st.pyplot(fig)

# Final analytical quantitative metric reporting
st.info(f"Simulation completed. Final concentration localized in trap zone: {history[-1]:.1f}%")
