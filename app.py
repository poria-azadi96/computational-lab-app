import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuration for the web layout
st.set_page_config(page_title="Computational Biology Lab", layout="centered")

# Main sidebar for navigation
st.sidebar.title("Lab Navigation")
category = st.sidebar.selectbox("Select Main Field", ["Theoretical Biology", "Bioinformatics Models"])

# First Category: Theoretical Biology
if category == "Theoretical Biology":
    st.sidebar.markdown("---")
    tutorial = st.sidebar.radio("Available Tutorials:", ["Dissipative Structures", "Autopoiesis Dynamics"])
    
    if tutorial == "Dissipative Structures":
        st.title("Study of Dissipative Structures")
        
        # Educational content using markdown
        st.markdown("""
        In non-equilibrium systems, order emerges through **Dissipative Structures**. 
        Review the simulation block below and click the button to observe the graphical outcome.
        """)
        
        # Presenting the code block to students
        st.code("""
# Simulation script for thermodynamic dissipation
time = np.linspace(0, 10, 200)
decay = np.exp(-0.2 * time) * np.cos(3 * np.pi * time)
fig, ax = plt.subplots()
ax.plot(time, decay, color='magenta')
st.pyplot(fig)
        """, language="python")
        
        # Interactive button to trigger calculation
        if st.button("Execute Simulation Code"):
            st.success("Execution completed successfully!")
            time = np.linspace(0, 10, 200)
            decay = np.exp(-0.2 * time) * np.cos(3 * np.pi * time)
            fig, ax = plt.subplots()
            ax.plot(time, decay, color='#ff007f') # Neon pink style
            st.pyplot(fig)

# Second Category: Bioinformatics Models
elif category == "Bioinformatics Models":
    st.title("Bioinformatics Practical Codes")
    st.info("The structural biology and alignment scripts will be available here soon.")
