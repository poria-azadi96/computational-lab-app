import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import os

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Computational Laboratory", layout="wide")
st.title("آزمایشگاه محاسباتی زیست‌شناسی نظری")

# --- HELPER FUNCTION TO READ TEXT FROM GITHUB PATHS ---
def load_tutorial_text(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    return "### خطا: فایل متنی این آموزش در مسیر مورد نظر یافت نشد."

# --- SIDEBAR CHAPTER SELECTION ---
st.sidebar.title("فهرست فصول آموزشی")
chapter = st.sidebar.selectbox(
    "انتخاب فصل جهت مطالعه و شبیه‌سازی:",
    [
        "بخش ۵: آزمایشگاه محاسباتی روی موبایل",
        "بخش ۶: نظریه مونتاژ (Assembly Theory)",
        "بخش ۷: دودکش‌های هیدروترمال اعماق دریا",
        "بخش ۸: جهان لیپیدی و مدل GARD"
    ]
)

# =========================================================================
# CHAPTER 5: MOBILE SIMULATION LAB
# =========================================================================
if chapter == "بخش ۵: آزمایشگاه محاسباتی روی موبایل":
    # 1. Load and render markdown text from local folder
    txt_path = "tutorials/1. Origin of Life/5. Mobile Simulation Lab/text.md"
    st.markdown(load_tutorial_text(txt_path))
    
    # 2. Render embedded native test script right below the text
    st.markdown("---")
    st.markdown("### باکس کدهای تست بستر محاسباتی موبایل")
    st.code('''# Verification script for mobile environment testing
import numpy as np
import scipy
import matplotlib

print("Checking native environment inside Android Ubuntu...")
print(f"NumPy Version: {np.__version__}")
print(f"SciPy Version: {scipy.__version__}")
print("Native environment setup is 100% successful!")''', language="python")

# =========================================================================
# CHAPTER 6: ASSEMBLY THEORY
# =========================================================================
elif chapter == "بخش ۶: نظریه مونتاژ (Assembly Theory)":
    # 1. Load and render markdown text
    txt_path = "tutorials/1. Origin of Life/6. Assembly Theory/text.md"
    st.markdown(load_tutorial_text(txt_path))
    
    # 2. Interactive Assembly Index Simulation Module
    st.markdown("---")
    st.markdown("### 🖥️ ابزار سنجش زنده شاخص مونتاژ")
    
    def calculate_assembly_index(target_string):
        pool = set(target_string)
        steps = len(pool)
        memory = list(pool)
        i = 0
        while i < len(target_string):
            matched = False
            for length in range(len(target_string) - i, 0, -1):
                substring = target_string[i:i+length]
                if substring in memory:
                    steps += 1
                    i += length
                    matched = True
                    break
            if not matched:
                steps += 1
                i += 1
            if i < len(target_string):
                memory.append(target_string[:i])
        return steps

    user_sequence = st.text_input("توالی مولکولی را وارد کنید:", "XGTYXGTYXGTY")
    if user_sequence:
        idx_result = calculate_assembly_index(user_sequence)
        c1, c2 = st.columns(2)
        c1.metric("شاخص مونتاژ محاسبه شده", idx_result)
        c2.metric("طول کل توالی", len(user_sequence))
        
        if idx_result > 15:
            st.success("شاخص بالاتر از ۱۵: ساختار از مرز شیمی غیرزنده عبور کرده و نشان‌دهنده فرگشتی فعال است.")
        else:
            st.info("شاخص کمتر یا مساوی ۱۵: ساختار در محدوده احتمالات شیمیایی پیش‌زیستی قرار دارد.")

# =========================================================================
# CHAPTER 7: HYDROTHERMAL VENTS
# =========================================================================
elif chapter == "بخش ۷: دودکش‌های هیدروترمال اعماق دریا":
    # 1. Load and render markdown text
    txt_path = "tutorials/1. Origin of Life/7. Hydrothermal Vents/text.md"
    st.markdown(load_tutorial_text(txt_path))
    
    # 2. Thermophoresis Particle Dynamics Simulation
    st.markdown("---")
    st.markdown("### 🖥️ شبیه‌ساز پویایی ذرات در ریزحفره‌های معدنی")
    
    drift = st.slider("شدت رانش ترموفورز (Soret Factor)", 0.0, 1.0, 0.3, 0.05)
    noise = st.slider("نویز ناشی از حرکت برآونی مولکولی", 0.1, 2.0, 1.0, 0.1)
    
    # Stochastic particle calculation loop
    x_positions = np.random.uniform(0, 100, 500)
    history = []
    for _ in range(200):
        x_positions += np.random.normal(0, noise, 500) + drift
        x_positions = np.clip(x_positions, 0, 100)
        trapped = np.sum(x_positions > 80)
        history.append((trapped / 500) * 100)
        
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    ax.plot(history, color='#00ffff', linewidth=2)
    ax.set_title("نمودار تجمع مولکولی در منطقه سرد حفره سنگی", color='white')
    ax.set_xlabel("گام‌های زمانی", color='white')
    ax.set_ylabel("درصد تمرکز ذرات در تله غلظتی", color='white')
    ax.grid(alpha=0.2, linestyle='--')
    ax.tick_params(colors='white')
    st.pyplot(fig)

# =========================================================================
# CHAPTER 8: LIPID WORLD AND GARD MODEL
# =========================================================================
elif chapter == "بخش ۸: جهان لیپیدی و مدل GARD":
    # 1. Load and render markdown text
    txt_path = "tutorials/1. Origin of Life/8. Lipid World/text.md"
    st.markdown(load_tutorial_text(txt_path))
    
    # 2. GARD Compositional Network Solver
    st.markdown("---")
    st.markdown("### 🖥️ داشبورد محاسباتی مدل غشایی GARD")
    
    n_max = st.slider("آستانه حجم بحرانی تقسیم فیزیکی (N_MAX)", 50, 200, 100, 10)
    n_types = st.slider("تعداد گونه‌های شیمیایی غشا", 3, 10, 5, 1)
    
    # Run dynamic vector loop
    np.random.seed(42)
    beta = np.random.uniform(0.1, 5.0, (n_types, n_types))
    rho = np.ones(n_types) * 2.5
    n = np.random.randint(2, 8, n_types).astype(float)
    gard_history = []
    fissions = []
    
    for step in range(2000):
        N = np.sum(n)
        if N <= 0:
            break
        catalysis = 1.0 + np.dot(beta, n / N)
        dn = (0.10 * rho - 0.20 * n) * catalysis * 0.01
        n += dn
        n = np.maximum(n, 0.0)
        if np.sum(n) >= n_max:
            n = np.random.multinomial(int(n_max / 2), n / np.sum(n)).astype(float)
            fissions.append(step)
        gard_history.append(n.copy())
        
    gard_history = np.array(gard_history)
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    for i in range(n_types):
        ax.plot(gard_history[:, i], label=f'Lipid {i+1}')
    for f in fissions:
        ax.axvline(x=f, color='gray', linestyle='--', alpha=0.4)
    ax.legend(facecolor='#0e1117', labelcolor='white')
    ax.grid(alpha=0.2)
    ax.tick_params(colors='white')
    st.pyplot(fig)
    st.info(f"تعداد چرخه‌های موفق تکثیر خودکاتالیزوری غشا: {len(fissions)}")
