# modules/fuzzy_sets.py
import numpy as np

def parse_fuzzy(text):
    """Convert string like (x1,0.3),(x2,0.7) → dict + array"""
    pairs = text.replace("{", "").replace("}", "").split(")")
    fuzzy_dict = {}
    for p in pairs:
        if "(" in p:
            vals = p.strip(" ,(").split(",")
            if len(vals) == 2:
                fuzzy_dict[vals[0]] = float(vals[1])
    labels = list(fuzzy_dict.keys())
    values = np.array(list(fuzzy_dict.values()))
    return labels, values




# -------------------------------
# FUZZY OPERATIONS
# -------------------------------

def equality(A, B):
    """Check if two fuzzy sets are equal"""
    return np.allclose(A, B)

def complement(A):
    """Fuzzy complement"""
    return 1 - np.array(A)

def intersection(A, B):
    """Fuzzy intersection (min)"""
    return np.fmin(A, B)

def union(A, B):
    """Fuzzy union (max)"""
    return np.fmax(A, B)

def algebraic_product(A, B):
    """Algebraic product"""
    return np.array(A) * np.array(B)

def crisp_multiply(A, k):
    """Multiply fuzzy set by crisp number"""
    return np.clip(np.array(A) * k, 0, 1)

def power(A, p):
    """Raise fuzzy set to power"""
    return np.clip(np.array(A) ** p, 0, 1)

def algebraic_sum(A, B):
    """Algebraic sum"""
    A, B = np.array(A), np.array(B)
    return np.clip(A + B - (A * B), 0, 1)

def algebraic_difference(A, B):
    """Algebraic difference"""
    A, B = np.array(A), np.array(B)
    return np.clip(A * (1 - B), 0, 1)

def bounded_sum(A, B):
    """Bounded sum"""
    return np.clip(np.array(A) + np.array(B), 0, 1)

def bounded_difference(A, B):
    """Bounded difference"""
    return np.clip(np.array(A) - np.array(B), 0, 1)

def cartesian_product(A, B):
    """Cartesian product (creates relation matrix)"""
    A, B = np.array(A), np.array(B)
    result = np.zeros((len(A), len(B)))
    for i in range(len(A)):
        for j in range(len(B)):
            result[i, j] = np.fmin(A[i], B[j])
    return result

def composition(R, S):
    """Max–Min composition for fuzzy relations"""
    R, S = np.array(R), np.array(S)
    if R.shape[1] != S.shape[0]:
        raise ValueError("Incompatible matrix dimensions for composition.")
    T = np.zeros((R.shape[0], S.shape[1]))
    for i in range(R.shape[0]):
        for j in range(S.shape[1]):
            T[i, j] = np.max(np.minimum(R[i, :], S[:, j]))
    return T
