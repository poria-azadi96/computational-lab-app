import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
import sqlite3
import uuid
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Dynamic Computational Lab", layout="wide")

# --- OPTION 5: UPDATED EYE-FRIENDLY CSS INJECTION (SOFT DARK THEME) ---
soft_dark_css = """
<style>
    /* Soft dark slate blue background for eye protection */
    .stApp {
        background-color: #0f172a;
        color: #cbd5e1;
    }
    /* Softer Sky Blue accents for headers, right-aligned for Persian */
    h1, h2, h3, h4 {
        color: #38bdf8 !important;
        text-align: right;
        direction: rtl;
    }
    /* Muted text colors to prevent high-contrast eye strain */
    p, li, span, label {
        text-align: right;
        direction: rtl;
        font-size: 1.05rem;
        color: #e2e8f0;
    }
    /* Muted sidebar background with elegant subtle border */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155 !important;
    }
    /* Smooth color transformation for key metric data displays */
    div[data-testid="stMetricValue"] {
        color: #38bdf8 !important;
    }
    /* Solid ocean blue button styling without aggressive neon glow */
    .stButton>button {
        background-color: #0284c7 !important;
        color: #ffffff !important;
        font-weight: bold;
        border-radius: 6px;
        width: 100%;
        border: none;
    }
</style>
"""
st.markdown(soft_dark_css, unsafe_allow_html=True)

# --- OPTION 2: ISOLATED DATABASE INTEGRATION (SQLITE + SESSION STATE) ---
DB_FILE = "lab_storage.db"

# Initialize a distinct browser token for tracking current user only
if "user_token" not in st.session_state:
    st.session_state["user_token"] = str(uuid.uuid4())

def init_db():
    """Initialize database schema with token separation framework."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  token TEXT,
                  category TEXT, 
                  tutorial TEXT, 
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

def log_activity(category, tutorial):
    """Log tutorial visit securely tied to the unique user token."""
    token = st.session_state["user_token"]
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO history (token, category, tutorial, timestamp) VALUES (?, ?, ?, ?)", 
              (token, category, tutorial, now))
    conn.commit()
    conn.close()

def get_recent_history():
    """Retrieve history logs restricted exclusively to the active browser token."""
    token = st.session_state["user_token"]
    if not os.path.exists(DB_FILE):
        return []
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT category, tutorial, timestamp FROM history WHERE token = ? ORDER BY id DESC LIMIT 5", (token,))
    rows = c.fetchall()
    conn.close()
    return rows

# Launch database creation sequence
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
        
        # Committing isolated log entry safely hidden from global access
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

# --- SIDEBAR SESSION-ISOLATED LOGS VIEW ---
st.sidebar.markdown("---")
st.sidebar.subheader("آخرین فعالیت‌های شما در این نشست")
history_logs = get_recent_history()
for log in history_logs:
    st.sidebar.caption(f"⏱️ {log[2]} \n {log[0]} ➔ {log[1]}")
