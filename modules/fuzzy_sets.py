# modules/fuzzy_sets.py
import numpy as np

def union(A, B):
    return np.fmax(A, B)

def intersection(A, B):
    return np.fmin(A, B)

def complement(A):
    return 1 - np.array(A)

def algebraic_sum(A, B):
    return np.clip(A + B - A * B, 0, 1)

def algebraic_product(A, B):
    return np.array(A) * np.array(B)

def bounded_sum(A, B):
    return np.clip(A + B, 0, 1)

def bounded_difference(A, B):
    return np.clip(A - B, 0, 1)
