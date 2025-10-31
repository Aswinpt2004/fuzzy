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
