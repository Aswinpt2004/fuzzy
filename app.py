# app.py
from flask import Flask, render_template, request, url_for, jsonify
from dotenv import load_dotenv
import os
import numpy as np
from modules import fuzzy_sets, fuzzy_membership
from utils.llm_explainer import explain_with_llm

# Load environment variables
load_dotenv()

app = Flask(__name__)


# Cache-busting helper for static assets: appends file mtime as v= query
@app.context_processor
def asset_helper():
    import os
    def asset(path: str):
        try:
            full_path = os.path.join(app.root_path, 'static', path.replace('/', os.sep))
            v = int(os.stat(full_path).st_mtime)
        except Exception:
            v = 0
        return url_for('static', filename=path, v=v)
    return dict(asset=asset)


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
        apply_to = request.form.get("apply_to", "A")

        labelsA, A = fuzzy_sets.parse_fuzzy(A_str)
        labelsB, B = fuzzy_sets.parse_fuzzy(B_str)

        try:
            # --- Perform operation ---
            # Determine target for single-set operations (A or B)
            target = A if apply_to == "A" else B

            if operation == "Equality":
                result = fuzzy_sets.equality(A, B)
            elif operation == "Complement":
                result = fuzzy_sets.complement(target)
            elif operation == "Intersection":
                result = fuzzy_sets.intersection(A, B)
            elif operation == "Union":
                result = fuzzy_sets.union(A, B)
            elif operation == "Algebraic Product":
                result = fuzzy_sets.algebraic_product(A, B)
            elif operation == "Multiplication by Crisp Number":
                # default crisp multiplier 0.5; applies to selected set
                result = fuzzy_sets.crisp_multiply(target, 0.5)
            elif operation == "Power of Fuzzy Set":
                # default exponent 2; applies to selected set
                result = fuzzy_sets.power(target, 2)
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

            # If a single-set operation was applied to B, prefer B's labels for plotting
            labels = labelsA if apply_to == "A" else labelsB
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

   

@app.route("/relations", methods=["GET", "POST"])
def relations():
    import numpy as np
    from modules import fuzzy_relations

    rows = 3
    cols = 3
    R = np.zeros((rows, cols))
    S = np.zeros((cols, rows))
    T = None
    mode = "Random"
    comp_type = "Max-Min"
    explanation = None

    props_R = None
    props_T = None

    if request.method == "POST":
        mode = request.form.get("mode", "Random")
        comp_type = request.form.get("composition", "Max-Min")
        rows = int(request.form.get("rows", 3))
        cols = int(request.form.get("cols", 3))

        if mode == "Random":
            R = fuzzy_relations.random_relation(rows, cols)
            S = fuzzy_relations.random_relation(cols, rows)
        else:
            # Manual: parse numeric grid entries instead of eval()
            try:
                R = np.zeros((rows, cols))
                S = np.zeros((cols, rows))
                for i in range(rows):
                    for j in range(cols):
                        R[i, j] = float(request.form.get(f"R_{i}_{j}", 0))
                for i in range(cols):
                    for j in range(rows):
                        S[i, j] = float(request.form.get(f"S_{i}_{j}", 0))
            except Exception as e:
                explanation = f"⚠️ Invalid entry: {e}"

        # Compute composition
        try:
            if comp_type == "Max-Min":
                T = fuzzy_relations.max_min_composition(R, S)
            else:
                T = fuzzy_relations.max_product_composition(R, S)
        except Exception as e:
            explanation = f"⚠️ Composition error: {e}"

        # Property checks (only applicable for square relations)
        try:
            props_R = fuzzy_relations.check_all_properties(R, comp_type)
        except Exception:
            props_R = None
        try:
            if T is not None:
                props_T = fuzzy_relations.check_all_properties(T, comp_type)
        except Exception:
            props_T = None

        # Gemini explanation
        if "explain" in request.form:
            explanation = explain_with_llm(
                "Fuzzy Relation Composition",
                f"R(x,y): {R.tolist()}, S(y,z): {S.tolist()}",
                f"Composition Type: {comp_type}",
                f"Result: {T.tolist() if T is not None else 'N/A'}"
            )

    return render_template(
        "relations.html",
        R=R.tolist(),
        S=S.tolist(),
        T=T.tolist() if T is not None else None,
        rows=rows,
        cols=cols,
        mode=mode,
        comp_type=comp_type,
        props_R=props_R,
        props_T=props_T,
        explanation=explanation
    )


# ================================
# 🔗 Fuzzy Implications Page
# ================================
@app.route("/implications", methods=["GET", "POST"])
def implications():
    from modules import fuzzy_implications
    
    result = None
    labels_A = []
    labels_B = []
    implication_type = None
    explanation = None
    
    if request.method == "POST":
        A_str = request.form.get("setA")
        B_str = request.form.get("setB")
        implication = request.form.get("implication", "mamdani")
        
        # Parse fuzzy sets
        labels_A, A = fuzzy_sets.parse_fuzzy(A_str)
        labels_B, B = fuzzy_sets.parse_fuzzy(B_str)
        
        # Get implication method
        impl_func = fuzzy_implications.get_implication_method(implication)
        result = impl_func(A, B)
        implication_type = implication.capitalize()
        
        # Explanation
        if "explain" in request.form:
            params = {
                'antecedent_A': A_str,
                'consequent_B': B_str,
                'operator': implication_type
            }
            context = "Fuzzy Implication"
            prompt = f"""
            Antecedent Set A: {A_str}
            Consequent Set B: {B_str}
            Implication Operator: {implication_type}
            
            Explain how the {implication_type} implication operator works and show the computation.
            """
            explanation = explain_with_llm(context, implication_type, params, prompt)
    
    return render_template(
        "implictaion.html",
        result=result.tolist() if result is not None else None,
        labels_A=labels_A,
        labels_B=labels_B,
        implication_type=implication_type,
        explanation=explanation
    )


@app.route("/fis", methods=["GET", "POST"])
def fis():
    from modules import fuzzy_implications, defuzzification
    
    aggregated_output = None
    crisp_output = None
    output_labels = []
    defuzz_method = None
    explanation = None
    lambda_value = None
    
    if request.method == "POST":
        input_str = request.form.get("input_set")
        output_str = request.form.get("output_set")
        inference_method = request.form.get("inference_method", "mamdani")
        defuzz_method = request.form.get("defuzz_method", "centroid")
        lambda_value = request.form.get("lambda_value", type=float)
        
        # Parse sets
        input_labels, input_values = fuzzy_sets.parse_fuzzy(input_str)
        output_labels, output_values = fuzzy_sets.parse_fuzzy(output_str)
        
        # Simple inference: use implication to generate output
        # For demonstration, we'll use the input values as the aggregated output
        # In a real FIS, you'd apply rules here
        impl_func = fuzzy_implications.get_implication_method(inference_method)
        
        # Aggregate (for demo, just copy input to output space)
        aggregated_output = input_values[:len(output_values)]
        if len(aggregated_output) < len(output_values):
            aggregated_output = np.pad(aggregated_output, (0, len(output_values) - len(aggregated_output)))
        
        # Defuzzification
        # Create numeric universe for defuzzification
        y = np.arange(len(output_labels))
        
        # Handle lambda-cut defuzzification specially
        if defuzz_method == 'lambda_cut':
            if lambda_value is None:
                lambda_value = 0.5  # Default
            crisp_output = defuzzification.lambda_cut_defuzzification(y, aggregated_output, lambda_value)
        else:
            defuzz_func = defuzzification.get_defuzzification_method(defuzz_method)
            crisp_output = defuzz_func(y, aggregated_output)
        
        # Explanation
        if "explain" in request.form:
            params = {
                'input_set': input_str,
                'inference_method': inference_method,
                'defuzzification_method': defuzz_method,
                'crisp_output': crisp_output
            }
            context = "Fuzzy Inference System"
            prompt = f"""
            Input Set: {input_str}
            Inference Method: {inference_method}
            Defuzzification Method: {defuzz_method}
            Crisp Output: {crisp_output:.3f}
            
            Explain the fuzzy inference process and how the crisp output was calculated.
            """
            explanation = explain_with_llm(context, "FIS", params, prompt)
    
    return render_template(
        "fis.html",
        aggregated_output=aggregated_output.tolist() if aggregated_output is not None else None,
        crisp_output=crisp_output,
        output_labels=output_labels,
        defuzz_method=defuzz_method,
        inference_method=inference_method if request.method == "POST" else None,
        aggregation=request.form.get("aggregation", "maximum") if request.method == "POST" else None,
        num_rules=1,  # Update this when implementing actual rule parsing
        lambda_value=lambda_value,
        explanation=explanation,
        zip=zip  # Make zip available in template
    )


if __name__ == "__main__":
    app.run(debug=True)
