import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import streamlit as st

# 1. Hypercycle system of coupled differential equations
def hypercycle_ode_system(t, y, k_rates, K_coeffs):
    """
    t: current time parameter
    y: concentration array of replicators
    k_rates: list of self-replication rates
    K_coeffs: list of cross-catalytic support coefficients
    """
    n = len(y)
    dydt = np.zeros(n)
    growth_rates = np.zeros(n)
    total_growth = 0
    
    # Calculate growth for each node in the closed loop
    for i in range(n):
        helper_idx = (i - 1) % n
        growth_rates[i] = y[i] * (k_rates[i] + K_coeffs[i] * y[helper_idx])
        total_growth += growth_rates[i]
    
    # Dilution flux to maintain constant total mass concentration
    sum_y = np.sum(y)
    phi = total_growth / sum_y if sum_y > 0 else 0
    
    # Final non-linear differential equation computation
    for i in range(n):
        dydt[i] = growth_rates[i] - y[i] * phi
        
    return dydt

# --- STREAMLIT UI LAYOUT ---
st.subheader("Manfred Eigen's Hypercycle Dynamics Solver")

# Dynamic parameter selection sidebar
st.sidebar.markdown("### Kinetic Coefficients")
base_k = st.sidebar.slider("Base Self-Replication Rate (k)", 0.01, 0.50, 0.10, 0.01)
base_K = st.sidebar.slider("Cross-Catalytic Coefficient (K)", 0.5, 5.0, 2.5, 0.1)

st.sidebar.markdown("### Initial Asymmetric Concentrations")
y1 = st.sidebar.slider("Replicator 1 Concentration", 0.05, 0.60, 0.40, 0.05)
y2 = st.sidebar.slider("Replicator 2 Concentration", 0.05, 0.60, 0.30, 0.05)
y3 = st.sidebar.slider("Replicator 3 Concentration", 0.05, 0.60, 0.20, 0.05)
y4 = st.sidebar.slider("Replicator 4 Concentration", 0.05, 0.60, 0.10, 0.05)

# 2. Solver Configuration
n_nodes = 4
k_rates = [base_k] * n_nodes
K_coeffs = [base_K] * n_nodes
initial_state = [y1, y2, y3, y4]
time_span = (0, 30)
time_eval_points = np.linspace(0, 30, 600)

# Compute numerical solutions using SciPy integration tool
solution = solve_ivp(
    hypercycle_ode_system, 
    time_span, 
    initial_state, 
    args=(k_rates, K_coeffs), 
    t_eval=time_eval_points
)

# 3. Graph Visual Output Setup
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#0e1117')
ax.set_facecolor('#0e1117')

# Color definitions for clear differentiation
colors = ['#00ffcc', '#ff007f', '#39ff14', '#bc13fe']

for i in range(n_nodes):
    ax.plot(solution.t, solution.y[i], label=f'Replicator {i+1}', color=colors[i], linewidth=2.5)

# Style parameters configuration
ax.set_xlabel('Time Units', color='white')
ax.set_ylabel('Relative Concentration', color='white')
ax.set_title("Hypercycle Convergence to Stable Equilibrium", color='white', fontsize=14)
ax.legend(facecolor='#0e1117', edgecolor='gray', labelcolor='white')
ax.grid(alpha=0.2, linestyle='--')

ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')
ax.tick_params(colors='white')

st.pyplot(fig)

st.info("Notice how the initial asymmetric chaos naturally self-organizes into a rhythmic, steady co-existence.")
