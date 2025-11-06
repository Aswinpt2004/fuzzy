# 🧠 Fuzzy Logic Toolbox - Complete Documentation

> **A professional web-based fuzzy logic system implementing fuzzy sets, relations, implications, inference, and defuzzification methods.**

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Module Reference](#module-reference)
4. [Mathematical Formulas](#mathematical-formulas)
5. [Installation & Setup](#installation--setup)
6. [Usage Guide](#usage-guide)
7. [API Reference](#api-reference)
8. [Testing](#testing)

---

## 🎯 Overview

This toolbox provides a complete implementation of fuzzy logic operations for:
- **Fuzzy Set Operations**: Complement, union, intersection, algebraic operations
- **Membership Functions**: Triangular, trapezoidal, Gaussian, bell-shaped, sigmoid
- **Fuzzy Relations**: Max-min and max-product composition with property checks
- **Fuzzy Implications**: Mamdani, Larsen, Zadeh, Reichenbach, Goguen operators
- **Fuzzy Inference**: Rule-based inference systems
- **Defuzzification**: Multiple methods for crisp output generation

### Key Features
✅ Professional black & white UI theme
✅ AI-powered explanations (Gemini integration)
✅ Real-time visualization with Plotly
✅ Property verification (reflexivity, symmetry, transitivity)
✅ Comprehensive mathematical operations
✅ RESTful API endpoints
✅ Cache-busted static assets

---

## 🏗️ Architecture

```
fuzzy/
├── app.py                    # Flask application & routes
├── instance/
│   └── config.py            # Configuration (API keys)
├── modules/                 # Core fuzzy logic modules
│   ├── fuzzy_sets.py       # Set operations
│   ├── fuzzy_membership.py  # Membership functions
│   ├── fuzzy_relations.py   # Relations & composition
│   ├── fuzzy_implications.py # Implication operators
│   ├── fuzzy_inference.py   # Inference engine
│   ├── fuzzy_algebra.py     # Algebraic operations
│   └── defuzzification.py   # Defuzzification methods
├── utils/
│   ├── llm_explainer.py    # AI explanation generator
│   └── parser.py           # Input parsing utilities
├── templates/              # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── fuzzy_sets.html
│   ├── membership.html
│   ├── relations.html
│   ├── implications.html
│   └── fis.html
├── static/
│   ├── css/
│   │   └── style.css       # Professional black/white theme
│   └── js/
│       ├── fuzzy_sets_ui.js
│       ├── membership.js
│       └── relations.js
└── fuzzy/                  # Virtual environment
```

---

## 📦 Module Reference

### 1. `modules/fuzzy_sets.py`

**Purpose**: Core fuzzy set operations

**Functions**:
- `parse_fuzzy(set_str)` → Parse fuzzy set from string format
- `equality(A, B)` → Check if two fuzzy sets are equal
- `complement(A)` → Fuzzy complement (1 - μ)
- `intersection(A, B)` → Min operation
- `union(A, B)` → Max operation
- `algebraic_product(A, B)` → μ_A × μ_B
- `algebraic_sum(A, B)` → μ_A + μ_B - μ_A×μ_B
- `bounded_sum(A, B)` → min(1, μ_A + μ_B)
- `bounded_difference(A, B)` → max(0, μ_A - μ_B)
- `power(A, p)` → (μ_A)^p
- `crisp_multiply(A, k)` → k × μ_A
- `cartesian_product(A, B)` → 2D relation matrix
- `composition(R, S)` → Max-min composition

---

### 2. `modules/fuzzy_membership.py`

**Purpose**: Membership function generators

**Functions**:
- `triangular(x, a, b, c)` → Triangular MF
- `trapezoidal(x, a, b, c, d)` → Trapezoidal MF
- `gaussian(x, mean, sigma)` → Gaussian MF
- `bell_shaped(x, a, b, c)` → Generalized bell MF
- `sigmoid(x, a, c)` → Sigmoid MF

**Parameters**:
- x: Domain values (numpy array)
- a, b, c, d: Shape parameters
- Returns: Membership values μ(x)

---

### 3. `modules/fuzzy_relations.py`

**Purpose**: Fuzzy relations and composition

**Functions**:
- `random_relation(rows, cols)` → Generate random relation
- `max_min_composition(R, S)` → T(x,z) = max_y(min(R(x,y), S(y,z)))
- `max_product_composition(R, S)` → T(x,z) = max_y(R(x,y) × S(y,z))
- `check_reflexivity(R)` → Verify R(x,x) = 1 ∀x
- `check_symmetry(R)` → Verify R(x,y) = R(y,x) ∀x,y
- `check_transitivity(R, comp_type)` → Verify R∘R ⊆ R
- `check_all_properties(R, comp_type)` → Combined check

**Returns**: Dict with `applicable`, boolean result, and numeric metrics

---

### 4. `modules/fuzzy_implications.py`

**Purpose**: Fuzzy implication operators for rule-based systems

**Functions**:

| Operator | Formula | Use Case |
|----------|---------|----------|
| `mamdani_implication(A, B)` | min(μ_A, μ_B) | Most common in FIS |
| `larsen_implication(A, B)` | μ_A × μ_B | Smooth control |
| `zadeh_implication(A, B)` | max(1-μ_A, μ_B) | Logical approach |
| `reichenbach_implication(A, B)` | 1-μ_A + μ_A×μ_B | Probabilistic |
| `goguen_implication(A, B)` | 1 if μ_A≤μ_B else μ_B/μ_A | Theoretical |

**Returns**: 2D numpy array R(x,y)

---

### 5. `modules/fuzzy_inference.py`

**Purpose**: Fuzzy inference engine

**Functions**:
- `apply_rules(fuzzified_inputs, rule_base, implication)` → Aggregate rule outputs
- `mamdani_inference(input_val, rules, mfs)` → Complete Mamdani FIS
- `larsen_inference(input_val, rules, mfs)` → Larsen-based FIS

**Process**:
1. Fuzzify crisp input
2. Apply each rule using selected implication
3. Aggregate outputs with max operator
4. Return fuzzy output set

---

### 6. `modules/defuzzification.py`

**Purpose**: Convert fuzzy output to crisp value

**Methods**:

| Method | Formula | Description |
|--------|---------|-------------|
| `centroid(y, μ)` | ∫yμ(y)dy / ∫μ(y)dy | Center of gravity (COG) |
| `bisector(y, μ)` | Split area 50-50 | Balance point |
| `mean_of_maxima(y, μ)` | avg(y where μ=max) | Mean of max (MOM) |
| `first_of_maxima(y, μ)` | min(y where μ=max) | First max (FOM) |
| `last_of_maxima(y, μ)` | max(y where μ=max) | Last max (LOM) |
| `weighted_average(y, μ)` | Σ(y_i × μ_i) / Σμ_i | Weighted avg |

---

### 7. `utils/llm_explainer.py`

**Purpose**: AI-powered step-by-step explanations

**Function**: `explain_with_llm(operation, *context)`

**Features**:
- Uses Google Gemini API
- Generates structured Markdown
- Preserves LaTeX math notation
- Returns HTML-safe output for MathJax

---

## 🔬 Mathematical Formulas

### Fuzzy Set Operations

**Complement**:
```
μ_A'(x) = 1 - μ_A(x)
```

**Intersection (Min)**:
```
μ_A∩B(x) = min(μ_A(x), μ_B(x))
```

**Union (Max)**:
```
μ_A∪B(x) = max(μ_A(x), μ_B(x))
```

**Algebraic Product**:
```
μ_A×B(x) = μ_A(x) × μ_B(x)
```

**Algebraic Sum**:
```
μ_A+B(x) = μ_A(x) + μ_B(x) - μ_A(x)×μ_B(x)
```

**Bounded Sum**:
```
μ_A⊕B(x) = min(1, μ_A(x) + μ_B(x))
```

**Bounded Difference**:
```
μ_A⊖B(x) = max(0, μ_A(x) - μ_B(x))
```

---

### Fuzzy Relations

**Max-Min Composition**:
```
T(x,z) = max_y [ min(R(x,y), S(y,z)) ]
```

**Max-Product Composition**:
```
T(x,z) = max_y [ R(x,y) × S(y,z) ]
```

**Reflexivity**: 
```
R is reflexive ⟺ R(x,x) = 1 ∀x
```

**Symmetry**:
```
R is symmetric ⟺ R(x,y) = R(y,x) ∀x,y
```

**Transitivity**:
```
R is transitive ⟺ R∘R ⊆ R
```

---

### Membership Functions

**Triangular**:
```
         ⎧ 0                 if x ≤ a
         ⎪ (x-a)/(b-a)       if a < x ≤ b
μ(x) =   ⎨ (c-x)/(c-b)       if b < x ≤ c
         ⎪ 0                 if x > c
         ⎩
```

**Gaussian**:
```
μ(x) = exp(-(x-mean)²/(2σ²))
```

**Generalized Bell**:
```
μ(x) = 1 / (1 + |((x-c)/a)|^(2b))
```

---

### Fuzzy Inference (Mamdani)

**Rule Evaluation**:
```
μ_output(y) = max_i [ min(μ_antecedent_i(x), μ_consequent_i(y)) ]
```

**Defuzzification (Centroid)**:
```
y* = Σ(y_i × μ(y_i)) / Σμ(y_i)
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- pip package manager

### Step 1: Clone & Navigate
```bash
cd D:\fuzzy
```

### Step 2: Activate Virtual Environment
```powershell
.\fuzzy\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```bash
pip install flask numpy python-dotenv google-generativeai markdown plotly
```

### Step 4: Configure API Key
Create `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 5: Run Application
```bash
python app.py
```

Application runs at: `http://127.0.0.1:5000`

---

## 📖 Usage Guide

### 1. Fuzzy Sets Operations (`/sets`)

**Input Format**:
```
(x1,0.5),(x2,0.8),(x3,0.3)
```

**Operations Available**:
- Equality, Complement
- Intersection, Union
- Algebraic Product/Sum/Difference
- Bounded Sum/Difference
- Power, Multiplication by Crisp Number
- Cartesian Product, Composition

**Workflow**:
1. Select operation
2. Enter Set A (required)
3. Enter Set B (for binary operations)
4. For scalar ops: choose "Apply to" (A or B) and enter scalar
5. Click **Compute** or **Explain**

---

### 2. Membership Functions (`/membership`)

**Parameters by Type**:
- **Triangular**: a, b, c (3 points)
- **Trapezoidal**: a, b, c, d (4 points)
- **Gaussian**: mean, sigma
- **Bell**: a, b, c
- **Sigmoid**: a, c

**Output**: Interactive Plotly chart + membership values

---

### 3. Fuzzy Relations & Composition (`/relations`)

**Modes**:
- **Random**: Auto-generate R and S
- **Manual**: Enter each matrix element

**Composition Types**:
- Max-Min (Mamdani)
- Max-Product

**Property Checks**:
- Reflexivity (diagonal = 1)
- Symmetry (R = Rᵀ)
- Transitivity (R∘R ⊆ R)

Displayed for both R (input) and T (result) when square.

---

### 4. Fuzzy Implications (`/implications`)

**Select Implication Operator**:
- Mamdani (min)
- Larsen (product)
- Zadeh (logical)
- Reichenbach (probabilistic)
- Goguen (theoretical)

**Input**: Two fuzzy sets (antecedent & consequent)

**Output**: 2D implication matrix + visualization

---

### 5. Fuzzy Inference System (`/fis`)

**Complete FIS Workflow**:
1. Define membership functions for input/output variables
2. Build rule base (IF-THEN rules)
3. Select inference method (Mamdani/Larsen)
4. Enter crisp input value
5. Choose defuzzification method
6. View fuzzified input, aggregated output, crisp result

---

## 🔌 API Reference

### Membership Function API

**Endpoint**: `POST /api/membership`

**Request Body**:
```json
{
  "mf_type": "Triangular",
  "params": [2, 5, 8]
}
```

**Response**:
```json
{
  "x": [0, 0.033, ..., 10],
  "y": [0, 0.011, ..., 0]
}
```

**Explanation Endpoint**: `POST /api/membership/explain`

---

## 🧪 Testing

### Manual Test Checklist

**✅ Fuzzy Sets** (`/sets`):
- [ ] Complement of single set
- [ ] Intersection of two sets
- [ ] Union, algebraic operations
- [ ] Power of set (scalar = 2)
- [ ] Cartesian product visualization
- [ ] Composition with Max-Min
- [ ] Explain button generates AI text

**✅ Membership Functions** (`/membership`):
- [ ] Triangular with params 2,5,8
- [ ] Gaussian with mean=5, sigma=1.5
- [ ] Slider updates work
- [ ] Explain generates description

**✅ Relations** (`/relations`):
- [ ] Random mode generates R, S matrices
- [ ] Manual mode accepts input
- [ ] Compute shows T matrix
- [ ] Property checks show correct Yes/No
- [ ] Reflexivity metric accurate for square R
- [ ] Transitivity violation shown when not transitive

**✅ UI/UX**:
- [ ] Black/white theme applied globally
- [ ] All buttons styled with brutalist shadows
- [ ] Tables have black borders
- [ ] Navigation sticky and responsive
- [ ] Mobile menu hidden on small screens
- [ ] Cache-busting works (CSS updates visible after refresh)

### Automated Test Script

```python
# test_fuzzy_modules.py
import numpy as np
from modules import fuzzy_sets, fuzzy_relations, fuzzy_implications

# Test 1: Fuzzy Sets
A = np.array([0.2, 0.5, 0.8])
B = np.array([0.3, 0.6, 0.7])
assert np.allclose(fuzzy_sets.intersection(A, B), [0.2, 0.5, 0.7])
print("✓ Fuzzy Sets: Intersection")

# Test 2: Relations Composition
R = np.array([[0.5, 0.8], [0.3, 0.9]])
S = np.array([[0.7, 0.4], [0.6, 0.8]])
T = fuzzy_relations.max_min_composition(R, S)
assert T.shape == (2, 2)
print("✓ Relations: Max-Min Composition")

# Test 3: Implications
implication_R = fuzzy_implications.mamdani_implication(A, B)
assert implication_R.shape == (3, 3)
print("✓ Implications: Mamdani")

print("\n✅ All basic tests passed!")
```

Run:
```bash
python test_fuzzy_modules.py
```

---

## 🎨 Design System

### Color Palette
- **Black**: `#000000` - Primary, borders, text
- **White**: `#ffffff` - Backgrounds, inverse text
- **Gray Scale**: 100-900 for subtle variations

### Typography
- **Headings**: 700-900 weight, uppercase, tight letter-spacing
- **Body**: Sans-serif, 16px base
- **Code**: Monospace, smaller size

### Components
- **Buttons**: 2px black border, 4-6px shadow offset, brutalist hover lift
- **Cards**: 2-3px borders, hard shadows, no gradients
- **Tables**: Separate borders, black headers, monospace numbers

### Spacing Scale
- xs: 0.25rem
- sm: 0.5rem
- md: 1rem
- lg: 1.5rem
- xl: 2rem
- 2xl: 3rem

---

## 🐛 Troubleshooting

### Issue: CSS not updating
**Solution**: Hard refresh (Ctrl+F5) or clear browser cache. The app uses cache-busting via file mtime.

### Issue: Import errors for modules
**Solution**: Ensure virtual environment is activated:
```powershell
.\fuzzy\Scripts\Activate.ps1
```

### Issue: Gemini API errors
**Solution**: Check `.env` file has valid `GEMINI_API_KEY`. Get one at: https://makersuite.google.com/app/apikey

### Issue: Template parse errors in editor
**Solution**: These are false positives from static linters. Jinja templates render correctly at runtime.

---

## 📚 References

1. **Fuzzy Set Theory**: Zadeh, L.A. (1965). "Fuzzy Sets". Information and Control.
2. **Fuzzy Inference Systems**: Mamdani, E.H. & Assilian, S. (1975). "An experiment in linguistic synthesis with a fuzzy logic controller".
3. **Defuzzification Methods**: Lee, C.C. (1990). "Fuzzy logic in control systems".

---

## 👤 Author

**Fuzzy Logic Toolbox**  
Professional implementation with black & white UI theme  
Developed with Flask, NumPy, Plotly, and Google Gemini AI

---

## 📄 License

Educational use. Not for commercial redistribution without permission.

---

**Last Updated**: November 6, 2025  
**Version**: 2.0 (Black & White Professional Edition)
