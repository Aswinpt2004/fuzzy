# 🚀 QUICK START: NEW FUZZY INFERENCE CAPABILITIES

## ✅ What's New

Three critical modules have been implemented, adding complete fuzzy inference system capabilities:

1. **fuzzy_tnorms.py** - T-norms and S-norms for fuzzy operations
2. **fuzzy_inference.py** - GMP/GMT inference engine
3. **fuzzy_rules.py** - Rule base management system

---

## 📖 Quick Examples

### Example 1: Using T-Norms

```python
from modules import fuzzy_tnorms
import numpy as np

# Define two fuzzy sets
A = np.array([0.2, 0.5, 0.8, 1.0])
B = np.array([0.3, 0.6, 0.7, 0.9])

# Apply different T-norms (fuzzy AND)
result_min = fuzzy_tnorms.minimum_tnorm(A, B)
result_product = fuzzy_tnorms.algebraic_product_tnorm(A, B)
result_bounded = fuzzy_tnorms.bounded_product_tnorm(A, B)

# Apply S-norms (fuzzy OR)
result_max = fuzzy_tnorms.maximum_snorm(A, B)
result_sum = fuzzy_tnorms.algebraic_sum_snorm(A, B)

# Compare all T-norms at once
all_tnorms = fuzzy_tnorms.compare_tnorms(0.7, 0.5)
print(all_tnorms)
# Output: {'minimum': 0.5, 'product': 0.35, 'bounded': 0.2, ...}
```

---

### Example 2: Generalized Modus Ponens (GMP)

```python
from modules import fuzzy_inference, fuzzy_implications
import numpy as np

# Define fuzzy sets
A = np.array([0.0, 0.5, 1.0, 0.5, 0.0])  # "Temperature is High"
B = np.array([0.0, 0.3, 0.7, 1.0, 0.8])  # "Fan speed is Fast"

# Create implication relation R: IF temp is High THEN fan is Fast
R = fuzzy_implications.mamdani_implication(A, B)

# Observed input (slightly different from A)
A_prime = np.array([0.0, 0.3, 0.8, 0.6, 0.0])  # "Temperature is somewhat high"

# Infer output using GMP
B_prime = fuzzy_inference.generalized_modus_ponens(A_prime, R, composition='max-min')

print("Inferred fan speed:", B_prime)
```

---

### Example 3: Creating Fuzzy Rules

```python
from modules.fuzzy_rules import FuzzyRule, FuzzyRuleBase
import numpy as np

# Define universes
temp = np.linspace(0, 100, 50)   # Temperature 0-100°C
fan = np.linspace(0, 100, 50)    # Fan speed 0-100%

# Define membership functions for temperature
cold = np.array([1.0, 0.8, 0.5, 0.2, 0.0, ...])
warm = np.array([0.0, 0.2, 0.5, 0.8, 1.0, 0.8, ...])
hot = np.array([0.0, 0.0, 0.0, 0.2, 0.5, 0.8, 1.0])

# Define membership functions for fan speed
slow = np.array([1.0, 0.8, 0.5, 0.2, 0.0, ...])
medium = np.array([0.0, 0.2, 0.5, 0.8, 1.0, 0.8, ...])
fast = np.array([0.0, 0.0, 0.0, 0.2, 0.5, 0.8, 1.0])

# Create rules
rule1 = FuzzyRule(
    "Temperature is Cold", 
    "Fan is Slow",
    cold, slow,
    implication_type='mamdani',
    weight=1.0
)

rule2 = FuzzyRule(
    "Temperature is Warm",
    "Fan is Medium", 
    warm, medium,
    implication_type='mamdani',
    weight=1.0
)

rule3 = FuzzyRule(
    "Temperature is Hot",
    "Fan is Fast",
    hot, fast,
    implication_type='mamdani',
    weight=1.0
)

# Create rule base
rule_base = FuzzyRuleBase(aggregation_method='maximum')
rule_base.add_rule(rule1)
rule_base.add_rule(rule2)
rule_base.add_rule(rule3)

print(rule_base)
# Output: 
# Fuzzy Rule Base (3 rules, aggregation=maximum):
#   1. IF Temperature is Cold THEN Fan is Slow (weight=1.0, impl=mamdani)
#   2. IF Temperature is Warm THEN Fan is Medium (weight=1.0, impl=mamdani)
#   3. IF Temperature is Hot THEN Fan is Fast (weight=1.0, impl=mamdani)
```

---

### Example 4: Complete Mamdani FIS

```python
from modules import fuzzy_inference, fuzzy_membership
from modules.fuzzy_rules import FuzzyRule
import numpy as np

# Define input/output universes
temperature = np.linspace(0, 100, 100)
fan_speed = np.linspace(0, 100, 100)

# Create membership functions using fuzzy_membership module
temp_cold = fuzzy_membership.trapezoidal_mf(temperature, 0, 0, 20, 40)
temp_warm = fuzzy_membership.triangular_mf(temperature, 30, 50, 70)
temp_hot = fuzzy_membership.trapezoidal_mf(temperature, 60, 80, 100, 100)

fan_slow = fuzzy_membership.trapezoidal_mf(fan_speed, 0, 0, 20, 40)
fan_medium = fuzzy_membership.triangular_mf(fan_speed, 30, 50, 70)
fan_fast = fuzzy_membership.trapezoidal_mf(fan_speed, 60, 80, 100, 100)

# Create rules
rules = [
    FuzzyRule("Cold", "Slow", temp_cold, fan_slow, 'mamdani'),
    FuzzyRule("Warm", "Medium", temp_warm, fan_medium, 'mamdani'),
    FuzzyRule("Hot", "Fast", temp_hot, fan_fast, 'mamdani')
]

# Run complete Mamdani FIS
input_temp = 65  # 65°C input
output_speed = fuzzy_inference.mamdani_inference_system(
    input_temp, 
    rules, 
    temperature, 
    fan_speed,
    defuzz_method='centroid',
    aggregation='maximum'
)

print(f"Input temperature: {input_temp}°C")
print(f"Output fan speed: {output_speed:.2f}%")
```

---

### Example 5: Sugeno FIS

```python
from modules import fuzzy_inference

# Sugeno rules with linear consequents
# Rule 1: IF temp is Low THEN speed = 0.5*temp + 10
# Rule 2: IF temp is High THEN speed = 1.5*temp + 20

rules_params = [
    (0.3, 0.5, 10),   # (firing_strength, p, q)
    (0.7, 1.5, 20)
]

input_temp = 65

output = fuzzy_inference.sugeno_inference_system(
    input_temp,
    rules_params,
    defuzz_method='wtaver'
)

print(f"Sugeno output: {output:.2f}")
```

---

### Example 6: Rule Chaining (Multi-Stage Inference)

```python
from modules import fuzzy_inference, fuzzy_implications
import numpy as np

# Define three fuzzy sets
A = np.array([0.0, 0.5, 1.0, 0.5])      # Input
B = np.array([0.0, 0.3, 0.7, 1.0])      # Intermediate
C = np.array([0.2, 0.6, 0.9, 1.0])      # Output

# Create two relations
R_AB = fuzzy_implications.mamdani_implication(A, B)  # IF A THEN B
R_BC = fuzzy_implications.mamdani_implication(B, C)  # IF B THEN C

# Chain rules: IF A THEN C (through B)
R_AC = fuzzy_inference.chain_rules(R_AB, R_BC, composition='max-min')

# Now use chained relation for inference
A_observed = np.array([0.1, 0.4, 0.9, 0.6])
C_inferred = fuzzy_inference.generalized_modus_ponens(A_observed, R_AC)

print("Direct inference from A to C:", C_inferred)
```

---

### Example 7: IF-THEN-ELSE Rules

```python
from modules.fuzzy_rules import rule_if_then_else
import numpy as np

A = np.array([0.0, 0.5, 1.0, 0.5, 0.0])  # Condition
B = np.array([0.0, 0.3, 0.7, 1.0, 0.8])  # Then consequent
C = np.array([1.0, 0.7, 0.3, 0.0, 0.0])  # Else consequent

# Create IF A THEN B ELSE C rule
rule = rule_if_then_else(A, B, C, "A", "B", "C")

print(rule)
# Output: IF A THEN B ELSE C
```

---

## 🎯 Key Functions

### T-Norms Module (fuzzy_tnorms.py)

| Function | Description |
|----------|-------------|
| `minimum_tnorm(a, b)` | Mamdani conjunction: min(a,b) |
| `algebraic_product_tnorm(a, b)` | Larsen conjunction: a·b |
| `bounded_product_tnorm(a, b)` | Łukasiewicz: max(0, a+b-1) |
| `maximum_snorm(a, b)` | Standard union: max(a,b) |
| `algebraic_sum_snorm(a, b)` | Probabilistic: a+b-ab |
| `get_tnorm(name)` | Get T-norm by name |
| `compare_tnorms(a, b)` | Compare all T-norms |

---

### Inference Module (fuzzy_inference.py)

| Function | Description |
|----------|-------------|
| `generalized_modus_ponens(A', R)` | Forward reasoning: B' = A' ∘ R |
| `generalized_modus_tollens(B', R)` | Backward reasoning: A' = B' ∘ R^T |
| `chain_rules(R1, R2)` | Hypothetical syllogism |
| `mamdani_inference_system(...)` | Complete Mamdani FIS |
| `sugeno_inference_system(...)` | Complete Sugeno FIS |
| `max_min_composition_inference(...)` | Max-min composition |
| `max_product_composition_inference(...)` | Max-product composition |

---

### Rules Module (fuzzy_rules.py)

| Class/Function | Description |
|----------------|-------------|
| `FuzzyRule` | Single IF-THEN rule |
| `FuzzyRuleBase` | Collection of rules |
| `create_rule(...)` | Factory for rules |
| `combine_rules(r1, r2, 'OR')` | Combine rules |
| `rule_if_then_else(A, B, C)` | IF-THEN-ELSE rule |
| `parse_rule_string(str)` | Parse natural language |

---

## 📊 Available Implication Types

When creating rules, you can use these implication types:

- `'mamdani'` - Min implication: R(x,y) = min(A(x), B(y))
- `'larsen'` - Product implication: R(x,y) = A(x) · B(y)
- `'zadeh'` - Zadeh implication: R(x,y) = max(1-A(x), min(A(x), B(y)))
- `'reichenbach'` - R(x,y) = 1 - A(x) + A(x)·B(y)
- `'goguen'` - R(x,y) = min(1, B(y)/A(x)) if A(x) > 0 else 1

---

## 🔄 Complete FIS Workflow

```python
# 1. Import modules
from modules import fuzzy_inference, fuzzy_membership
from modules.fuzzy_rules import FuzzyRule, FuzzyRuleBase
import numpy as np

# 2. Define universes
x = np.linspace(0, 10, 100)
y = np.linspace(0, 20, 100)

# 3. Define membership functions
input_low = fuzzy_membership.triangular_mf(x, 0, 0, 5)
input_high = fuzzy_membership.triangular_mf(x, 5, 10, 10)
output_small = fuzzy_membership.triangular_mf(y, 0, 0, 10)
output_large = fuzzy_membership.triangular_mf(y, 10, 20, 20)

# 4. Create rules
rule1 = FuzzyRule("Low", "Small", input_low, output_small, 'mamdani')
rule2 = FuzzyRule("High", "Large", input_high, output_large, 'mamdani')

# 5. Build rule base
rb = FuzzyRuleBase(aggregation_method='maximum')
rb.add_rule(rule1)
rb.add_rule(rule2)

# 6. Run inference
crisp_input = 7.5
crisp_output = fuzzy_inference.mamdani_inference_system(
    crisp_input, [rule1, rule2], x, y, 'centroid', 'maximum'
)

print(f"Input: {crisp_input} → Output: {crisp_output:.2f}")
```

---

## 🧪 Testing Your Setup

Run this quick test to verify everything works:

```python
from modules import fuzzy_tnorms, fuzzy_inference
from modules.fuzzy_rules import FuzzyRule, FuzzyRuleBase
import numpy as np

# Test T-norms
print("✅ Testing T-norms...")
result = fuzzy_tnorms.minimum_tnorm(0.7, 0.5)
print(f"min(0.7, 0.5) = {result}")

# Test GMP
print("\n✅ Testing GMP...")
A = np.array([0.2, 0.5, 0.8, 1.0])
R = np.outer(A, A)  # Simple relation
B = fuzzy_inference.generalized_modus_ponens(A, R)
print(f"GMP result shape: {B.shape}")

# Test Rules
print("\n✅ Testing Rules...")
rule = FuzzyRule("Test", "Test", A, A, 'mamdani')
rb = FuzzyRuleBase()
rb.add_rule(rule)
print(f"Rule base has {len(rb)} rules")

print("\n🎉 All modules working correctly!")
```

---

## 📚 Next Steps

1. **Try the examples above** to understand the new capabilities
2. **Create your own fuzzy rules** for control problems
3. **Experiment with different T-norms** and implication types
4. **Build complete FIS** for real-world applications
5. **Check CRITICAL_MODULES_COMPLETE.md** for detailed documentation

---

## 🆘 Need Help?

- **Module documentation**: Check docstrings in each module
- **Mathematical formulas**: See CRITICAL_MODULES_COMPLETE.md
- **Implementation plan**: See IMPLEMENTATION_PLAN.md
- **Examples**: Run the code snippets above

---

**Status**: ✅ All critical modules implemented and ready to use!
