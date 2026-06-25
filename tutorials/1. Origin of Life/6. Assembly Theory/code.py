import streamlit as st

def calculate_assembly_index(target_string):
    # Start with basic alphabet as the initial building blocks
    pool = set(target_string)
    steps = len(pool)  # Initial steps to create basic elements
    
    # Track the sub-structures created along the way (Memory Pool)
    memory = list(pool)
    
    i = 0
    while i < len(target_string):
        matched = False
        # Search for the longest existing sub-structure in memory
        for length in range(len(target_string) - i, 0, -1):
            substring = target_string[i:i+length]
            if substring in memory:
                steps += 1
                i += length
                matched = True
                break
        
        if not matched:
            # If no match found in memory, add single character
            steps += 1
            i += 1
            
        # Update memory with newly generated patterns
        if i < len(target_string):
            memory.append(target_string[:i])
            
    return steps

# --- STREAMLIT UI LAYOUT ---
st.subheader("Assembly Index Computational Solver")

# Interactive sequence input for students
user_sequence = st.text_input("Enter Molecular Sequence String to Analyze:", "XGTYXGTYXGTY")

if user_sequence:
    # Compute the dynamic index
    idx_result = calculate_assembly_index(user_sequence)
    
    st.metric("Computed Assembly Index", idx_result)
    st.metric("Total Sequence Length", len(user_sequence))
    
    # Threshold classification logic
    if idx_result > 15:
        st.success("Assembly Index > 15: Living system signature confirmed! This output cannot be achieved without active evolutionary history and agency.")
    else:
        st.info("Assembly Index <= 15: This structure lies within the expected limits of abiotic chemical physics.")
        
    # Structural breakdown feedback
    st.markdown("### Memory Pool Analysis")
    base_elements = len(set(user_sequence))
    st.write(f"Basic building blocks count (Base Steps): {base_elements}")
    st.write(f"Recursive patterns reused from memory: {len(user_sequence) - idx_result + base_elements}")
