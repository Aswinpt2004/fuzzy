# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from utils.llm_explainer import explain_with_llm

# Page config
st.set_page_config(page_title="Soft Computing Fuzzy Toolbox", layout="wide")

st.title("🧠 Soft Computing Fuzzy Logic Toolbox (Web Edition)")
st.caption("A web-based intelligent fuzzy logic toolbox with explainable AI integration.")

# Sidebar navigation
page = st.sidebar.radio(
    "Navigate to:",
    [
        "Home",
        "Fuzzy Set Operations",
        "Membership Function Editor",
        "Fuzzy Relations & Composition",
        "Fuzzy Implications & Rule Base",
        "Fuzzy Inference & Defuzzification"
    ]
)

# ---------------- HOME ----------------
if page == "Home":
    st.markdown("""
    ### 👋 Welcome to the Soft Computing Fuzzy Toolbox (Web Version)
    This toolbox allows you to:
    - Perform all fuzzy set operations
    - Design and visualize membership functions
    - Compute fuzzy relations and implications
    - Build fuzzy rule bases and inference systems
    - Perform **defuzzification**
    - Get instant **AI explanations** for each computation using an integrated LLM API

    ---
    **Developed by:** Navaras P  
    **Institution:** Kerala University of Digital Sciences  
    **Powered by:** Streamlit + OpenAI GPT  
    ---
    """)

# ---------------- FUZZY SET OPERATIONS ----------------
elif page == "Fuzzy Set Operations":
    st.header("🧩 Fuzzy Set Operations")

    st.write("### Enter Fuzzy Sets Manually")
    A_str = st.text_input("Set A:", "(x1,0.5),(x2,0.3),(x3,0.7)")
    B_str = st.text_input("Set B:", "(x1,0.4),(x2,0.6),(x3,0.5)")
    operation = st.selectbox(
        "Select Operation",
        [
            "Union", "Intersection", "Complement",
            "Algebraic Product", "Algebraic Sum",
            "Bounded Sum", "Bounded Difference",
            "Crisp Multiplication", "Power"
        ]
    )

    if st.button("Compute"):
        try:
            # Parse fuzzy sets
            def parse_fuzzy_set(text):
                pairs = text.replace("{", "").replace("}", "").split(")")
                data = {}
                for p in pairs:
                    if "(" in p:
                        vals = p.strip(" ,(").split(",")
                        if len(vals) == 2:
                            data[vals[0]] = float(vals[1])
                return list(data.keys()), np.array(list(data.values()))

            labelsA, A = parse_fuzzy_set(A_str)
            labelsB, B = parse_fuzzy_set(B_str)

            # Compute basic fuzzy operations
            if operation == "Union":
                result = np.fmax(A, B)
            elif operation == "Intersection":
                result = np.fmin(A, B)
            elif operation == "Complement":
                result = 1 - A
            elif operation == "Algebraic Product":
                result = A * B
            elif operation == "Algebraic Sum":
                result = np.clip(A + B - (A * B), 0, 1)
            elif operation == "Bounded Sum":
                result = np.clip(A + B, 0, 1)
            elif operation == "Bounded Difference":
                result = np.clip(A - B, 0, 1)
            elif operation == "Crisp Multiplication":
                result = np.clip(A * 0.5, 0, 1)
            elif operation == "Power":
                result = np.clip(A ** 2, 0, 1)
            else:
                result = np.zeros_like(A)

            # Display result
            st.success(f"**Result ({operation})**: {np.round(result, 3)}")

            # Plot result
            fig, ax = plt.subplots()
            x = np.arange(len(A))
            bar_width = 0.25
            ax.bar(x - bar_width, A, width=bar_width, label="A", color="blue")
            ax.bar(x, B, width=bar_width, label="B", color="orange")
            ax.bar(x + bar_width, result, width=bar_width, label="Result", color="green")
            ax.set_xticks(x)
            ax.set_xticklabels(labelsA)
            ax.set_ylim(0, 1.05)
            ax.legend()
            st.pyplot(fig)

            # Explain Button
            if st.button("🧠 Explain This Operation"):
                with st.spinner("Generating explanation..."):
                    explanation = explain_with_llm(operation, A, B, result)
                    st.markdown(explanation)

        except Exception as e:
            st.error(f"Error: {e}")

# ---------------- MEMBERSHIP FUNCTION EDITOR ----------------
elif page == "Membership Function Editor":
    st.header("📈 Membership Function Editor (Triangular, Trapezoidal, Gaussian)")
    st.info("Coming next — sliders to define and visualize membership functions interactively.")

# ---------------- RELATIONS ----------------
elif page == "Fuzzy Relations & Composition":
    st.header("🔗 Fuzzy Relations & Composition")
    st.info("This module will visualize fuzzy relation matrices and perform Max–Min compositions.")

# ---------------- IMPLICATIONS ----------------
elif page == "Fuzzy Implications & Rule Base":
    st.header("⚙️ Fuzzy Implications & Rule Base")
    st.info("This section will let you build rule bases like 'IF temp is high THEN fan speed is fast'.")

# ---------------- FIS + DEFUZZIFICATION ----------------
elif page == "Fuzzy Inference & Defuzzification":
    st.header("🧠 Fuzzy Inference & Defuzzification")
    st.info("This will handle the full Mamdani FIS process including defuzzification methods (centroid, bisector, etc.).")
