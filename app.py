# app.py
from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import numpy as np
from modules import fuzzy_sets
from utils.llm_explainer import explain_with_llm
from modules import fuzzy_membership
from flask import jsonify
from flask import jsonify, request

# Load environment variables
load_dotenv()

app = Flask(__name__)


# 🏠 Home route
@app.route("/")
def home():
    return render_template("index.html")


# ================================
# 🧩 Fuzzy Set Operations Page
# ================================
@app.route("/sets", methods=["GET", "POST"])
def fuzzy_sets_page():
    result = None
    labels = []
    operation = None
    explanation = None
    chart_type = "line"
    A_plot, B_plot = [], []

    if request.method == "POST":
        A_str = request.form.get("setA")
        B_str = request.form.get("setB")
        operation = request.form.get("operation")

        labelsA, A = fuzzy_sets.parse_fuzzy(A_str)
        labelsB, B = fuzzy_sets.parse_fuzzy(B_str)

        try:
            # --- Perform operation ---
            if operation == "Equality":
                result = fuzzy_sets.equality(A, B)
            elif operation == "Complement":
                result = fuzzy_sets.complement(A)
            elif operation == "Intersection":
                result = fuzzy_sets.intersection(A, B)
            elif operation == "Union":
                result = fuzzy_sets.union(A, B)
            elif operation == "Algebraic Product":
                result = fuzzy_sets.algebraic_product(A, B)
            elif operation == "Multiplication by Crisp Number":
                result = fuzzy_sets.crisp_multiply(A, 0.5)
            elif operation == "Power of Fuzzy Set":
                result = fuzzy_sets.power(A, 2)
            elif operation == "Algebraic Sum":
                result = fuzzy_sets.algebraic_sum(A, B)
            elif operation == "Algebraic Difference":
                result = fuzzy_sets.algebraic_difference(A, B)
            elif operation == "Bounded Sum":
                result = fuzzy_sets.bounded_sum(A, B)
            elif operation == "Bounded Difference":
                result = fuzzy_sets.bounded_difference(A, B)
            elif operation == "Cartesian Product":
                result = fuzzy_sets.cartesian_product(A, B)
                chart_type = "heatmap"
            elif operation == "Composition":
                R = fuzzy_sets.cartesian_product(A, B)
                S = fuzzy_sets.cartesian_product(B, A)
                result = fuzzy_sets.composition(R, S)
                chart_type = "heatmap"
            else:
                result = np.zeros_like(A)

            # LLM explanation
            if "explain" in request.form:
                explanation = explain_with_llm(
                    operation,
                    A.tolist() if hasattr(A, "tolist") else A,
                    B.tolist() if hasattr(B, "tolist") else B,
                    result.tolist() if hasattr(result, "tolist") else result,
                )

            labels = labelsA or labelsB
            A_plot = A.tolist()
            B_plot = B.tolist()

        except Exception as e:
            explanation = f"⚠️ Error: {e}"

    # --- Safe conversion ---
    def safe_to_list(x):
        try:
            return x.tolist()
        except Exception:
            return x

    return render_template(
        "fuzzy_sets.html",
        result=safe_to_list(result),
        labels=safe_to_list(labels),
        A=A_plot,
        B=B_plot,
        operation=operation,
        explanation=explanation,
        chart_type=chart_type,
    )


# ================================
# Other Placeholder Routes
# ================================
@app.route("/membership", methods=["GET", "POST"])
def membership():
    x = np.linspace(0, 10, 300)
    y = np.zeros_like(x)
    mf_type = "Triangular"
    params = []
    explanation = None

    if request.method == "POST":
        mf_type = request.form.get("mf_type")

        try:
            param_values = [float(p.strip()) for p in request.form.get("params").split(",")]

            if mf_type == "Triangular":
                y = fuzzy_membership.triangular(x, *param_values)
            elif mf_type == "Trapezoidal":
                y = fuzzy_membership.trapezoidal(x, *param_values)
            elif mf_type == "Gaussian":
                y = fuzzy_membership.gaussian(x, *param_values)
            elif mf_type == "Bell":
                y = fuzzy_membership.bell_shaped(x, *param_values)
            elif mf_type == "Sigmoid":
                y = fuzzy_membership.sigmoid(x, *param_values)
            else:
                y = np.zeros_like(x)

            params = param_values

            if "explain" in request.form:
                explanation = explain_with_llm(
                    f"{mf_type} Membership Function",
                    f"Parameters: {params}",
                    "Domain: 0–10",
                    f"Output: {y.tolist()[:10]}..."
                )

        except Exception as e:
            explanation = f"⚠️ Error: {e}"

    return render_template(
        "membership.html",
        x=x.tolist(),
        y=y.tolist(),
        mf_type=mf_type,
        params=params,
        explanation=explanation
    )


# ================================
# 🧩 API: Membership Function JSON
# ================================
@app.route("/api/membership", methods=["POST"])
def api_membership():
    data = request.get_json()
    mf_type = data.get("mf_type")
    params = data.get("params", [])
    x = np.linspace(0, 10, 300)

    try:
        if mf_type == "Triangular":
            y = fuzzy_membership.triangular(x, *params)
        elif mf_type == "Trapezoidal":
            y = fuzzy_membership.trapezoidal(x, *params)
        elif mf_type == "Gaussian":
            y = fuzzy_membership.gaussian(x, *params)
        elif mf_type == "Bell":
                y = fuzzy_membership.bell_shaped(x, *params)
        elif mf_type == "Sigmoid":
                y = fuzzy_membership.sigmoid(x, *params)
        else:
            y = np.zeros_like(x)

        return jsonify({"x": x.tolist(), "y": y.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/membership/explain", methods=["POST"])
def api_membership_explain():
    """Generate LLM explanation for the current MF."""
    data = request.get_json()
    mf_type = data.get("mf_type")
    params = data.get("params", [])
    prompt = f"""
    Explain this fuzzy membership function type and its parameters.
    Type: {mf_type}
    Parameters: {params}
    Domain: 0–10
    Describe its mathematical formula, how the parameters affect the shape,
    and a simple real-world example.
    """

    try:
        response = explain_with_llm("Membership Function", mf_type, params, prompt)
        return jsonify({"explanation": response})
    except Exception as e:
        return jsonify({"explanation": f"⚠️ Error: {e}"}), 500

   

@app.route("/relations")
def relations():
    return render_template("relations.html")

@app.route("/implications")
def implications():
    return render_template("implications.html")

@app.route("/fis")
def fis():
    return render_template("fis.html")


if __name__ == "__main__":
    app.run(debug=True)
