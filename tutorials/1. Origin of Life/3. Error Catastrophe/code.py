import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# 1. Vectorized Quasispecies Evolution Engine
def run_quasispecies_simulation(pop_size, seq_len, generations, mutation_rate, master_fitness):
    """
    Simulates molecular evolution and tracks error catastrophe thresholds.
    All calculations are vectorized via NumPy for maximum execution speed.
    """
    # Initialize population: All arrays start as Master Sequence (all 1s)
    pop = np.ones((pop_size, seq_len), dtype=int)
    master_ratio_history = []

    for _ in range(generations):
        # Calculate fitness: Master sequence gets premium advantage, others get baseline
        current_sum = pop.sum(axis=1)
        fitness = np.where(current_sum == seq_len, master_fitness, 1.0)
        
        # Selection step based on evolutionary fitness probabilities
        probabilities = fitness / fitness.sum()
        selected_indices = np.random.choice(pop_size, size=pop_size, p=probabilities)
        pop = pop[selected_indices]
        
        # Mutation step: Stochastic bit flips across the entire matrix
        mutation_mask = np.random.random(pop.shape) < mutation_rate
        pop = np.bitwise_xor(pop, mutation_mask)
        
        # Track the fraction of perfect Master Sequences remaining
        master_count = (pop.sum(axis=1) == seq_len).sum()
        master_ratio_history.append(master_count / pop_size)
        
    return master_ratio_history

# --- STREAMLIT UI LAYOUT ---
st.subheader("Eigen's Quasispecies & Error Catastrophe Solver")

# Sidebar parameters for customized mathematical tracking
st.sidebar.markdown("### Population & Genome Constraints")
pop_size = st.sidebar.slider("Population Size", 500, 2000, 1000, 100)
seq_len = st.sidebar.slider("Sequence Length (Global Bits)", 10, 50, 25, 5)
generations = st.sidebar.slider("Total Generations", 50, 300, 150, 10)
master_fitness = st.sidebar.slider("Master Selection Advantage", 1.5, 5.0, 2.0, 0.5)

st.sidebar.markdown("### Mutation Rate Scenarios")
mutation_low = st.sidebar.slider("Low Mutation Rate (Stable)", 0.001, 0.05, 0.01, 0.001)
mutation_high = st.sidebar.slider("High Mutation Rate (Melting)", 0.05, 0.30, 0.15, 0.01)

# 2. Compute evolutionary paths
low_mutation_history = run_quasispecies_simulation(pop_size, seq_len, generations, mutation_low, master_fitness)
high_mutation_history = run_quasispecies_simulation(pop_size, seq_len, generations, mutation_high, master_fitness)

# 3. Visualization Layout
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#0e1117')
ax.set_facecolor('#0e1117')

# Plotting histories for contrast analysis
ax.plot(low_mutation_history, label=f'Low Mutation ({mutation_low*100:.1f}%)', color='#11caa0', linewidth=2.5)
ax.plot(high_mutation_history, label=f'High Mutation ({mutation_high*100:.1f}%)', color='#e63946', linewidth=2.5)

# Visual aesthetics configuration
ax.set_xlabel('Generations', color='white')
ax.set_ylabel('Master Sequence Fraction', color='white')
ax.set_title("Information Melting Threshold Graph", color='white', fontsize=14)
ax.legend(facecolor='#0e1117', edgecolor='gray', labelcolor='white')
ax.grid(alpha=0.2, linestyle='--')

ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')
ax.tick_params(colors='white')

st.pyplot(fig)

# Analytical reporting to dashboard user
st.info(f"Final Master Fraction -> Low Mutation: {low_mutation_history[-1]*100:.1f}% | High Mutation: {high_mutation_history[-1]*100:.1f}%")
