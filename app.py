import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os

# Page configuration
st.set_page_config(page_title="Dynamic Computational Lab", layout="centered")

TUTORIALS_DIR = "tutorials"

def get_categories():
    """Retrieve list of categories from directory names."""
    if not os.path.exists(TUTORIALS_DIR):
        return []
    return sorted([d for d in os.listdir(TUTORIALS_DIR) if os.path.isdir(os.path.join(TUTORIALS_DIR, d))])

def get_tutorials(category):
    """Retrieve list of tutorials inside a specific category."""
    category_path = os.path.join(TUTORIALS_DIR, category)
    if not os.path.exists(category_path):
        return []
    return sorted([d for d in os.listdir(category_path) if os.path.isdir(os.path.join(category_path, d))])

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Lab Navigation")

categories = get_categories()

if not categories:
    st.title("Welcome to Computational Lab")
    st.info("Please create a 'tutorials' folder and add your categories and lessons.")
else:
    clean_categories = [c.split(". ", 1)[-1] if ". " in c else c for c in categories]
    category_mapping = dict(zip(clean_categories, categories))
    
    selected_clean_cat = st.sidebar.selectbox("Select Field", clean_categories)
    actual_category = category_mapping[selected_clean_cat]
    
    st.sidebar.markdown("---")
    
    tutorials = get_tutorials(actual_category)
    
    if not tutorials:
        st.title(selected_clean_cat)
        st.write("No tutorials available in this section yet.")
    else:
        selected_tutorial = st.sidebar.radio("Available Lessons:", tutorials)
        
        tutorial_path = os.path.join(TUTORIALS_DIR, actual_category, selected_tutorial)
        text_file_path = os.path.join(tutorial_path, "text.md")
        code_file_path = os.path.join(tutorial_path, "code.py")
        
        st.title(selected_tutorial)
        
        if os.path.exists(text_file_path):
            with open(text_file_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.warning("Educational content file (text.md) is missing.")
            
        if os.path.exists(code_file_path):
            with open(code_file_path, "r", encoding="utf-8") as f:
                code_content = f.read()
            
            st.code(code_content, language="python")
            
            if st.button("Run Simulation Code"):
                st.success("Execution completed successfully!")
                try:
                    exec_env = {"st": st, "np": np, "plt": plt}
                    exec(code_content, exec_env)
                except Exception as e:
                    st.error(f"Error executing code: {e}")
        else:
            st.info("No interactive code script available for this lesson.")
