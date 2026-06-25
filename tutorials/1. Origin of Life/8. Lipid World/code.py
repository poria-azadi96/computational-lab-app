import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# 1. Vectorized GARD Simulation Engine
def run_gard_simulation(n_types, n_max, steps, dt, kf, kb, seed=42):
    """
    Simulates the Graded Autocatalytic Replication Domain (GARD) model.
    Tracks kinetic influx/efflux and vesicle fission events.
    """
    np.random.seed(seed)
    
    # Beta Matrix: Non-negative random catalytic interaction networks
    beta = np.random.uniform(0.1, 5.0, (n_types, n_types))
    # Constant buffered environmental concentration of free precursors
    rho = np.ones(n_types) * 2.5

    # Initializing Vesicle Molecular Counts
    n = np.random.randint(2, 8, n_types).astype(float)
    history = []
    fission_events = []

    # Dynamic Simulation Loop
    for step in range(steps):
        N = np.sum(n)
        if N <= 0:
            break
            
        # Evaluating Compositional Catalysis Factor using vector dot product
        catalysis_factor = 1.0 + np.dot(beta, n / N)
        
        # Differential changes in concentration components over time
        dn = (kf * rho - kb * n) * catalysis_factor * dt
        n += dn
        n = np.maximum(n, 0.0)  # Boundary protection
        
        # Evaluating Fission Threshold
        if np.sum(n) >= n_max:
            # Stochastic splitting via multinomial sample
            probabilities = n / np.sum(n)
            half_size = int(n_max / 2)
            n = np.random.multinomial(half_size, probabilities).astype(float)
            fission_events.append(step)
            
        history.append(n.copy())
        
    return np.array(history), fission_events, n_types

# --- STREAMLIT UI LAYOUT ---
st.subheader("GARD Compositional Kinetic Network Solver")

# Sidebar parameter controls for dynamic membrane tracking
st.sidebar.markdown("### Vesicle Physical Properties")
n_max = st.sidebar.slider("Critical Fission Threshold (N_MAX)", 50, 200, 100, 10)
n_types = st.sidebar.slider("Amphiphile Chemical Species Types", 3, 10, 5, 1)

st.sidebar.markdown("### Influx/Efflux Basal Rates")
kf = st.sidebar.slider("Basal Entry Rate Constant (kf)", 0.05, 0.30, 0.10, 0.01)
kb = st.sidebar.slider("Basal Exit Rate Constant (kb)", 0.05, 0.40, 0.20, 0.01)

# 2. Compute dynamic simulation state
history, fission_events, current_types = run_gard_simulation(
    n_types=n_types, 
    n_max=n_max, 
    steps=5000, 
    dt=0.01, 
    kf=kf, 
    kb=kb
)

# 3. Graphical Visualization Setup
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#0e1117')
ax.set_facecolor('#0e1117')

# Plotting each lipid profile concentration over time
for i in range(current_types):
    ax.plot(history[:, i], label=f'Lipid Type {i+1}', linewidth=2)

# Marking fission cycles on the trajectory graph
for event in fission_events:
    ax.axvline(x=event, color='gray', linestyle='--', alpha=0.4)

# Formatting axes aesthetics
ax.set_xlabel('Simulation Steps', color='white')
ax.set_ylabel('Molar Count Within Vesicle Cluster (n_i)', color='white')
ax.set_title('Compositional Homeostasis & Fission Dynamics', color='white', fontsize=14)
ax.legend(facecolor='#0e1117', edgecolor='gray', labelcolor='white')
ax.grid(alpha=0.2, linestyle='--')

ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')
ax.tick_params(colors='white')

st.pyplot(fig)

# Display numerical performance metrics to user
st.info(f"Simulation completed. Total self-regulated division cycles achieved: {len(fission_events)}")
