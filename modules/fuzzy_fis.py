import skfuzzy as fuzz
import numpy as np

def defuzzify(x, mf, method="centroid"):
    return fuzz.defuzz(x, mf, method)
