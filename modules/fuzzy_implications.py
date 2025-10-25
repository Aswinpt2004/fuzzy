import numpy as np

def mamdani_implication(A, B):
    return np.fmin(A, B)

def larsen_implication(A, B):
    return np.multiply(A, B)

def zadeh_implication(A, B):
    return np.fmax(1 - A, B)
