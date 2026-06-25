import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
import sqlite3
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Dynamic Computational Lab", layout="wide")

# --- OPTION 5: CUSTOM CSS INJECTION (CYBERNETIC THEME) ---
cyber_css = """
<style>
    /* Main application background and font smoothing */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    /* Right align and RTL directional formatting for Persian texts */
    h1, h2, h3, h4 {
        color: #00ffcc !important; /* Neon Cyan accents */
        text-align: right;
        direction: rtl;
    }
    p, li, span, label {
        text-align: right;
        direction: rtl;
        font-size: 1.05rem;
    }
    /* Sidebar navigation customized border and dark background */
    section[data-testid="stSidebar"] {
        background-color: #07090e !important;
        border-right: 2px solid #ff007f !important; /* Cyber Pink Boundary */
    }
    /* Customizing data metric outputs display */
    div[data-testid="stMetricValue"] {
        color: #ff007f !important;
    }
    /* High contrast interactive button styling */
    .stButton>button {
        background-color: #00ffcc !important;
        color: #000000 !important;
        font-weight: bold;
        border-radius: 6px;
        width: 100%;
        border: none;
    }
</style>
"""
st.markdown(cyber_css, unsafe_allow_html=True)

# --- OPTION 2: LOCAL DATABASE INTEGRATION (SQLITE) ---
DB_FILE = "lab_storage.db"

def init_db():
    """Initialize local SQLite database schema for logging user interactions."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  category TEXT, 
                  tutorial TEXT, 
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

def log_activity(category, tutorial):
    """Log the current evaluated tutorial session to global database storage."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO history (category, tutorial, timestamp) VALUES (?, ?, ?)", 
              (category, tutorial, now))
    conn.commit()
    conn.close()

def get_recent_history():
    """Retrieve recent recorded sessions sequentially from sqlite database."""
    if not os.path.exists(DB_FILE):
        return []
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT category, tutorial, timestamp FROM history ORDER BY id DESC LIMIT 5")
    rows = c.fetchall()
    conn.close()
    return rows

# Automatically execute database connection engine on launch
init_db()

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
        
        # Silently commit log event to database on evaluation navigation
        log_activity(selected_clean_cat, selected_tutorial)
        
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

# --- SIDEBAR DATABASE LIVE TRACKING VIEW ---
st.sidebar.markdown("---")
st.sidebar.subheader("آخرین فعالیت‌های ثبت‌شده در دیتابیس")
history_logs = get_recent_history()
for log in history_logs:
    st.sidebar.caption(f"⏱️ {log[2]} \n {log[0]} ➔ {log[1]}")
