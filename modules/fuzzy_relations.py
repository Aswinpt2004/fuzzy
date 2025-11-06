# modules/fuzzy_relations.py
import numpy as np

def random_relation(rows, cols):
    """Generate a random fuzzy relation matrix."""
    return np.round(np.random.rand(rows, cols), 2)

def max_min_composition(R, S):
    """Compute Max-Min Composition of R(x, y) and S(y, z)."""
    m, n = R.shape
    n2, p = S.shape
    assert n == n2, "Inner dimensions must match for composition."
    T = np.zeros((m, p))
    for i in range(m):
        for j in range(p):
            T[i, j] = np.max(np.minimum(R[i, :], S[:, j]))
    return np.round(T, 3)

def max_product_composition(R, S):
    """Compute Max-Product Composition of R(x, y) and S(y, z)."""
    m, n = R.shape
    n2, p = S.shape
    assert n == n2, "Inner dimensions must match for composition."
    T = np.zeros((m, p))
    for i in range(m):
        for j in range(p):
            T[i, j] = np.max(R[i, :] * S[:, j])
    return np.round(T, 3)

# ------------------------------
# Relation Property Checks
# ------------------------------

def _is_square(M: np.ndarray) -> bool:
    return len(M.shape) == 2 and M.shape[0] == M.shape[1]

def check_reflexivity(R: np.ndarray, eps: float = 1e-6):
    """Reflexive if all diagonal entries are 1 (within eps). Returns dict."""
    if not _is_square(R):
        return {"applicable": False, "is_reflexive": None, "min_diag": None, "note": "Not square"}
    diag = np.diag(R)
    min_diag = float(np.min(diag)) if diag.size else 0.0
    is_reflexive = bool(np.all(np.abs(diag - 1.0) <= eps))
    return {"applicable": True, "is_reflexive": is_reflexive, "min_diag": round(min_diag, 3)}

def check_symmetry(R: np.ndarray, eps: float = 1e-6):
    """Symmetric if R[i,j] == R[j,i] for all i,j (within eps). Returns dict."""
    if not _is_square(R):
        return {"applicable": False, "is_symmetric": None, "max_diff": None, "note": "Not square"}
    diff = np.abs(R - R.T)
    max_diff = float(np.max(diff)) if diff.size else 0.0
    is_symmetric = bool(max_diff <= eps)
    return {"applicable": True, "is_symmetric": is_symmetric, "max_diff": round(max_diff, 3)}

def check_transitivity(R: np.ndarray, comp_type: str = "Max-Min", eps: float = 1e-6):
    """Transitive (for fuzzy relations) if (R∘R) ⊆ R under selected composition.
    Returns dict with boolean and max violation.
    """
    if not _is_square(R):
        return {"applicable": False, "is_transitive": None, "max_violation": None, "note": "Not square"}

    if comp_type == "Max-Product":
        T = max_product_composition(R, R)
    else:
        T = max_min_composition(R, R)

    violation = np.maximum(T - R, 0)
    max_violation = float(np.max(violation)) if violation.size else 0.0
    is_transitive = bool(max_violation <= eps)
    return {"applicable": True, "is_transitive": is_transitive, "max_violation": round(max_violation, 3)}

def check_all_properties(R: np.ndarray, comp_type: str = "Max-Min", eps: float = 1e-6):
    """Aggregate all checks into one dictionary."""
    return {
        "reflexivity": check_reflexivity(R, eps),
        "symmetry": check_symmetry(R, eps),
        "transitivity": check_transitivity(R, comp_type, eps),
    }
