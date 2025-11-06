"""
Fuzzy T-Norms and S-Norms Module
Implements triangular norms (AND operations) and S-norms (OR operations)
for fuzzy logic systems.

T-norms define fuzzy conjunction (AND-like operations).
S-norms define fuzzy disjunction (OR-like operations).
"""
import numpy as np


# ========================================
# T-NORMS (Fuzzy AND Operations)
# ========================================

def minimum_tnorm(a, b):
    """
    Minimum T-norm (Mamdani)
    Formula: T_min(a,b) = min(a,b)
    
    Most commonly used in fuzzy systems.
    Properties: Commutative, Associative, Monotonic
    
    Args:
        a, b: Membership values (float or numpy array)
    
    Returns:
        Minimum of a and b
    """
    return np.minimum(a, b)


def algebraic_product_tnorm(a, b):
    """
    Algebraic Product T-norm (Larsen)
    Formula: T_ap(a,b) = a · b
    
    Provides smooth, multiplicative conjunction.
    Used when smoother transitions are needed.
    
    Args:
        a, b: Membership values (float or numpy array)
    
    Returns:
        Product of a and b
    """
    return np.multiply(a, b)


def bounded_product_tnorm(a, b):
    """
    Bounded Product T-norm (Łukasiewicz)
    Formula: T_bp(a,b) = max(0, a + b - 1)
    
    Bounds the sum to ensure result stays in [0,1].
    Stricter than minimum, more lenient than product.
    
    Args:
        a, b: Membership values (float or numpy array)
    
    Returns:
        Bounded product value
    """
    return np.maximum(0, a + b - 1)


def drastic_product_tnorm(a, b):
    """
    Drastic Product T-norm
    Formula: T_dp(a,b) = {a if b=1; b if a=1; 0 otherwise}
    
    Extreme intersection case - very strict.
    Only returns non-zero if one operand is exactly 1.
    
    Args:
        a, b: Membership values (float or numpy array)
    
    Returns:
        Drastic product value
    """
    a = np.asarray(a)
    b = np.asarray(b)
    
    result = np.zeros_like(a, dtype=float)
    
    # If b = 1, return a
    mask_b_one = np.isclose(b, 1.0)
    result = np.where(mask_b_one, a, result)
    
    # If a = 1, return b
    mask_a_one = np.isclose(a, 1.0)
    result = np.where(mask_a_one & ~mask_b_one, b, result)
    
    # Otherwise return 0 (already initialized)
    
    return result


def hamacher_product_tnorm(a, b, gamma=0):
    """
    Hamacher Product T-norm
    Formula: T_h(a,b) = ab / (γ + (1-γ)(a + b - ab))
    
    Parameterized T-norm family.
    γ=0: Algebraic Product
    γ=1: Einstein Product
    γ→∞: Drastic Product
    
    Args:
        a, b: Membership values (float or numpy array)
        gamma: Parameter (default 0)
    
    Returns:
        Hamacher product value
    """
    a = np.asarray(a)
    b = np.asarray(b)
    
    numerator = a * b
    denominator = gamma + (1 - gamma) * (a + b - a * b)
    
    # Avoid division by zero
    denominator = np.where(denominator == 0, 1e-10, denominator)
    
    return numerator / denominator


# ========================================
# S-NORMS (Fuzzy OR Operations)
# ========================================

def maximum_snorm(a, b):
    """
    Maximum S-norm
    Formula: S_max(a,b) = max(a,b)
    
    Dual of minimum T-norm.
    Most commonly used fuzzy union.
    
    Args:
        a, b: Membership values (float or numpy array)
    
    Returns:
        Maximum of a and b
    """
    return np.maximum(a, b)


def algebraic_sum_snorm(a, b):
    """
    Algebraic Sum S-norm
    Formula: S_as(a,b) = a + b - a·b
    
    Probabilistic sum - ensures result ≤ 1.
    Dual of algebraic product T-norm.
    
    Args:
        a, b: Membership values (float or numpy array)
    
    Returns:
        Algebraic sum value
    """
    return a + b - a * b


def bounded_sum_snorm(a, b):
    """
    Bounded Sum S-norm (Łukasiewicz)
    Formula: S_bs(a,b) = min(1, a + b)
    
    Simple bounded addition.
    Dual of bounded product T-norm.
    
    Args:
        a, b: Membership values (float or numpy array)
    
    Returns:
        Bounded sum value
    """
    return np.minimum(1, a + b)


def drastic_sum_snorm(a, b):
    """
    Drastic Sum S-norm
    Formula: S_ds(a,b) = {a if b=0; b if a=0; 1 otherwise}
    
    Extreme union case - very permissive.
    Returns 1 unless one operand is exactly 0.
    
    Args:
        a, b: Membership values (float or numpy array)
    
    Returns:
        Drastic sum value
    """
    a = np.asarray(a)
    b = np.asarray(b)
    
    result = np.ones_like(a, dtype=float)
    
    # If b = 0, return a
    mask_b_zero = np.isclose(b, 0.0)
    result = np.where(mask_b_zero, a, result)
    
    # If a = 0, return b
    mask_a_zero = np.isclose(a, 0.0)
    result = np.where(mask_a_zero & ~mask_b_zero, b, result)
    
    # Otherwise return 1 (already initialized)
    
    return result


def hamacher_sum_snorm(a, b, gamma=0):
    """
    Hamacher Sum S-norm
    Formula: S_h(a,b) = (a + b - (2-γ)ab) / (1 - (1-γ)ab)
    
    Dual of Hamacher product.
    
    Args:
        a, b: Membership values (float or numpy array)
        gamma: Parameter (default 0)
    
    Returns:
        Hamacher sum value
    """
    a = np.asarray(a)
    b = np.asarray(b)
    
    numerator = a + b - (2 - gamma) * a * b
    denominator = 1 - (1 - gamma) * a * b
    
    # Avoid division by zero
    denominator = np.where(denominator == 0, 1e-10, denominator)
    
    return numerator / denominator


# ========================================
# AVERAGING OPERATORS
# ========================================

def arithmetic_mean(a, b):
    """
    Arithmetic Mean
    Formula: (a + b) / 2
    
    Simple averaging operator.
    
    Args:
        a, b: Membership values (float or numpy array)
    
    Returns:
        Arithmetic mean
    """
    return (a + b) / 2.0


def geometric_mean(a, b):
    """
    Geometric Mean
    Formula: √(a · b)
    
    Multiplicative averaging.
    
    Args:
        a, b: Membership values (float or numpy array)
    
    Returns:
        Geometric mean
    """
    return np.sqrt(a * b)


def harmonic_mean(a, b):
    """
    Harmonic Mean
    Formula: 2ab / (a + b)
    
    Used when averaging rates or ratios.
    
    Args:
        a, b: Membership values (float or numpy array)
    
    Returns:
        Harmonic mean
    """
    denominator = a + b
    denominator = np.where(denominator == 0, 1e-10, denominator)
    return 2 * a * b / denominator


# ========================================
# FACTORY FUNCTIONS
# ========================================

def get_tnorm(name):
    """
    Factory function to get T-norm by name
    
    Args:
        name: String name of T-norm
    
    Returns:
        Function reference to T-norm operator
    
    Available T-norms:
        - 'minimum', 'min', 'mamdani'
        - 'product', 'algebraic_product', 'larsen'
        - 'bounded_product', 'lukasiewicz'
        - 'drastic_product', 'drastic'
        - 'hamacher_product', 'hamacher'
    """
    tnorms = {
        'minimum': minimum_tnorm,
        'min': minimum_tnorm,
        'mamdani': minimum_tnorm,
        
        'product': algebraic_product_tnorm,
        'algebraic_product': algebraic_product_tnorm,
        'larsen': algebraic_product_tnorm,
        
        'bounded_product': bounded_product_tnorm,
        'bounded': bounded_product_tnorm,
        'lukasiewicz': bounded_product_tnorm,
        
        'drastic_product': drastic_product_tnorm,
        'drastic': drastic_product_tnorm,
        
        'hamacher_product': hamacher_product_tnorm,
        'hamacher': hamacher_product_tnorm,
    }
    
    return tnorms.get(name.lower(), minimum_tnorm)


def get_snorm(name):
    """
    Factory function to get S-norm by name
    
    Args:
        name: String name of S-norm
    
    Returns:
        Function reference to S-norm operator
    
    Available S-norms:
        - 'maximum', 'max'
        - 'algebraic_sum', 'probsum'
        - 'bounded_sum', 'lukasiewicz'
        - 'drastic_sum', 'drastic'
        - 'hamacher_sum', 'hamacher'
    """
    snorms = {
        'maximum': maximum_snorm,
        'max': maximum_snorm,
        
        'algebraic_sum': algebraic_sum_snorm,
        'probsum': algebraic_sum_snorm,
        
        'bounded_sum': bounded_sum_snorm,
        'bounded': bounded_sum_snorm,
        'lukasiewicz': bounded_sum_snorm,
        
        'drastic_sum': drastic_sum_snorm,
        'drastic': drastic_sum_snorm,
        
        'hamacher_sum': hamacher_sum_snorm,
        'hamacher': hamacher_sum_snorm,
    }
    
    return snorms.get(name.lower(), maximum_snorm)


# ========================================
# UTILITY FUNCTIONS
# ========================================

def compare_tnorms(a, b):
    """
    Compare all T-norms on given inputs
    
    Args:
        a, b: Membership values
    
    Returns:
        Dictionary with results from all T-norms
    """
    return {
        'Minimum (Mamdani)': minimum_tnorm(a, b),
        'Algebraic Product (Larsen)': algebraic_product_tnorm(a, b),
        'Bounded Product': bounded_product_tnorm(a, b),
        'Drastic Product': drastic_product_tnorm(a, b),
        'Hamacher Product': hamacher_product_tnorm(a, b),
    }


def compare_snorms(a, b):
    """
    Compare all S-norms on given inputs
    
    Args:
        a, b: Membership values
    
    Returns:
        Dictionary with results from all S-norms
    """
    return {
        'Maximum': maximum_snorm(a, b),
        'Algebraic Sum': algebraic_sum_snorm(a, b),
        'Bounded Sum': bounded_sum_snorm(a, b),
        'Drastic Sum': drastic_sum_snorm(a, b),
        'Hamacher Sum': hamacher_sum_snorm(a, b),
    }
