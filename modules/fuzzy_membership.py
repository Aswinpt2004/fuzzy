import numpy as np

def triangular(x, a, b, c):
    return np.maximum(np.minimum((x - a)/(b - a), (c - x)/(c - b)), 0)

def trapezoidal(x, a, b, c, d):
    return np.maximum(np.minimum(np.minimum((x - a)/(b - a), 1), (d - x)/(d - c)), 0)

def gaussian(x, mean, sigma):
    return np.exp(-0.5 * ((x - mean)/sigma)**2)

def bell_shaped(x, a, b, c):
    return 1 / (1 + np.abs((x - c)/a) ** (2 * b))

def sigmoid(x, a, c):
    return 1 / (1 + np.exp(-a * (x - c)))