# Aswin's Fuzzy Logic Toolbox

A comprehensive web-based interactive fuzzy logic system built with Flask and Python. This toolbox provides complete support for fuzzy set operations, membership functions, relations, implications, and full fuzzy inference workflows.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Installation & Setup](#installation--setup)
3. [Project Architecture](#project-architecture)
4. [Core Modules](#core-modules)
5. [Flask Routes & Pages](#flask-routes--pages)
6. [API Documentation](#api-documentation)
7. [Usage Examples](#usage-examples)
8. [Advanced Workflows](#advanced-workflows)

---

## Project Overview

### What is Fuzzy Logic?
Fuzzy logic is a mathematical framework for handling uncertainty and imprecision in data. Unlike classical binary logic (0 or 1), fuzzy logic allows values between 0 and 1 (called membership degrees) to represent partial truth.

**Key Concepts:**
- **Fuzzy Set**: A set where elements have partial membership (degree between 0 and 1)
- **Membership Function**: Maps input values to membership degrees
- **Fuzzy Operations**: Union, intersection, complement on fuzzy sets
- **Fuzzy Inference**: Rule-based reasoning with fuzzy sets
- **Defuzzification**: Converting fuzzy output to crisp (single) values

### Application Areas
- Temperature control systems
- Traffic management
- Medical diagnosis
- Decision support systems
- Image processing

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone or Download the Project
```bash
cd d:\fuzzy
```

### Step 2: Create Virtual Environment
```powershell
python -m venv fuzzy
.\fuzzy\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```bash
pip install flask numpy scipy python-dotenv google-generativeai markdown
```

### Step 4: Environment Configuration
Create `.env` file in project root:
```
GEMINI_API_KEY=your_google_api_key_here
```

Get API key from [Google AI Studio](https://aistudio.google.com/apikey)

### Step 5: Run the Application
```bash
python app.py
```

Open browser: `http://127.0.0.1:5000`

---

## Project Architecture

```
d:\fuzzy/
├── app.py                          # Main Flask application
├── .env                            # Environment variables (API keys)
├── .gitignore                      # Git ignore rules
├── modules/                        # Core fuzzy logic modules
│   ├── fuzzy_sets.py              # Fuzzy set operations
│   ├── fuzzy_membership.py         # Membership functions
│   ├── fuzzy_relations.py          # Fuzzy relations & composition
│   ├── fuzzy_implications.py       # Implication operators
│   ├── fuzzy_tnorms.py             # T-norms & S-norms
│   ├── fuzzy_rules.py              # Rule evaluation
│   ├── fuzzy_inference.py          # Inference engine
│   └── defuzzification.py          # Defuzzification methods
├── utils/
│   └── llm_explainer.py            # AI-powered explanations (Gemini API)
├── static/
│   ├── css/
│   │   └── style.css               # Global styles
│   └── js/
│       ├── fuzzy_sets_ui.js        # Fuzzy sets page interactivity
│       └── membership.js            # Membership function editor
├── templates/
│   ├── base.html                   # Base template with navigation
│   ├── index.html                  # Home page
│   ├── fuzzy_sets.html             # Fuzzy set operations page
│   ├── membership.html             # Membership functions page
│   ├── relations.html              # Fuzzy relations page
│   ├── implictaion.html            # Implications & rule base page
│   └── fis.html                    # Fuzzy inference system page
├── DOC_*.md                        # Individual page documentation files
└── README.md                       # This file
```

---

## Core Modules

### 1. `modules/fuzzy_sets.py` – Fuzzy Set Operations

This module implements fundamental fuzzy set operations and parsing.

#### Functions

**`parse_fuzzy(text: str) -> Tuple[List[str], np.ndarray]`**
- **Purpose**: Convert string representation to labels and membership values
- **Input**: `"(x1,0.5),(x2,0.3),(x3,0.7)"`
- **Output**: `(['x1','x2','x3'], array([0.5, 0.3, 0.7]))`
- **Use Case**: Parsing form inputs from web UI

```python
labels, values = parse_fuzzy("(low,0.2),(medium,0.5),(high,0.8)")
# labels = ['low', 'medium', 'high']
# values = array([0.2, 0.5, 0.8])
```

**`equality(A: np.ndarray, B: np.ndarray) -> bool`**
- **Purpose**: Check if two fuzzy sets are equal
- **Formula**: Returns True if all membership values match within tolerance
- **Example**: 
  ```python
  A = np.array([0.5, 0.3, 0.7])
  B = np.array([0.5, 0.3, 0.7])
  equality(A, B)  # True
  ```

**`complement(A: np.ndarray) -> np.ndarray`**
- **Purpose**: Fuzzy complement (negation)
- **Formula**: μ̄(x) = 1 - μ(x)
- **Example**: `complement([0.2, 0.5, 0.8])` → `[0.8, 0.5, 0.2]`
- **Interpretation**: If "temperature is low" has degree 0.2, then "temperature is not low" has degree 0.8

**`intersection(A: np.ndarray, B: np.ndarray) -> np.ndarray`**
- **Purpose**: Fuzzy intersection (AND operation)
- **Formula**: μ_{A∩B}(x) = min(μ_A(x), μ_B(x))
- **Example**: 
  ```python
  A = [0.5, 0.3, 0.7]
  B = [0.4, 0.6, 0.5]
  intersection(A, B)  # [0.4, 0.3, 0.5]
  ```
- **Logic**: Elements in both sets take the minimum membership

**`union(A: np.ndarray, B: np.ndarray) -> np.ndarray`**
- **Purpose**: Fuzzy union (OR operation)
- **Formula**: μ_{A∪B}(x) = max(μ_A(x), μ_B(x))
- **Example**: `union([0.5, 0.3], [0.4, 0.6])` → `[0.5, 0.6]`
- **Logic**: Elements belong to the union with their maximum membership

**`algebraic_product(A: np.ndarray, B: np.ndarray) -> np.ndarray`**
- **Purpose**: Element-wise multiplication
- **Formula**: μ(x) = μ_A(x) × μ_B(x)
- **Example**: `algebraic_product([0.5, 0.3], [0.4, 0.6])` → `[0.20, 0.18]`
- **Use**: Modular strength computation

**`algebraic_sum(A: np.ndarray, B: np.ndarray) -> np.ndarray`**
- **Purpose**: Probabilistic sum
- **Formula**: μ(x) = μ_A(x) + μ_B(x) - (μ_A(x) × μ_B(x))
- **Example**: `algebraic_sum([0.5, 0.3], [0.4, 0.6])` → `[0.7, 0.72]`
- **Logic**: Combines sets while avoiding saturation at 1

**`bounded_sum(A: np.ndarray, B: np.ndarray) -> np.ndarray`**
- **Purpose**: Bounded union
- **Formula**: μ(x) = min(1, μ_A(x) + μ_B(x))
- **Example**: `bounded_sum([0.5, 0.8], [0.6, 0.5])` → `[1.0, 1.0]`

**`bounded_difference(A: np.ndarray, B: np.ndarray) -> np.ndarray`**
- **Purpose**: Bounded difference
- **Formula**: μ(x) = max(0, μ_A(x) - μ_B(x))
- **Example**: `bounded_difference([0.7, 0.3], [0.5, 0.4])` → `[0.2, 0.0]`

**`crisp_multiply(A: np.ndarray, k: float) -> np.ndarray`**
- **Purpose**: Scale fuzzy set by crisp number
- **Formula**: μ'(x) = clip(k × μ(x), 0, 1)
- **Example**: `crisp_multiply([0.5, 0.3, 0.7], 0.5)` → `[0.25, 0.15, 0.35]`
- **Use**: Hedging ("very", "slightly") – NOT used directly but foundation

**`power(A: np.ndarray, p: float) -> np.ndarray`**
- **Purpose**: Raise fuzzy set to power
- **Formula**: μ'(x) = [μ(x)]^p
- **Example**: `power([0.5, 0.3], 2)` → `[0.25, 0.09]`
- **p=2**: "concentration" (makes low values lower)
- **p=0.5**: "dilation" (makes low values higher)

**`cartesian_product(A: np.ndarray, B: np.ndarray) -> np.ndarray`**
- **Purpose**: Create 2D relation R(x,y) from two sets
- **Formula**: r_{ij} = min(A_i, B_j)
- **Output**: 2D matrix of shape (len(A), len(B))
- **Example**:
  ```python
  A = [0.5, 0.3]
  B = [0.4, 0.6]
  cartesian_product(A, B)
  # [[0.4, 0.5],
  #  [0.3, 0.3]]
  ```

**`composition(R: np.ndarray, S: np.ndarray) -> np.ndarray`**
- **Purpose**: Max-Min composition of two relations
- **Formula**: T_{ik} = max_j min(R_{ij}, S_{jk})
- **Example**:
  ```python
  R = [[0.2, 0.8], [0.5, 0.4]]
  S = [[0.7, 0.3], [0.6, 0.9]]
  # Result: composition matrix
  ```
- **Use**: Combining relations transitively (e.g., "similar to" ∘ "taller than")

---

### 2. `modules/fuzzy_membership.py` – Membership Functions

Defines various membership function types. Each function maps a continuous input `x` to membership value μ(x) ∈ [0,1].

**`triangular(x: np.ndarray, a: float, b: float, c: float) -> np.ndarray`**
- **Purpose**: Triangular membership function
- **Formula**: 
  - μ(x) = 0 if x < a or x > c
  - μ(x) = (x - a)/(b - a) if a ≤ x ≤ b
  - μ(x) = (c - x)/(c - b) if b ≤ x ≤ c
- **Parameters**:
  - `a`: left foot
  - `b`: peak (apex)
  - `c`: right foot
- **Example**: `triangular(x, 2, 5, 8)` creates triangle peaking at x=5
- **Visual**: Linear rise from a to b, then linear fall to c
- **Common Use**: Temperature ranges (cold, warm, hot)

**`trapezoidal(x: np.ndarray, a: float, b: float, c: float, d: float) -> np.ndarray`**
- **Purpose**: Trapezoidal membership function
- **Formula**: Piecewise linear with a flat plateau
  - μ(x) = 0 if x < a or x > d
  - μ(x) = (x - a)/(b - a) if a ≤ x < b
  - μ(x) = 1 if b ≤ x ≤ c
  - μ(x) = (d - x)/(d - c) if c < x ≤ d
- **Parameters**:
  - `a`: left foot
  - `b`: left shoulder (plateau starts)
  - `c`: right shoulder (plateau ends)
  - `d`: right foot
- **Example**: `trapezoidal(x, 2, 4, 6, 8)` creates trapezoid with plateau [4,6]
- **Use**: Expressing "acceptable ranges" with uncertainty at boundaries

**`gaussian(x: np.ndarray, mean: float, sigma: float) -> np.ndarray`**
- **Purpose**: Gaussian (bell curve) membership function
- **Formula**: μ(x) = exp(-0.5 × ((x - mean)/σ)²)
- **Parameters**:
  - `mean`: center of the curve (where μ=1)
  - `sigma`: standard deviation (spread/width)
- **Example**: `gaussian(x, 5, 1.5)` creates smooth bell centered at 5
- **Properties**: Smooth, differentiable, symmetric
- **σ interpretation**:
  - Small σ: sharp, concentrated peak
  - Large σ: wide, gradual spread
- **Use**: Natural phenomena (age distributions, sensor readings)

**`bell_shaped(x: np.ndarray, a: float, b: float, c: float) -> np.ndarray`**
- **Purpose**: Generalized bell membership function
- **Formula**: μ(x) = 1 / (1 + |((x - c) / a)|^(2b))
- **Parameters**:
  - `a`: width parameter
  - `b`: slope parameter (sharpness of rise)
  - `c`: center (where μ=1)
- **Example**: `bell_shaped(x, 2, 3, 5)` creates smooth bell
- **Flexibility**: More control over shape than Gaussian
- **b=1**: gentler slope
- **b>1**: sharper, more step-like transition

**`sigmoid(x: np.ndarray, a: float, c: float) -> np.ndarray`**
- **Purpose**: Sigmoid (S-curve) membership function
- **Formula**: μ(x) = 1 / (1 + exp(-a × (x - c)))
- **Parameters**:
  - `a`: slope parameter (steepness)
  - `c`: inflection point (where μ=0.5)
- **Example**: `sigmoid(x, 1.2, 5)` creates S-curve through point (5, 0.5)
- **Properties**: Monotonic, asymptotic to 0 and 1
- **Use Cases**:
  - "more than" (e.g., "more than 50 kg")
  - "less than" (via 1 - sigmoid)
  - Directional fuzzy sets

---

### 3. `modules/fuzzy_implications.py` – Implication Operators

Implication operators define how antecedent fuzzy sets map to consequent fuzzy sets in rules.

**`mamdani_implication(A: np.ndarray, B: np.ndarray) -> np.ndarray`**
- **Purpose**: Min implication (most common)
- **Formula**: I(a_i, b_j) = min(μ_A(a_i), μ_B(b_j))
- **Output**: 2D matrix (rows: A elements, columns: B elements)
- **Logic**: Implication strength limited by weaker membership
- **Example**:
  ```
  A = [0.2, 0.5]
  B = [0.6, 0.9]
  
  Result matrix:
  [min(0.2, 0.6), min(0.2, 0.9)]   [0.2, 0.2]
  [min(0.5, 0.6), min(0.5, 0.9)] = [0.5, 0.5]
  ```
- **Pros**: Simple, efficient
- **Cons**: May create flat regions in output
- **Used In**: Most practical fuzzy systems (fans, controllers)

**`larsen_implication(A: np.ndarray, B: np.ndarray) -> np.ndarray`**
- **Purpose**: Product implication
- **Formula**: I(a_i, b_j) = μ_A(a_i) × μ_B(b_j)
- **Output**: Outer product of A and B
- **Logic**: Multiplicative strength
- **Example**:
  ```
  A = [0.5, 0.3]
  B = [0.6, 0.9]
  
  Result:
  [0.5×0.6, 0.5×0.9]   [0.30, 0.45]
  [0.3×0.6, 0.3×0.9] = [0.18, 0.27]
  ```
- **Pros**: Smoother control surface, better for continuous outputs
- **Cons**: Slightly more computationally expensive
- **Used In**: Advanced process control

**`zadeh_implication(A: np.ndarray, B: np.ndarray) -> np.ndarray`**
- **Purpose**: Logical implication (Zadeh operator)
- **Formula**: I(a_i, b_j) = max(1 - μ_A(a_i), μ_B(b_j))
- **Logic**: Classical material implication from logic theory
- **Example**:
  ```
  A = [0.2, 0.5]
  B = [0.6, 0.3]
  
  Row 1: [max(0.8, 0.6), max(0.8, 0.3)] = [0.8, 0.8]
  Row 2: [max(0.5, 0.6), max(0.5, 0.3)] = [0.6, 0.5]
  ```
- **Interpretation**: "If A is false (low), then anything follows; if A is true, then B must follow"
- **Used In**: Theoretical frameworks, logic-based systems

**`reichenbach_implication(A: np.ndarray, B: np.ndarray) -> np.ndarray`**
- **Purpose**: Reichenbach probabilistic implication
- **Formula**: I(a_i, b_j) = 1 - μ_A(a_i) + μ_A(a_i) × μ_B(b_j)
- **Logic**: Probabilistic approach: P(A→B) = 1 - P(A) + P(A)P(B)
- **Example**:
  ```
  I(0.5, 0.6) = 1 - 0.5 + 0.5 × 0.6 = 1.0
  I(0.8, 0.3) = 1 - 0.8 + 0.8 × 0.3 = 0.44
  ```
- **Used In**: Probabilistic systems, Bayesian frameworks

**`goguen_implication(A: np.ndarray, B: np.ndarray) -> np.ndarray`**
- **Purpose**: Goguen fuzzy implication (ratio-based)
- **Formula**: 
  - If μ_A(a_i) ≤ μ_B(b_j): I = 1.0
  - Else: I = μ_B(b_j) / μ_A(a_i)
- **Logic**: Ratio of consequent to antecedent strength
- **Example**:
  ```
  I(0.2, 0.6) = 1.0 (antecedent < consequent)
  I(0.8, 0.4) = 0.4 / 0.8 = 0.5
  ```
- **Used In**: Theoretical fuzzy logic, specialized applications

**`get_implication_method(method_name: str)`**
- **Purpose**: Factory function to retrieve implication by name
- **Supported Names**: 'mamdani', 'min', 'larsen', 'product', 'zadeh', 'logical', 'reichenbach', 'goguen'
- **Example**:
  ```python
  impl = get_implication_method('larsen')
  result = impl(A, B)
  ```

---

### 4. `modules/fuzzy_relations.py` – Fuzzy Relations & Composition

Handles fuzzy relations and composition operations.

**`random_relation(rows: int, cols: int) -> np.ndarray`**
- **Purpose**: Generate random fuzzy relation matrix
- **Output**: Matrix of shape (rows, cols) with values ∈ [0, 1]
- **Use**: Testing, demonstration, initial exploration

**`max_min_composition(R: np.ndarray, S: np.ndarray) -> np.ndarray`**
- **Purpose**: Compute max-min composition T = R ∘ S
- **Formula**: T_{ik} = max_j(min(R_{ij}, S_{jk}))
- **Dimensions**: R is (m×n), S is (n×p), result is (m×p)
- **Algorithm**:
  ```
  For each cell T[i,k]:
    1. Get row i from R: R[i,:] = [r_i1, r_i2, ..., r_in]
    2. Get column k from S: S[:,k] = [s_1k, s_2k, ..., s_nk]
    3. Compute pairwise min: [min(r_i1,s_1k), min(r_i2,s_2k), ...]
    4. Take max of results: max([...])
  ```
- **Example**:
  ```python
  R = [[0.2, 0.8], [0.5, 0.4]]
  S = [[0.7, 0.3], [0.6, 0.9]]
  
  T[0,0] = max(min(0.2,0.7), min(0.8,0.6)) = max(0.2, 0.6) = 0.6
  T[0,1] = max(min(0.2,0.3), min(0.8,0.9)) = max(0.2, 0.8) = 0.8
  # ... continue for T[1,0], T[1,1]
  ```
- **Interpretation**: "Similar to" ∘ "Faster than" = how much does chaining preserve the relation?

**`max_product_composition(R: np.ndarray, S: np.ndarray) -> np.ndarray`**
- **Purpose**: Compute max-product composition
- **Formula**: T_{ik} = max_j(R_{ij} × S_{jk})
- **Difference from max-min**: Uses multiplication instead of minimum
- **Example**: `max_product_composition(R, S)` → alternative result
- **Use**: When proportional strength matters more than limiting minimum

**`check_reflexivity(R: np.ndarray, eps: float = 1e-6) -> dict`**
- **Purpose**: Check if relation is reflexive
- **Definition**: Reflexive if R[i,i] = 1 for all i (within tolerance)
- **Output Dictionary**:
  ```python
  {
    "applicable": True/False,
    "is_reflexive": True/False,
    "min_diag": float (minimum diagonal value)
  }
  ```
- **Example**: Identity matrix is reflexive; empty relation is not
- **Interpretation**: "Every element relates to itself?"

**`check_symmetry(R: np.ndarray, eps: float = 1e-6) -> dict`**
- **Purpose**: Check if relation is symmetric
- **Definition**: Symmetric if R[i,j] = R[j,i] for all i,j
- **Output Dictionary**:
  ```python
  {
    "applicable": True/False,
    "is_symmetric": True/False,
    "max_diff": float (maximum asymmetry)
  }
  ```
- **Example**: "Friends" is symmetric; "Parent of" is not
- **Requirement**: Must be square matrix

**`check_transitivity(R: np.ndarray, comp_type: str = "Max-Min", eps: float = 1e-6) -> dict`**
- **Purpose**: Check if relation is transitive
- **Definition**: Transitive if (R ∘ R) ⊆ R (composition doesn't exceed original)
- **Algorithm**:
  1. Compute T = R ∘ R using specified composition type
  2. Find violations: V = max(0, T - R) for each element
  3. Report maximum violation and boolean result
- **Output Dictionary**:
  ```python
  {
    "applicable": True/False,
    "is_transitive": True/False,
    "max_violation": float (how much T exceeds R)
  }
  ```
- **Example**: "Greater than" is transitive; "Close to" is not necessarily
- **Composition Type Effect**: Same relation may be transitive under Max-Min but not Max-Product

**`check_all_properties(R: np.ndarray, comp_type: str = "Max-Min", eps: float = 1e-6) -> dict`**
- **Purpose**: Check all three properties in one call
- **Output Dictionary**:
  ```python
  {
    "reflexivity": {is_reflexive, min_diag, ...},
    "symmetry": {is_symmetric, max_diff, ...},
    "transitivity": {is_transitive, max_violation, ...}
  }
  ```
- **Use**: Comprehensive relation analysis in one function

---

### 5. `modules/defuzzification.py` – Defuzzification Methods

Converts fuzzy output sets to crisp (single numeric) values.

**`centroid(y: np.ndarray, mu: np.ndarray) -> float`**
- **Purpose**: Center of Gravity (CoG) defuzzification
- **Formula**: y* = Σ(y_i × μ_i) / Σμ_i
- **Example**:
  ```
  y = [0, 1, 2, 3, 4]
  μ = [0.0, 0.3, 0.8, 0.8, 0.2]
  
  Numerator = 0×0 + 1×0.3 + 2×0.8 + 3×0.8 + 4×0.2 = 5.1
  Denominator = 0 + 0.3 + 0.8 + 0.8 + 0.2 = 2.1
  y* = 5.1 / 2.1 ≈ 2.43
  ```
- **Properties**: Smooth, continuous, balances all membership contributions
- **Pros**: Intuitive (center of mass), widely used
- **Cons**: May produce intermediate values not representing peaks
- **Used In**: Most practical applications (77% of FIS systems)

**`bisector(y: np.ndarray, mu: np.ndarray) -> float`**
- **Purpose**: Bisector defuzzification
- **Method**: Find point that splits membership area exactly in half
- **Algorithm**:
  1. Compute cumulative sum of μ
  2. Find index where cumsum ≈ total/2
  3. Return corresponding y value
- **Example**:
  ```
  μ = [0.0, 0.3, 0.8, 0.8, 0.2]
  cumsum = [0.0, 0.3, 1.1, 1.9, 2.1]
  half = 2.1/2 = 1.05
  Nearest index: 2 (cumsum[2]=1.1)
  Result: y[2] = 2
  ```
- **Properties**: May differ from centroid, emphasizes median
- **Use**: When geometric center matters more than mass balance

**`mean_of_maxima(y: np.ndarray, mu: np.ndarray) -> float`**
- **Purpose**: Mean of Maxima (MoM) defuzzification
- **Method**: Average of all y where μ achieves maximum value
- **Formula**: y* = (Σ y_i where μ_i = max(μ)) / (count of maxima)
- **Example**:
  ```
  y = [0, 1, 2, 3, 4]
  μ = [0.0, 0.3, 0.8, 0.8, 0.2]
  
  max(μ) = 0.8 at indices 2, 3
  y* = (2 + 3) / 2 = 2.5
  ```
- **When to use**: Multiple peaks (ambiguity handling)
- **Interpretation**: "Report the average of the most likely outcomes"

**`first_of_maxima(y: np.ndarray, mu: np.ndarray) -> float`**
- **Purpose**: First of Maxima (FoM) defuzzification
- **Method**: Smallest y where μ achieves maximum
- **Formula**: y* = min(y_i where μ_i = max(μ))
- **Example**: In above case, y* = 2
- **Use**: Prefer conservative (early/small) values in decision making
- **Applications**: Safety-critical systems, risk-averse scenarios

**`last_of_maxima(y: np.ndarray, mu: np.ndarray) -> float`**
- **Purpose**: Last of Maxima (LoM) defuzzification
- **Method**: Largest y where μ achieves maximum
- **Formula**: y* = max(y_i where μ_i = max(μ))
- **Example**: In above case, y* = 3
- **Use**: Prefer optimistic (late/large) values
- **Applications**: Opportunity-seeking systems, aggressive strategies

**`height_method(y: np.ndarray, mu: np.ndarray) -> float`**
- **Purpose**: Height Method (maxima-based)
- **Implementation**: Alias for `mean_of_maxima` in this toolbox
- **Use**: Simple, fast, suitable for singleton output fuzzy sets
- **Common in**: Mamdani inference systems

**`weighted_average(y: np.ndarray, mu: np.ndarray) -> float`**
- **Purpose**: Weighted average defuzzification
- **Formula**: Same as centroid (y* = Σ(y_i × μ_i) / Σμ_i)
- **Note**: Identical to centroid when applied to single fuzzy set
- **Extension**: For multiple rule outputs, sum all before weighting
- **Use**: Aggregating rule outputs with membership weights

**`center_of_sums(y: np.ndarray, mu_list: List[np.ndarray]) -> float`**
- **Purpose**: Center of Sums defuzzification
- **Method**: Sum membership functions first, then apply centroid
- **Formula**: y* = Σ(y_i × (Σ μ_k_i)) / Σ(Σ μ_k_i)
- **Difference from CoG**: Doesn't normalize per rule; counts total area
- **Example**:
  ```
  From Rule 1: μ1 = [0.2, 0.5, 0.3]
  From Rule 2: μ2 = [0.1, 0.4, 0.6]
  
  Sum: [0.3, 0.9, 0.9]
  Apply centroid on summed set
  ```
- **Use**: Multiple rule outputs contributing to same output space
- **Characteristic**: Output can exceed individual rule outputs

**`lambda_cut(fuzzy_set: np.ndarray, lambda_value: float) -> np.ndarray`**
- **Purpose**: Apply lambda-cut (α-cut)
- **Formula**: A_λ = {x | μ_A(x) ≥ λ}
- **Output**: Binary array (1 where μ ≥ λ, 0 elsewhere)
- **Example**:
  ```
  μ = [0.2, 0.5, 0.8, 0.3]
  λ = 0.4
  Result: [0, 1, 1, 0]
  ```
- **Interpretation**: "Which elements meet the confidence threshold?"
- **Use Cases**: 
  - Filtering low-confidence memberships
  - Creating crisp sets from fuzzy sets
  - Extracting support regions

**`lambda_cut_defuzzification(y: np.ndarray, mu: np.ndarray, lambda_value: float, method='centroid') -> float`**
- **Purpose**: Combined lambda-cut and defuzzification
- **Algorithm**:
  1. Apply lambda-cut: μ_cut = (μ ≥ λ)
  2. If result is empty, reduce λ
  3. Apply defuzzification method on cut set
- **Example**:
  ```
  y = [0, 1, 2, 3, 4]
  μ = [0.2, 0.5, 0.8, 0.3, 0.1]
  λ = 0.5
  
  Step 1: μ_cut = [0, 1, 1, 0, 0]
  Step 2: y_cut = [1, 2]
  Step 3: centroid([1, 2], [1, 1]) = 1.5
  ```
- **Use**: Focusing decision on high-confidence regions only

**`multi_level_lambda_cut(y: np.ndarray, mu: np.ndarray, lambda_levels=None) -> float`**
- **Purpose**: Multi-level lambda-cut defuzzification
- **Method**: Apply multiple lambda levels, combine results
- **Default Levels**: [0.25, 0.5, 0.75, 1.0]
- **Weighting**: Higher lambda levels weighted more heavily
- **Use**: Hierarchical confidence consideration
- **Example**:
  ```
  λ=0.25: defuzzy → 2.1
  λ=0.50: defuzzy → 2.5
  λ=0.75: defuzzy → 2.8
  λ=1.00: defuzzy → 2.6 (peak only)
  
  Result: weighted average considering hierarchy
  ```

**`get_defuzzification_method(method_name: str)`**
- **Purpose**: Factory function to retrieve defuzzification method
- **Supported Methods**: 'centroid', 'cog', 'bisector', 'mom', 'fom', 'lom', 'height', 'cos', 'coa', 'wtaver', 'lambda_cut', 'multi_lambda'
- **Example**:
  ```python
  defuzz_func = get_defuzzification_method('centroid')
  crisp_output = defuzz_func(y, mu)
  ```

**`get_all_methods() -> dict`**
- **Purpose**: Get all available defuzzification methods organized by category
- **Output Structure**:
  ```python
  {
    'Maxima Methods': [('height', 'Height Method'), ('mom', 'Mean of Maxima')...],
    'Centroid Methods': [('cog', 'Center of Gravity')...],
    'Other Methods': [('lambda_cut', 'Lambda-Cut')...]
  }
  ```
- **Use**: UI dropdown population, documentation

---

### 6. `utils/llm_explainer.py` – AI-Powered Explanations

Generates educational explanations using Google Gemini API.

**`explain_with_llm(context: str, mf_type: str, params: dict/list, prompt: str) -> str`**
- **Purpose**: Generate AI-powered explanation of fuzzy operations
- **Parameters**:
  - `context`: Topic (e.g., "Fuzzy Implication", "Membership Function")
  - `mf_type`: Function type (e.g., "Gaussian", "Mamdani")
  - `params`: Parameters used
  - `prompt`: Specific task/question
- **Output**: HTML-formatted explanation with:
  - Markdown-rendered text
  - LaTeX math expressions ($...$ and $$...$$)
  - Section headings, bullet points, examples
- **Prompt Format**:
  ```
  "Explain the {mf_type} implication operator..."
  ```
- **Gemini Configuration**: Uses "gemini-pro-latest" model
- **Processing Pipeline**:
  1. Build structured prompt with context
  2. Call Gemini API
  3. Protect LaTeX from markdown processing
  4. Convert markdown to HTML
  5. Restore LaTeX for MathJax rendering
- **Error Handling**: Returns error message if API fails
- **Use**: Click "Explain" button on any page for instant understanding

---

## Flask Routes & Pages

### Main Application Flow (`app.py`)

**Route: `GET/POST /`**
- **Template**: `index.html`
- **Purpose**: Home page with navigation and feature overview
- **Displays**: Links to all tools and features

**Route: `GET/POST /sets`**
- **Template**: `fuzzy_sets.html`
- **Purpose**: Fuzzy set operations page
- **Accepts**:
  - `setA`: First fuzzy set string
  - `setB`: Second fuzzy set string
  - `operation`: Name of operation to perform
  - `apply_to`: "A" or "B" (for single-set operations)
  - `explain`: Optional flag for AI explanation
- **Computes**: Specified operation and optionally generates explanation
- **Returns**: Result (scalar, vector, or matrix), chart data, explanation
- **Operations Implemented**:
  ```
  Equality, Complement, Intersection, Union, 
  Algebraic Product, Multiplication by Crisp Number, 
  Power of Fuzzy Set, Algebraic Sum, Algebraic Difference, 
  Bounded Sum, Bounded Difference, 
  Cartesian Product, Composition
  ```

**Route: `GET/POST /membership`**
- **Template**: `membership.html`
- **Purpose**: Interactive membership function editor
- **Features**:
  - Dropdown to select MF type
  - Sliders to adjust parameters dynamically
  - Real-time Plotly visualization
  - Explain button for AI explanation

**Route: `POST /api/membership`**
- **Purpose**: API endpoint for membership function computation
- **Input**: JSON
  ```json
  {
    "mf_type": "Gaussian",
    "params": [5, 1.5]
  }
  ```
- **Output**: JSON
  ```json
  {
    "x": [0.0, 0.1, 0.2, ..., 10.0],
    "y": [0.0000, 0.0001, ..., 1.0000]
  }
  ```
- **Use**: Real-time updates without page reload

**Route: `POST /api/membership/explain`**
- **Purpose**: API endpoint for membership function explanations
- **Input**: JSON with mf_type and params
- **Output**: JSON with HTML explanation
- **Async**: Can be called independently of page submission

**Route: `GET/POST /relations`**
- **Template**: `relations.html`
- **Purpose**: Fuzzy relations and composition
- **Modes**:
  - Random: System generates random R and S
  - Manual: User inputs matrix values
- **Options**:
  - Rows (X): 2-6
  - Cols (Y): 2-6
  - Composition Type: Max-Min or Max-Product
- **Outputs**:
  - R and S matrices (displayed as tables)
  - Composition result T
  - Property checks (reflexivity, symmetry, transitivity)
  - Optional explanation
- **Property Checks**: Performed automatically for square matrices

**Route: `GET/POST /implications`**
- **Template**: `implictaion.html`
- **Purpose**: Fuzzy implications and rule base system
- **Section 1 - Simple Implication Matrix**:
  - Inputs: Antecedent set A, Consequent set B, Operator
  - Operators: Mamdani, Larsen, Zadeh, Reichenbach, Goguen
  - Output: Implication matrix + line plot
- **Section 2 - Rule Base System**:
  - Dynamic rule cards (add/remove)
  - Per-rule configuration: type, method, sets A/B/C
  - Rule evaluation with matrix display
  - Support for IF-THEN and IF-THEN-ELSE rules
- **Workflow**:
  1. Configure rules (fuzzy sets and operators)
  2. Click "Evaluate Rules"
  3. View implication matrices for each rule
  4. (Optional) Get AI explanation

**Route: `GET/POST /fis`**
- **Template**: `fis.html`
- **Purpose**: Complete fuzzy inference system
- **Sections**:
  1. Rule Base Builder (rule cards like implications page)
  2. Input/Output Configuration (fuzzified input, output universe)
  3. Inference Settings (inference method, t-norm, aggregation)
  4. Defuzzification Settings (method selection)
  5. Results (aggregated output, crisp value, plot)
- **Inference Methods**: Mamdani, Larsen, Zadeh
- **T-Norms**: Minimum, Product, Bounded, Drastic
- **Aggregation**: Maximum, Sum, Probabilistic Sum, Mean
- **Defuzzification**: All 11 methods (including lambda-cut)
- **Plot**: Line chart of aggregated output + vertical line for crisp value
- **Current State**: UI complete, backend computation ready for full pipeline wiring

**Route: `GET/POST /defuzzification` (conceptual)**
- **Purpose**: Standalone defuzzification page
- **Template**: `defuzzification.html` (currently removed; route logic exists)
- **Inputs**:
  - Fuzzy set (form: `(label,μ)` pairs)
  - Universe (optional numeric support)
  - Method selection
  - Lambda value (for lambda-cut)
- **Outputs**: Crisp value + line plot
- **Note**: Route `/defuzzification` present in app.py but template was deleted in cleanup

---

## API Documentation

### JSON Request/Response Formats

#### `/api/membership` - Compute Membership Function
```python
# Request
POST /api/membership
Content-Type: application/json

{
  "mf_type": "Gaussian",           # Type: Triangular, Trapezoidal, Gaussian, Bell, Sigmoid
  "params": [5.0, 1.5]             # [mean, sigma] for Gaussian
}

# Response
{
  "x": [0.0, 0.033, 0.067, ..., 10.0],    # 300 points in [0,10]
  "y": [0.00001, 0.00002, 0.00003, ...]   # Corresponding membership values
}

# Error Response
{
  "error": "Descriptive error message"
}
```

#### `/api/membership/explain` - Explain Membership Function
```python
# Request
POST /api/membership/explain
Content-Type: application/json

{
  "mf_type": "Gaussian",
  "params": [5.0, 1.5]
}

# Response
{
  "explanation": "<html><h3>Definition...</h3><p>...</p>..."
}

# Error Response
{
  "explanation": "<p class='error'>Gemini API error: ...</p>"
}
```

### Error Handling

All routes catch exceptions and return user-friendly error messages:
- Form validation errors display in explanation box
- Invalid fuzzy set strings show parsing errors
- API errors include error type and details
- Mathematical errors (division by zero, dimension mismatch) are caught

---

## Usage Examples

### Example 1: Basic Fuzzy Set Operations

**Goal**: Find intersection of two temperature readings

```python
from modules import fuzzy_sets
import numpy as np

# Define two fuzzy sets
A = np.array([0.2, 0.5, 0.8])  # low, medium, high
B = np.array([0.3, 0.6, 0.7])

# Compute intersection (minimum)
result = fuzzy_sets.intersection(A, B)
print(result)  # [0.2, 0.5, 0.7]

# Union
union_result = fuzzy_sets.union(A, B)
print(union_result)  # [0.3, 0.6, 0.8]

# Complement of A
complement_A = fuzzy_sets.complement(A)
print(complement_A)  # [0.8, 0.5, 0.2]
```

### Example 2: Membership Function Definition

**Goal**: Define a temperature range as Gaussian curve

```python
from modules import fuzzy_membership
import numpy as np

# Create input space (temperature range 0-40°C)
x = np.linspace(0, 40, 100)

# Define "comfortable" temperature as Gaussian around 22°C
comfortable = fuzzy_membership.gaussian(x, mean=22, sigma=5)

# Show peak and half-width
print(f"Peak at x=22: {comfortable[np.argmax(comfortable)]}")  # 1.0
print(f"Value at x=27: {comfortable[int(27*100/40)]}")  # ~0.368 (one std dev away)
```

### Example 3: Implication Operators Comparison

**Goal**: Compare how different operators handle a simple rule

```python
from modules import fuzzy_implications
import numpy as np

A = np.array([0.3, 0.7])  # Antecedent degrees
B = np.array([0.8, 0.4])  # Consequent degrees

# Mamdani (Min)
mamdani = fuzzy_implications.mamdani_implication(A, B)
print("Mamdani:\n", mamdani)
# [[0.3, 0.3],
#  [0.7, 0.4]]

# Larsen (Product)
larsen = fuzzy_implications.larsen_implication(A, B)
print("Larsen:\n", larsen)
# [[0.24, 0.12],
#  [0.56, 0.28]]

# Zadeh (Logical)
zadeh = fuzzy_implications.zadeh_implication(A, B)
print("Zadeh:\n", zadeh)
# [[0.8, 0.7],
#  [0.8, 0.4]]
```

### Example 4: Fuzzy Relation Composition

**Goal**: Compose two relations (e.g., "close to" ∘ "faster than")

```python
from modules import fuzzy_relations
import numpy as np

# Relation 1: How similar are objects X and Y?
R = np.array([[1.0, 0.7, 0.3],
              [0.7, 1.0, 0.5],
              [0.3, 0.5, 1.0]])

# Relation 2: How much faster is Y than Z?
S = np.array([[0.9, 0.2],
              [0.6, 0.5],
              [0.4, 0.8]])

# Compose: how similar are X and Z when considering speed?
T = fuzzy_relations.max_min_composition(R, S)
print("Composition Result:\n", T)

# Check properties
props = fuzzy_relations.check_all_properties(R, comp_type="Max-Min")
print("R is reflexive:", props['reflexivity']['is_reflexive'])
print("R is symmetric:", props['symmetry']['is_symmetric'])
```

### Example 5: Complete Defuzzification Workflow

**Goal**: Convert fuzzy output to crisp decision

```python
from modules import defuzzification
import numpy as np

# Output universe (temperature control: 0-100% fan speed)
y = np.array([0, 20, 40, 60, 80, 100])

# Fuzzy output from inference: how much should fan run?
mu = np.array([0.0, 0.1, 0.5, 0.8, 0.3, 0.1])

# Try different methods
print("Centroid:", defuzzification.centroid(y, mu))
print("MoM:", defuzzification.mean_of_maxima(y, mu))
print("FoM:", defuzzification.first_of_maxima(y, mu))
print("LoM:", defuzzification.last_of_maxima(y, mu))

# Lambda-cut: only use high-confidence regions (≥0.5)
crisp_high_conf = defuzzification.lambda_cut_defuzzification(y, mu, lambda_value=0.5)
print("Lambda-cut (λ=0.5):", crisp_high_conf)
```

---

## Advanced Workflows

### Workflow 1: Complete Temperature Control System

```
INPUT: Raw temperature (e.g., 24°C)
        ↓
FUZZIFICATION: Map to fuzzy sets
        "Low (0.1), Medium (0.7), High (0.2)"
        ↓
RULE EVALUATION (via Implications):
        Rule 1: IF temp is Low THEN fan is Slow
        Rule 2: IF temp is Medium THEN fan is Medium
        Rule 3: IF temp is High THEN fan is Fast
        ↓
AGGREGATION: Combine rule outputs
        Fan output: Slow (0.1), Medium (0.7), Fast (0.2)
        ↓
DEFUZZIFICATION: Convert to crisp value
        Centroid → 55% fan speed
        ↓
OUTPUT: Control fan to 55%
```

**Implementation Steps**:
1. Define membership functions for input (temperature) and output (fan speed)
2. Create rule base with implication matrices
3. Aggregate rule outputs
4. Apply defuzzification
5. Loop for continuous control

### Workflow 2: Multi-Rule Analysis with Properties

```
LOAD: Two fuzzy relations R and S
    ↓
COMPOSE: T = R ∘ S (Max-Min or Max-Product)
    ↓
CHECK PROPERTIES:
    - Is T reflexive? (relates to self?)
    - Is T symmetric? (bidirectional?)
    - Is T transitive? (chaining valid?)
    ↓
VISUALIZE: Display matrices, highlight violations
    ↓
INTERPRET: Understand relation characteristics
```

**Use Cases**: Knowledge representation, semantic similarity, hierarchical systems

### Workflow 3: Membership Function Tuning

```
START: Rough parameters (e.g., Gaussian with σ=2)
    ↓
TEST: Visualize on real data
    ↓
ADJUST: Modify parameters (mean, sigma) via UI sliders
    ↓
COMPARE: See how shape changes affect membership values
    ↓
FINALIZE: Once satisfied, use in FIS system
```

**Tips**:
- Start with symmetric shapes (Gaussian)
- Adjust width (σ) to match expected range
- Use multiple overlapping functions for smooth transitions
- Validate against domain expert expectations

---

## Tips & Troubleshooting

### Common Issues

**Issue**: API key not working
- **Solution**: Check `.env` file has correct `GEMINI_API_KEY`
- **Test**: Try `/api/membership/explain` endpoint

**Issue**: Fuzzy set parsing errors
- **Solution**: Ensure format is `(label,value)` with commas, e.g. `(low,0.2),(high,0.8)`
- **Valid**: `(x1,0.5),(x2,0.8),(x3,0.3)`
- **Invalid**: `x1:0.5, x2:0.8` (wrong separator)

**Issue**: Dimension mismatch in composition
- **Solution**: Ensure R is (m×n) and S is (n×p)
- **Example**: 2×3 matrix composed with 3×4 matrix → valid

**Issue**: All defuzzification methods return same value
- **Likely Cause**: Single peak (one element with high membership)
- **Solution**: Check fuzzy output distribution

### Performance Tips

- Large matrices (>100×100): Max-Product composition is slower than Max-Min
- Many rules in FIS: Processing time scales linearly; optimize rules if >20
- Real-time control: Cache membership functions, recompute only when parameters change

### Documentation Files

For detailed per-page documentation, see:
- `DOC_FUZZY_SETS.md` – All fuzzy set operations explained with examples
- `DOC_MEMBERSHIP.md` – Membership function types and use cases
- `DOC_RELATIONS.md` – Relations and composition workflows
- `DOC_IMPLICATIONS.md` – Implication operators and rule bases
- `DOC_DEFUZZIFICATION.md` – All defuzzification methods with examples
- `DOC_FIS.md` – End-to-end fuzzy inference workflows

---

## Contributing & Extension Points

### Adding a New Fuzzy Operation

1. Add function to `modules/fuzzy_sets.py`:
   ```python
   def new_operation(A, B):
       """Docstring"""
       return result
   ```

2. Add form field to `templates/fuzzy_sets.html`:
   ```html
   <option>New Operation</option>
   ```

3. Add handler in `app.py` `/sets` route:
   ```python
   elif operation == "New Operation":
       result = fuzzy_sets.new_operation(A, B)
   ```

4. (Optional) Update chart type if result is 2D

### Adding a New Membership Function

1. Add to `modules/fuzzy_membership.py`
2. Add option to `templates/membership.html` dropdown
3. Add case in `/api/membership` endpoint
4. Ensure parameters are clearly documented

### Adding a New Defuzzification Method

1. Add function to `modules/defuzzification.py`
2. Register in `get_defuzzification_method()` dictionary
3. Add to `get_all_methods()` return value
4. Test with various fuzzy outputs

---

## License & Attribution

This project is developed and maintained by Aswin.

**Dependencies**:
- Flask 3.1.2
- NumPy 2.3.4
- Google Generative AI (Gemini)
- Plotly 6.3.1

---

## Contact & Support

For questions, issues, or feature requests, please refer to the project documentation or contact the maintainer.

**Quick Help**:
- Syntax issues? → Check DOC files for format examples
- Understanding concepts? → Use "Explain" buttons throughout the UI
- API problems? → Verify `.env` configuration
- Logic issues? → Review mathematical formulas in this README

---

**Last Updated**: November 10, 2025

Happy fuzzy reasoning! 🧠
