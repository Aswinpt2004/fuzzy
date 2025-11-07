# FIS System — Detailed Overview

Date: November 6, 2025
Path: D:\fuzzy

Purpose
-------
This document explains how the Fuzzy Inference System (FIS) in this repository works end-to-end, how it was implemented, which options are available in the UI and backend, and where to extend it. Use this as a developer-facing reference and quick onboarding guide.

High-level flow
---------------
The FIS follows the classical pipeline:

1. Fuzzification — map crisp inputs into membership degrees across linguistic terms.
2. Rule Evaluation — for each rule, compute antecedent matching degrees and rule strength (apply T-norms for AND, S-norms for OR where supported).
3. Implication — transform antecedent truth to consequent fuzzy sets (Mamdani, Larsen, etc.).
4. Aggregation — combine all rule fuzzy outputs into a single aggregated fuzzy set over the output universe.
5. Defuzzification — convert the aggregated fuzzy set to a crisp value by selected method (CoG, CoS, CoA, maxima methods, lambda-cut, etc.).
6. Explanation (optional) — generate an AI/templated summary of the reasoning steps.

Files & Modules
----------------
Key source locations (relative to repo root):

- `app.py` — Flask routes and glue code (front controller). Main `/fis` route handles the form submission and orchestration.
- `templates/fis.html` — Rule builder UI, inference controls, plotting for aggregated result, and AI explanation button.
- `modules/fuzzy_membership.py` — Membership function definitions and helpers.
- `modules/fuzzy_rules.py` — Rule and rulebase classes and parsing utilities (rule objects, evaluation scaffolding).
- `modules/fuzzy_tnorms.py` — T-norms (AND) and S-norms (OR) implementations and selection helpers.
- `modules/fuzzy_implications.py` — Implication operators (Mamdani, Larsen, Zadeh, Reichenbach, Goguen/...); `get_implication_method()` exposes functions.
- `modules/defuzzification.py` — All defuzzification implementations: centroid methods, maxima methods, height, lambda-cut and helpers.
- `static/js/*` — UI scripts for the FIS: dynamic rule builder (`fis.html` embedded JS), plotting via Plotly.
- `utils/llm_explainer.py` — LLM-based explanatory text generator (`explain_with_llm()`).

Implementation details and data shapes
-------------------------------------
This section documents how the components expect data and what shapes they return.

1) Fuzzification
- Input: user-provided `input_set` string (example form: `(low,0.2),(medium,0.5),(high,0.3)`).
- Parsing: `modules/fuzzy_sets.parse_fuzzy()` (used by `app.py`) returns `(labels, values)` where `labels` is a list of linguistic names and `values` a numeric list of membership degrees.
- Result: `input_labels` and `input_values` (both lists). The UI expects the input field `input_set`.

2) Rule representation (UI -> form fields)
- Each rule in the UI produces form inputs named using the pattern `rule_N_field` where N is index (0-based) and `field` is one of:
  - `type`: `if-then` or `if-then-else` (new)
  - `antecedent`: linguistic antecedent (string)
  - `consequent`: linguistic consequent (string)
  - `else_consequent`: alternative consequent when rule type is `if-then-else`
  - `weight`: numeric 0..1
- Example names: `rule_0_antecedent`, `rule_0_consequent`, `rule_0_weight`, `rule_0_type`, `rule_0_else_consequent`.
- Backend (future work): parsing these fields into `FuzzyRule` objects in `modules/fuzzy_rules.py` is recommended (currently UI fields are available but full parsing/usage is partially implemented).

3) Rule evaluation & T-norms
- Antecedent degree lookup: For demo, `app.py` uses fuzzy input values directly. Full evaluation should map antecedent linguistic term name to a membership degree from `input_values`.
- T-norm selection (UI field `tnorm`) chooses how to combine multiple antecedents (minimum, product, bounded, drastic). `modules/fuzzy_tnorms.get_tnorm()` should expose a function to combine a list of antecedent degrees.

4) Implication
- The selected `inference_method` (UI field) maps to an implication function via `fuzzy_implications.get_implication_method(name)`.
- Implication functions accept antecedent degree `a` and consequent membership `b` and produce an implication result per crisp consequent value or vector over the output universe.
- Common semantics:
  - Mamdani (min): μR = min(a, b)
  - Larsen (product): μR = a * b
  - Zadeh (logical): μR = max(1 - a, b)
  - Reichenbach/Goguen/bounded: other algebraic forms

5) Aggregation
- After implication, each rule contributes a fuzzy set over the output universe; aggregation combines those with methods selected by `aggregation` UI (maximum, sum, probabilistic sum, mean, etc.).
- Aggregation operates element-wise across the numeric arrays representing membership values for each output label.

6) Defuzzification
- Available options in UI (`defuzz_method`) include maxima methods (height, MoM, FoM, LoM), centroid methods (CoG, CoS, CoA), bisector, weighted average, and lambda-cut.
- Data passed: numeric `y` universe (in current `app.py` numeric universe is `np.arange(len(output_labels))`) and `aggregated_output` numeric array.
- Lambda-cut: special handling required — `lambda_value` param (0..1) used to alpha-trim the fuzzy set before defuzz.

Current behavior vs TODOs
-------------------------
What is implemented today (core, tested):
- Membership functions, implication operators, T-norms, defuzzification suite, fuzzy rules scaffolding, FIS UI with dynamic rule builder; Plotly visualizations.
- Implication plotting (now line plots per antecedent) and aggregated output plotting implemented in templates.

What is partially implemented or intentionally simplified:
- Full parsing and evaluation of rules created in the UI is not yet wired end-to-end. `app.py` currently demonstrates mapping input values onto output values for demo purposes and does not yet evaluate arbitrary rule expressions, multi-input expressions, or IF–THEN–ELSE semantics fully.
- Suggested extension: move parsing and rule evaluation into `modules/fuzzy_rules.py` such that `app.py` constructs a `FuzzyRuleBase` from form fields and executes it against `input_values`.

UI fields (summary)
-------------------
- `input_set` — fuzzified input string.
- `output_set` — output linguistic terms.
- `rule_N_type` — `if-then` or `if-then-else`.
- `rule_N_antecedent` — antecedent linguistic term.
- `rule_N_consequent` — consequent linguistic term.
- `rule_N_else_consequent` — else consequent (if rule type is if-then-else).
- `rule_N_weight` — rule weight (0..1).
- `inference_method` — chosen implication operator (`mamdani`, `larsen`, `zadeh`, ...).
- `tnorm` — conjunction operator for multi-input rules (`minimum`, `product`, `bounded`, `drastic`).
- `aggregation` — method for combining rule outputs (`maximum`, `sum`, `probsum`, `mean`).
- `defuzz_method` — defuzzification method.
- `lambda_value` — for lambda-cut defuzzification.

Suggested IF–THEN–ELSE semantics (implementations)
-------------------------------------------------
We added UI support for IF–THEN–ELSE rules. There are two reasonable behaviors to implement on the backend:

A) Deterministic threshold behavior (simple):
- If antecedent degree >= threshold (e.g., 0.5) → apply THEN consequence.
- Else → apply ELSE consequence.
- Good for crisp fallback behavior.

B) Weighted blending (smooth):
- THEN contribution weight = antecedent_degree * rule_weight
- ELSE contribution weight = (1 - antecedent_degree) * rule_weight
- Combine both contributions into aggregation (this allows partial activation and a more continuous mapping)
- This design aligns with fuzzy logic principles and is recommended if you want smoother transitions.

How to wire an IF–THEN–ELSE rule in code (sketch)
-------------------------------------------------
- Map antecedent linguistic term to degree `a` from `input_values`.
- Map consequent linguistic term to consequent membership vector `b` over numeric output universe (convert linguistic term to membership function shape or one-hot membership if using term labels only).
- For `if-then`: implication_result = implication(a, b) (vector)
- For `if-then-else` using weighted blending: implication_then = implication(a, b_then); implication_else = implication(1 - a, b_else); final_contribution = rule_weight * (implication_then + implication_else)
- Aggregate across all rules.

Testing and verification
------------------------
- Use `test_modules.py` to verify individual module imports and basic functions. The file already contains tests for `fuzzy_implications` and more — run it in the project virtualenv.
- Unit tests to add:
  - Parser tests for `input_set` and `output_set` parsing.
  - Rule parsing tests: construct forms simulating multiple rules and ensure `FuzzyRuleBase` correctly represents them.
  - IF–THEN–ELSE semantics tests for deterministic and weighted modes.
  - End-to-end integration test: given an `input_set`, a set of rules, inference & aggregation method, and defuzzification method — assert expected crisp output.

How to run (dev)
-----------------
Activate the venv and run Flask from project root (Windows PowerShell):

```powershell
& D:/fuzzy/fuzzy/Scripts/Activate.ps1
python app.py
```

Open http://127.0.0.1:5000/fis and use the Rule Builder.

Notes & limitations
-------------------
- `app.py` currently contains a simplified demo inference pipeline. The UI now collects full rule information but the server must be extended to parse and evaluate rules end-to-end.
- Some modules (e.g., `modules/fuzzy_fis.py`) were removed because they required external dependencies (`skfuzzy`) and were unused; the current modules are self-contained.
- LLM explanation depends on having correct API keys and model access in `utils/llm_explainer.py`.

Developer action plan (recommended next steps)
---------------------------------------------
1. Implement rule parsing: add a `parse_rules_from_form(form)` helper in `modules/fuzzy_rules.py` that returns a `FuzzyRuleBase` containing rule objects with fields: antecedent_name(s), consequent_name(s), else_consequent, weight, type.
2. Evaluate rules: add an evaluation method that accepts `input_labels`, `input_values`, `output_labels`, `output_universe` and returns per-rule contribution arrays.
3. Support multi-input rules: extend antecedent parsing and T-norm evaluation to support multiple antecedents per rule.
4. Implement IF–THEN–ELSE semantics (weighted blending) as default behavior.
5. Add unit tests and integration tests, then wire explanation outputs to include which rules used THEN vs ELSE and their strengths.
6. Add optional UI toggle to switch aggregated view between heatmap and line plots (already changed for implications; FIS output currently uses bar + crisp line).

Appendix: Example end-to-end sketch (pseudocode)
-----------------------------------------------
```python
# parse
rules = parse_rules_from_form(request.form)
# evaluate
contributions = []
for rule in rules:
    a = get_antecedent_degree(rule.antecedent, input_labels, input_values)
    b_then = get_consequent_vector(rule.consequent, output_labels)
    if rule.type == 'if-then':
        contrib = implication_func(a, b_then) * rule.weight
    else: # if-then-else
        b_else = get_consequent_vector(rule.else_consequent, output_labels)
        contrib_then = implication_func(a, b_then) * rule.weight
        contrib_else = implication_func(1 - a, b_else) * rule.weight
        contrib = contrib_then + contrib_else
    contributions.append(contrib)
# aggregate
aggregated = aggregate(contributions, method=aggregation)
# defuzzify
crisp = defuzzification.get_defuzzification_method(defuzz_method)(y_universe, aggregated)
```

Contact/notes
-------------
If you want, I can now implement step 1 and 2 (rule parsing and evaluation) with weighted IF–THEN–ELSE semantics and unit tests. I will:

- Update `modules/fuzzy_rules.py` to parse and represent rules.
- Update `app.py` to use parsed rules for inference rather than the current demo mapping.
- Add 3 unit tests to `test_modules.py` for parsing, evaluation, and IF–THEN–ELSE behavior.

I left this task in the todo list as `Produce FIS system detailed report` (in-progress); I'll mark it completed after you confirm you want the content saved and/or want me to implement the parsing/evaluation next.

---

End of FIS System Report
