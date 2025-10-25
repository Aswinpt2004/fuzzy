import numpy as np

def triangular(x, a, b, c):
    return np.maximum(np.minimum((x - a)/(b - a), (c - x)/(c - b)), 0)

def trapezoidal(x, a, b, c, d):
    return np.maximum(np.minimum(np.minimum((x - a)/(b - a), 1), (d - x)/(d - c)), 0)

def gaussian(x, mean, sigma):
    return np.exp(-0.5 * ((x - mean)/sigma)**2)
