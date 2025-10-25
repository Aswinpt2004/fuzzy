import numpy as np

def cartesian_product(A, B):
    return np.fmin.outer(A, B)

def max_min_composition(R, S):
    return np.max(np.minimum(R[:, np.newaxis, :], S[np.newaxis, :, :]), axis=2)
