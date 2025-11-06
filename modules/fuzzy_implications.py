"""
Fuzzy Implication Operators Module
Implements various fuzzy implication methods for rule-based systems
"""
import numpy as np


def mamdani_implication(A, B):
    """
    Mamdani (Min) Implication
    Formula: μ_R(x,y) = min(μ_A(x), μ_B(y))
    Most commonly used in fuzzy inference systems
    
    Args:
        A: Antecedent fuzzy set (1D array)
        B: Consequent fuzzy set (1D array)
    
    Returns:
        2D implication matrix R
    """
    A = np.asarray(A).flatten()
    B = np.asarray(B).flatten()
    
    # Create meshgrid and compute min
    A_mesh, B_mesh = np.meshgrid(B, A)
    return np.minimum(A_mesh.T, B_mesh.T)


def larsen_implication(A, B):
    """
    Larsen (Product) Implication
    Formula: μ_R(x,y) = μ_A(x) × μ_B(y)
    Provides smoother control surfaces
    
    Args:
        A: Antecedent fuzzy set (1D array)
        B: Consequent fuzzy set (1D array)
    
    Returns:
        2D implication matrix R
    """
    A = np.asarray(A).flatten()
    B = np.asarray(B).flatten()
    
    # Outer product
    return np.outer(A, B)


def zadeh_implication(A, B):
    """
    Zadeh (Logical) Implication
    Formula: μ_R(x,y) = max(1 - μ_A(x), μ_B(y))
    Based on classical logic implication
    
    Args:
        A: Antecedent fuzzy set (1D array)
        B: Consequent fuzzy set (1D array)
    
    Returns:
        2D implication matrix R
    """
    A = np.asarray(A).flatten()
    B = np.asarray(B).flatten()
    
    R = np.zeros((len(A), len(B)))
    for i in range(len(A)):
        for j in range(len(B)):
            R[i, j] = max(1 - A[i], B[j])
    
    return R


def reichenbach_implication(A, B):
    """
    Reichenbach Implication
    Formula: μ_R(x,y) = 1 - μ_A(x) + μ_A(x) × μ_B(y)
    Probabilistic approach to implication
    
    Args:
        A: Antecedent fuzzy set (1D array)
        B: Consequent fuzzy set (1D array)
    
    Returns:
        2D implication matrix R
    """
    A = np.asarray(A).flatten()
    B = np.asarray(B).flatten()
    
    R = np.zeros((len(A), len(B)))
    for i in range(len(A)):
        for j in range(len(B)):
            R[i, j] = 1 - A[i] + A[i] * B[j]
    
    return R


def goguen_implication(A, B):
    """
    Goguen Implication
    Formula: μ_R(x,y) = 1 if μ_A(x) ≤ μ_B(y) else μ_B(y) / μ_A(x)
    Theoretical implication based on division
    
    Args:
        A: Antecedent fuzzy set (1D array)
        B: Consequent fuzzy set (1D array)
    
    Returns:
        2D implication matrix R
    """
    A = np.asarray(A).flatten()
    B = np.asarray(B).flatten()
    
    R = np.zeros((len(A), len(B)))
    for i in range(len(A)):
        for j in range(len(B)):
            if A[i] <= B[j]:
                R[i, j] = 1.0
            elif A[i] == 0:
                R[i, j] = 1.0
            else:
                R[i, j] = min(1.0, B[j] / A[i])
    
    return R


def get_implication_method(method_name):
    """
    Factory function to get implication method by name
    
    Args:
        method_name: String name of the method
    
    Returns:
        Function reference
    """
    methods = {
        'mamdani': mamdani_implication,
        'min': mamdani_implication,
        'larsen': larsen_implication,
        'product': larsen_implication,
        'zadeh': zadeh_implication,
        'logical': zadeh_implication,
        'reichenbach': reichenbach_implication,
        'goguen': goguen_implication
    }
    
    return methods.get(method_name.lower(), mamdani_implication)
