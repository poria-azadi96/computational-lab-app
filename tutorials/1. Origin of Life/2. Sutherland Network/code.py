import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import streamlit as st

# 1. Mathematical formulation of the system of ODEs
def sutherland_advanced_network(t, y, k_nucleo, k_amino, k_lipid):
    """
    t: current time step
    y: list of concentrations [HCN, H2S, Nucleotides, Amino_Acids, Lipids]
    """
    HCN, H2S, Nucleo, Amino, Lipid = y
    
    # Prebiotic reaction rates based on mass action kinetics
    r_nucleo = k_nucleo * HCN * H2S
    r_amino = k_amino * HCN
    r_lipid = k_lipid * H2S * HCN
    
    # Precursors are consumed
    dHCN = -r_nucleo - r_amino - r_lipid
    dH2S = -r_nucleo - r_lipid
    
    # Synchronous biopoiesis products are formed
    dNucleo = r_nucleo
    dAmino = r_amino
    dLipid = r_lipid
    
    return [dHCN, dH2S, dNucleo, dAmino, dLipid]

# --- STREAMLIT UI LAYOUT ---
st.subheader("Prebiotic Systems Chemistry Solver (Sutherland Model)")

# Sidebar sliders for custom interactive kinetic simulations
st.sidebar.markdown("### Kinetic Rate Constants")
k_nucleo = st.sidebar.slider("RNA Precursor Rate (k_nucleo)", 0.01, 0.10, 0.04, 0.01)
k_amino = st.sidebar.slider("Protein Precursor Rate (k_amino)", 0.01, 0.10, 0.02, 0.01)
k_lipid = st.sidebar.slider("Lipid Membrane Rate (k_lipid)", 0.01, 0.10, 0.03, 0.01)

st.sidebar.markdown("### Initial Concentrations (Molar)")
init_hcn = st.sidebar.slider("Initial HCN", 0.5, 2.0, 1.0, 0.1)
init_h2s = st.sidebar.slider("Initial H2S", 0.5, 2.0, 0.8, 0.1)

# 2. Solver Setup
initial_state = [init_hcn, init_h2s, 0.0, 0.0, 0.0]
time_span = (0, 150)
time_points = np.linspace(0, 150, 600)

# Compute non-linear coupled differential equations using SciPy
sol = solve_ivp(
    sutherland_advanced_network, 
    time_span, 
    initial_state, 
    args=(k_nucleo, k_amino, k_lipid), 
    t_eval=time_points
)

# 3. Visualization and Rendering Layout
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#0e1117')
ax.set_facecolor('#0e1117')

# Plotting concentration dynamics over time
ax.plot(sol.t, sol.y[0], label='HCN (Precursor)', color='red', linestyle='--', alpha=0.7)
ax.plot(sol.t, sol.y[1], label='H2S (Precursor)', color='orange', linestyle='--', alpha=0.7)
ax.plot(sol.t, sol.y[2], label='Nucleotides (RNA)', color='#00ffcc', linewidth=2.5)
ax.plot(sol.t, sol.y[3], label='Amino Acids (Proteins)', color='#ff007f', linewidth=2.5)
ax.plot(sol.t, sol.y[4], label='Lipids (Membrane)', color='#purple', linewidth=2.5)

# Graphical styling parameters
ax.set_xlabel('Time Units', color='white')
ax.set_ylabel('Molar Concentration', color='white')
ax.set_title('Synchronous Production of Life Components', color='white', fontsize=14)
ax.legend(facecolor='#0e1117', edgecolor='gray', labelcolor='white')
ax.grid(alpha=0.2, linestyle='--')

ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')
ax.tick_params(colors='white')

st.pyplot(fig)

# Show final concentrations as analytical feedback
st.info(f"Final State -> RNA Precursors: {sol.y[2][-1]:.3f} M | Amino Acids: {sol.y[3][-1]:.3f} M | Lipids: {sol.y[4][-1]:.3f} M")
