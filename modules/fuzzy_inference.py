"""
Fuzzy Inference Module
Implements Generalized Modus Ponens (GMP), Generalized Modus Tollens (GMT),
and complete fuzzy inference systems (Mamdani and Sugeno).

Mathematical foundation:
- GMP: Given A→B and A', infer B' = A' ∘ R
- GMT: Given A→B and B', infer A' = B' ∘ R^T
- Composition: max-min, max-product, max-average
"""
import numpy as np
from modules import fuzzy_tnorms, fuzzy_implications, fuzzy_relations, defuzzification


# ========================================
# GENERALIZED MODUS PONENS (GMP)
# ========================================

def generalized_modus_ponens(A_prime, R, composition='max-min'):
    """
    Generalized Modus Ponens inference
    
    Rule: IF x is A THEN y is B  → Relation R(x,y)
    Fact: x is A' (observed)
    -------------------------
    Conclusion: y is B' = A' ∘ R
    
    Formula: µ_B'(y) = max_x [T(µ_A'(x), µ_R(x,y))]
    where T is a t-norm (typically min or product)
    
    Args:
        A_prime: Observed fuzzy set (1D array of membership values)
        R: Fuzzy relation matrix (2D array, shape: len(A_prime) × len(B))
        composition: 'max-min' (Mamdani) or 'max-product' (Larsen)
    
    Returns:
        B_prime: Inferred fuzzy set (1D array)
    """
    # Get composition operator
    if composition == 'max-min':
        tnorm = fuzzy_tnorms.minimum_tnorm
    elif composition == 'max-product':
        tnorm = fuzzy_tnorms.algebraic_product_tnorm
    elif composition == 'max-bounded':
        tnorm = fuzzy_tnorms.bounded_product_tnorm
    else:
        tnorm = fuzzy_tnorms.minimum_tnorm
    
    # B'(y) = max_x [T(A'(x), R(x,y))]
    m, n = R.shape  # m = len(A_prime), n = len(B)
    B_prime = np.zeros(n)
    
    for j in range(n):
        # For each output element y_j
        conjunction = tnorm(A_prime, R[:, j])
        B_prime[j] = np.max(conjunction)
    
    return B_prime


def max_min_composition_inference(A_prime, R):
    """
    Max-min composition inference (Mamdani)
    
    µ_B'(y) = max_x [min(µ_A'(x), µ_R(x,y))]
    
    Args:
        A_prime: Observed fuzzy input
        R: Fuzzy relation matrix
    
    Returns:
        B_prime: Inferred fuzzy output
    """
    return generalized_modus_ponens(A_prime, R, composition='max-min')


def max_product_composition_inference(A_prime, R):
    """
    Max-product composition inference (Larsen)
    
    µ_B'(y) = max_x [µ_A'(x) · µ_R(x,y)]
    
    Args:
        A_prime: Observed fuzzy input
        R: Fuzzy relation matrix
    
    Returns:
        B_prime: Inferred fuzzy output
    """
    return generalized_modus_ponens(A_prime, R, composition='max-product')


# ========================================
# GENERALIZED MODUS TOLLENS (GMT)
# ========================================

def generalized_modus_tollens(B_prime, R, composition='max-min'):
    """
    Generalized Modus Tollens inference (backward reasoning)
    
    Rule: IF x is A THEN y is B  → Relation R(x,y)
    Fact: y is B' (observed output)
    -------------------------
    Conclusion: x is A' = B' ∘ R^T
    
    Formula: µ_A'(x) = max_y [T(µ_B'(y), µ_R(x,y))]
    
    Args:
        B_prime: Observed fuzzy output (1D array)
        R: Fuzzy relation matrix (2D array, shape: len(A) × len(B_prime))
        composition: 'max-min' or 'max-product'
    
    Returns:
        A_prime: Inferred fuzzy input (1D array)
    """
    # Get composition operator
    if composition == 'max-min':
        tnorm = fuzzy_tnorms.minimum_tnorm
    elif composition == 'max-product':
        tnorm = fuzzy_tnorms.algebraic_product_tnorm
    else:
        tnorm = fuzzy_tnorms.minimum_tnorm
    
    # A'(x) = max_y [T(B'(y), R(x,y))]
    m, n = R.shape  # m = len(A), n = len(B_prime)
    A_prime = np.zeros(m)
    
    for i in range(m):
        # For each input element x_i
        conjunction = tnorm(B_prime, R[i, :])
        A_prime[i] = np.max(conjunction)
    
    return A_prime


# ========================================
# RULE CHAINING (HYPOTHETICAL SYLLOGISM)
# ========================================

def chain_rules(R1, R2, composition='max-min'):
    """
    Chain two fuzzy rules using hypothetical syllogism
    
    Rule 1: IF x is A THEN y is B  → R_AB(x,y)
    Rule 2: IF y is B THEN z is C  → R_BC(y,z)
    -------------------------
    Chained: IF x is A THEN z is C → R_AC(x,z) = R_AB ∘ R_BC
    
    Formula: µ_R_AC(x,z) = max_y [T(µ_R_AB(x,y), µ_R_BC(y,z))]
    
    Args:
        R1: First relation matrix (shape: m × n)
        R2: Second relation matrix (shape: n × p)
        composition: 'max-min' or 'max-product'
    
    Returns:
        R_chained: Chained relation matrix (shape: m × p)
    """
    # Use fuzzy_relations module
    return fuzzy_relations.max_min_composition(R1, R2)


def multi_stage_inference(input_fuzzy, relations_list, composition='max-min'):
    """
    Multi-stage fuzzy inference through chain of relations
    
    Args:
        input_fuzzy: Initial fuzzy input
        relations_list: List of relation matrices [R1, R2, ..., Rn]
        composition: Composition type
    
    Returns:
        Final inferred fuzzy output
    """
    current = input_fuzzy
    
    for R in relations_list:
        current = generalized_modus_ponens(current, R, composition)
    
    return current


# ========================================
# MAMDANI FUZZY INFERENCE SYSTEM
# ========================================

def mamdani_inference_system(input_value, rules, input_domain, output_domain,
                             defuzz_method='centroid', aggregation='maximum'):
    """
    Complete Mamdani-type fuzzy inference system
    
    Steps:
    1. Fuzzification: Convert crisp input to fuzzy set
    2. Rule evaluation: Apply all rules using GMP
    3. Aggregation: Combine rule outputs
    4. Defuzzification: Convert to crisp output
    
    Args:
        input_value: Crisp input value
        rules: List of FuzzyRule objects
        input_domain: Array of input universe values
        output_domain: Array of output universe values
        defuzz_method: Defuzzification method ('centroid', 'bisector', etc.)
        aggregation: Rule aggregation method ('maximum', 'sum', 'probsum')
    
    Returns:
        Crisp output value
    """
    from modules.fuzzy_rules import FuzzyRuleBase
    
    # Create rule base
    rule_base = FuzzyRuleBase(aggregation_method=aggregation)
    for rule in rules:
        rule_base.add_rule(rule)
    
    # Step 1: Fuzzification
    # Find where input_value is in input_domain
    idx = np.argmin(np.abs(input_domain - input_value))
    input_fuzzy = np.zeros(len(input_domain))
    input_fuzzy[idx] = 1.0  # Singleton fuzzification
    
    # Step 2 & 3: Inference and Aggregation
    output_fuzzy = rule_base.infer(input_fuzzy)
    
    # Step 4: Defuzzification
    if defuzz_method == 'centroid':
        crisp_output = defuzzification.centroid(output_domain, output_fuzzy)
    elif defuzz_method == 'bisector':
        crisp_output = defuzzification.bisector(output_domain, output_fuzzy)
    elif defuzz_method == 'mom':
        crisp_output = defuzzification.mean_of_maximum(output_domain, output_fuzzy)
    elif defuzz_method == 'som':
        crisp_output = defuzzification.smallest_of_maximum(output_domain, output_fuzzy)
    elif defuzz_method == 'lom':
        crisp_output = defuzzification.largest_of_maximum(output_domain, output_fuzzy)
    elif defuzz_method == 'wtaver':
        crisp_output = defuzzification.weighted_average(output_domain, output_fuzzy)
    else:
        crisp_output = defuzzification.centroid(output_domain, output_fuzzy)
    
    return crisp_output


def mamdani_step_by_step(input_value, rules, input_domain, output_domain):
    """
    Mamdani inference with detailed step-by-step breakdown
    
    Returns:
        Dictionary with intermediate results for visualization
    """
    from modules.fuzzy_rules import FuzzyRuleBase
    
    # Step 1: Fuzzification
    idx = np.argmin(np.abs(input_domain - input_value))
    input_fuzzy = np.zeros(len(input_domain))
    input_fuzzy[idx] = 1.0
    
    # Step 2: Rule evaluation
    rule_outputs = []
    for rule in rules:
        output = rule.evaluate(input_fuzzy)
        rule_outputs.append({
            'rule': str(rule),
            'output': output
        })
    
    # Step 3: Aggregation
    rule_base = FuzzyRuleBase(aggregation_method='maximum')
    for rule in rules:
        rule_base.add_rule(rule)
    
    aggregated = rule_base.aggregate([r['output'] for r in rule_outputs])
    
    # Step 4: Defuzzification
    crisp = defuzzification.centroid(output_domain, aggregated)
    
    return {
        'input_crisp': input_value,
        'input_fuzzy': input_fuzzy,
        'rule_outputs': rule_outputs,
        'aggregated_output': aggregated,
        'output_crisp': crisp,
        'input_domain': input_domain,
        'output_domain': output_domain
    }


# ========================================
# SUGENO FUZZY INFERENCE SYSTEM
# ========================================

def sugeno_inference_system(input_values, rules_params, defuzz_method='wtaver'):
    """
    Sugeno-type fuzzy inference system
    
    Sugeno rules have crisp linear functions as consequents:
    IF x is A THEN y = p*x + q
    
    Args:
        input_values: List/array of crisp input values
        rules_params: List of tuples [(A_fuzzy_set, p, q), ...]
                     where A is fuzzy set, p and q are linear parameters
        defuzz_method: 'wtaver' (weighted average) or 'wtsum' (weighted sum)
    
    Returns:
        Crisp output value
    """
    input_values = np.atleast_1d(input_values)
    
    # Calculate firing strength for each rule
    firing_strengths = []
    outputs = []
    
    for A_fuzzy, p, q in rules_params:
        # Firing strength = membership degree of input in A
        # Assuming singleton fuzzification
        if isinstance(A_fuzzy, (int, float)):
            alpha = A_fuzzy
        else:
            # Take max membership if input is fuzzy
            alpha = np.max(A_fuzzy)
        
        firing_strengths.append(alpha)
        
        # Consequent: y = p*x + q
        if len(input_values) == 1:
            y = p * input_values[0] + q
        else:
            # Multiple inputs: y = p1*x1 + p2*x2 + ... + q
            if isinstance(p, (list, np.ndarray)):
                y = np.dot(p, input_values) + q
            else:
                y = p * input_values[0] + q
        
        outputs.append(y)
    
    firing_strengths = np.array(firing_strengths)
    outputs = np.array(outputs)
    
    # Weighted average defuzzification
    if defuzz_method == 'wtaver':
        if np.sum(firing_strengths) == 0:
            return 0.0
        return np.sum(firing_strengths * outputs) / np.sum(firing_strengths)
    elif defuzz_method == 'wtsum':
        return np.sum(firing_strengths * outputs)
    else:
        return np.sum(firing_strengths * outputs) / np.sum(firing_strengths)


# ========================================
# INFERENCE WITH MEMBERSHIP FUNCTIONS
# ========================================

def infer_with_membership_functions(input_value, rules_mf, output_domain, 
                                   mf_type='triangular', defuzz='centroid'):
    """
    Inference using membership function definitions
    
    Args:
        input_value: Crisp input value
        rules_mf: List of tuples [(input_mf_params, output_mf_params, weight), ...]
        output_domain: Output universe array
        mf_type: 'triangular', 'gaussian', etc.
        defuzz: Defuzzification method
    
    Returns:
        Crisp output value
    """
    from modules import fuzzy_membership
    
    # Evaluate all rules
    rule_outputs = []
    
    for input_params, output_params, weight in rules_mf:
        # Calculate firing strength (antecedent membership)
        if mf_type == 'triangular':
            firing_strength = fuzzy_membership.triangular(input_value, *input_params)
        elif mf_type == 'trapezoidal':
            firing_strength = fuzzy_membership.trapezoidal(input_value, *input_params)
        elif mf_type == 'gaussian':
            firing_strength = fuzzy_membership.gaussian(input_value, *input_params)
        elif mf_type == 'sigmoid':
            firing_strength = fuzzy_membership.sigmoid(input_value, *input_params)
        elif mf_type == 'bell':
            firing_strength = fuzzy_membership.bell(input_value, *input_params)
        else:
            firing_strength = fuzzy_membership.triangular(input_value, *input_params)
        
        # Apply weight
        firing_strength *= weight
        
        # Calculate consequent fuzzy set
        if mf_type == 'triangular':
            consequent_full = fuzzy_membership.triangular_mf(output_domain, *output_params)
        elif mf_type == 'trapezoidal':
            consequent_full = fuzzy_membership.trapezoidal_mf(output_domain, *output_params)
        elif mf_type == 'gaussian':
            consequent_full = fuzzy_membership.gaussian_mf(output_domain, *output_params)
        elif mf_type == 'sigmoid':
            consequent_full = fuzzy_membership.sigmoid_mf(output_domain, *output_params)
        elif mf_type == 'bell':
            consequent_full = fuzzy_membership.bell_mf(output_domain, *output_params)
        else:
            consequent_full = fuzzy_membership.triangular_mf(output_domain, *output_params)
        
        # Clip consequent by firing strength (Mamdani implication)
        clipped = np.minimum(firing_strength, consequent_full)
        rule_outputs.append(clipped)
    
    # Aggregate all rule outputs
    aggregated = np.maximum.reduce(rule_outputs)
    
    # Defuzzify
    if defuzz == 'centroid':
        return defuzzification.centroid(output_domain, aggregated)
    elif defuzz == 'bisector':
        return defuzzification.bisector(output_domain, aggregated)
    elif defuzz == 'mom':
        return defuzzification.mean_of_maximum(output_domain, aggregated)
    else:
        return defuzzification.centroid(output_domain, aggregated)


# ========================================
# UTILITY FUNCTIONS
# ========================================

def get_inference_method(method_name):
    """
    Get inference function by name
    
    Args:
        method_name: 'gmp', 'gmt', 'max-min', 'max-product', 'mamdani', 'sugeno'
    
    Returns:
        Inference function
    """
    method_map = {
        'gmp': generalized_modus_ponens,
        'generalized_modus_ponens': generalized_modus_ponens,
        'gmt': generalized_modus_tollens,
        'generalized_modus_tollens': generalized_modus_tollens,
        'max-min': max_min_composition_inference,
        'max_min': max_min_composition_inference,
        'max-product': max_product_composition_inference,
        'max_product': max_product_composition_inference,
        'mamdani': mamdani_inference_system,
        'sugeno': sugeno_inference_system,
    }
    
    return method_map.get(method_name.lower(), generalized_modus_ponens)


def compare_inference_methods(A_prime, R):
    """
    Compare different inference composition methods
    
    Args:
        A_prime: Input fuzzy set
        R: Relation matrix
    
    Returns:
        Dictionary with results from each method
    """
    results = {
        'max-min (Mamdani)': max_min_composition_inference(A_prime, R),
        'max-product (Larsen)': max_product_composition_inference(A_prime, R),
        'max-bounded': generalized_modus_ponens(A_prime, R, composition='max-bounded'),
    }
    
    return results
