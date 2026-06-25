import random
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

# 1. Molecular Generation functions
def generate_binary_polymers(max_len):
    """Generate all binary polymer strings up to a specific maximum length."""
    polymers = []
    for length in range(1, max_len + 1):
        for i in range(2**length):
            binary_str = bin(i)[2:].zfill(length)
            polymers.append(binary_str)
    return polymers

def generate_reaction_network(polymers, max_len):
    """Map out all possible ligation reactions within the defined size bounds."""
    reactions = []
    for m1 in polymers:
        for m2 in polymers:
            product = m1 + m2
            if len(product) <= max_len:
                reactions.append((m1, m2, product))
    return reactions

# 2. Catalysis Assignment Simulation
def simulate_catalysis(polymers, reactions, probability):
    """Randomly assign molecules to catalyze reactions based on probability."""
    catalysis_map = {rxn: [] for rxn in reactions}
    for rxn in reactions:
        for p in polymers:
            if random.random() < probability:
                catalysis_map[rxn].append(p)
    return catalysis_map

# 3. Dynamic Network Extraction
def extract_autocatalytic_set(reactions, catalysis_map):
    """Construct graph structure filter out un-catalyzed pathway noise."""
    G = nx.DiGraph()
    catalyzed_count = 0
    
    for m1, m2, prod in reactions:
        catalysts = catalysis_map[(m1, m2, prod)]
        if catalysts:
            catalyzed_count += 1
            # Add metabolic structural paths
            G.add_edge(m1, prod, role='reactant')
            G.add_edge(m2, prod, role='reactant')
            # Add chemical feedback loops
            for cat in catalysts:
                G.add_edge(cat, prod, role='catalyst')
                
    return G, catalyzed_count

# --- STREAMLIT UI PARAMETERS AND EXECUTION ---
st.subheader("Advanced Autocatalytic System Dashboard")

# High-depth simulation parameters configuration
max_polymer_length = 4
catalysis_probability = 0.12

# Run heavy topological computations
polymers_pool = generate_binary_polymers(max_polymer_length)
chemical_reactions = generate_reaction_network(polymers_pool, max_polymer_length)
assigned_catalysis = simulate_catalysis(polymers_pool, chemical_reactions, catalysis_probability)
network_graph, active_reactions = extract_autocatalytic_set(chemical_reactions, assigned_catalysis)

# Mathematical analysis report rendering
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Molecular Species", len(polymers_pool))
with col2:
    st.metric("Catalyzed Reactions", active_reactions)

# Graphical visualization layout
fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor('#0e1117')
ax.set_facecolor('#0e1117')

if len(network_graph.nodes) > 0:
    pos = nx.spring_layout(network_graph, seed=42)
    
    # Differentiate visual styling based on network roles
    nx.draw_networkx_nodes(network_graph, pos, node_color='#00ffcc', node_size=700, alpha=0.8, ax=ax)
    nx.draw_networkx_labels(network_graph, pos, font_size=8, font_color='white', font_weight='bold', ax=ax)
    
    # Rendering interaction paths
    nx.draw_networkx_edges(network_graph, pos, edge_color='gray', arrows=True, alpha=0.5, ax=ax)
    
    ax.axis('off')
    st.pyplot(fig)
else:
    st.warning("No dynamic autocatalytic closure achieved at this low catalysis probability.")
