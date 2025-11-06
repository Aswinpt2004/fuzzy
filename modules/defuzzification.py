"""
Defuzzification Methods Module
Converts fuzzy output sets to crisp values using various methods
"""
import numpy as np


def centroid(y, mu):
    """
    Centroid (Center of Gravity) defuzzification
    Formula: y* = ∫y*μ(y)dy / ∫μ(y)dy
    
    Args:
        y: Universe of discourse (numpy array)
        mu: Membership values (numpy array)
    
    Returns:
        Crisp output value (float)
    """
    if np.sum(mu) == 0:
        return np.mean(y)
    return np.sum(y * mu) / np.sum(mu)


def bisector(y, mu):
    """
    Bisector defuzzification - splits area under curve in half
    
    Args:
        y: Universe of discourse (numpy array)
        mu: Membership values (numpy array)
    
    Returns:
        Crisp output value (float)
    """
    total_area = np.sum(mu)
    if total_area == 0:
        return np.mean(y)
    
    cumsum = np.cumsum(mu)
    half_area = total_area / 2
    idx = np.argmin(np.abs(cumsum - half_area))
    return y[idx]


def mean_of_maxima(y, mu):
    """
    Mean of Maxima (MOM) - average of y where μ(y) is maximum
    
    Args:
        y: Universe of discourse (numpy array)
        mu: Membership values (numpy array)
    
    Returns:
        Crisp output value (float)
    """
    max_mu = np.max(mu)
    if max_mu == 0:
        return np.mean(y)
    
    max_indices = np.where(mu == max_mu)[0]
    return np.mean(y[max_indices])


def first_of_maxima(y, mu):
    """
    First of Maxima (FOM) - smallest y where μ(y) is maximum
    
    Args:
        y: Universe of discourse (numpy array)
        mu: Membership values (numpy array)
    
    Returns:
        Crisp output value (float)
    """
    max_mu = np.max(mu)
    if max_mu == 0:
        return y[0]
    
    max_indices = np.where(mu == max_mu)[0]
    return y[max_indices[0]]


def last_of_maxima(y, mu):
    """
    Last of Maxima (LOM) - largest y where μ(y) is maximum
    
    Args:
        y: Universe of discourse (numpy array)
        mu: Membership values (numpy array)
    
    Returns:
        Crisp output value (float)
    """
    max_mu = np.max(mu)
    if max_mu == 0:
        return y[-1]
    
    max_indices = np.where(mu == max_mu)[0]
    return y[max_indices[-1]]


def weighted_average(y, mu):
    """
    Weighted Average defuzzification
    Formula: Σ(y_i × μ_i) / Σμ_i
    
    Args:
        y: Universe of discourse (numpy array)
        mu: Membership values (numpy array)
    
    Returns:
        Crisp output value (float)
    """
    if np.sum(mu) == 0:
        return np.mean(y)
    return np.sum(y * mu) / np.sum(mu)


def center_of_area(y, mu):
    """
    Center of Area (COA) - similar to centroid
    
    Args:
        y: Universe of discourse (numpy array)
        mu: Membership values (numpy array)
    
    Returns:
        Crisp output value (float)
    """
    return centroid(y, mu)


def smallest_of_maximum(y, mu):
    """
    Smallest of Maximum (SOM) - alias for First of Maxima (FOM)
    
    Args:
        y: Universe of discourse (numpy array)
        mu: Membership values (numpy array)
    
    Returns:
        Crisp output value (float)
    """
    return first_of_maxima(y, mu)


def largest_of_maximum(y, mu):
    """
    Largest of Maximum (LOM) - alias for Last of Maxima
    
    Args:
        y: Universe of discourse (numpy array)
        mu: Membership values (numpy array)
    
    Returns:
        Crisp output value (float)
    """
    return last_of_maxima(y, mu)


def height_method(y, mu):
    """
    Height Method (Maxima Method)
    Returns the y value where membership is maximum
    
    This is typically used for singleton output fuzzy sets.
    If multiple points have max membership, returns their mean.
    
    Args:
        y: Universe of discourse (numpy array)
        mu: Membership values (numpy array)
    
    Returns:
        Crisp output value (float)
    """
    return mean_of_maxima(y, mu)


def center_of_sums(y_values, mu_values_list):
    """
    Center of Sums (CoS) Method
    Used for aggregating multiple fuzzy sets before defuzzification
    
    Formula: y* = Σ(Σμ_i(y) × y) / Σ(Σμ_i(y))
    
    This sums the membership functions rather than taking their maximum,
    then applies centroid method.
    
    Args:
        y_values: Universe of discourse (numpy array)
        mu_values_list: List of membership arrays, one per rule
    
    Returns:
        Crisp output value (float)
    """
    if isinstance(mu_values_list, list):
        # Sum all membership functions
        mu_sum = np.sum(mu_values_list, axis=0)
    else:
        mu_sum = mu_values_list
    
    if np.sum(mu_sum) == 0:
        return np.mean(y_values)
    
    return np.sum(y_values * mu_sum) / np.sum(mu_sum)


def lambda_cut(fuzzy_set, lambda_value):
    """
    Lambda-cut (Alpha-cut) operation
    Returns crisp set where membership >= lambda
    
    Formula: A_λ = {x | µ_A(x) ≥ λ}
    
    Args:
        fuzzy_set: Membership values (numpy array)
        lambda_value: Threshold value (0 to 1)
    
    Returns:
        Binary array (1 where µ ≥ λ, 0 elsewhere)
    """
    return (fuzzy_set >= lambda_value).astype(float)


def alpha_cut(fuzzy_set, alpha):
    """
    Alpha-cut operation (alias for lambda-cut)
    
    Args:
        fuzzy_set: Membership values (numpy array)
        alpha: Threshold value (0 to 1)
    
    Returns:
        Binary array (1 where µ ≥ α, 0 elsewhere)
    """
    return lambda_cut(fuzzy_set, alpha)


def lambda_cut_defuzzification(y, mu, lambda_value, method='centroid'):
    """
    Lambda-cut Defuzzification
    
    Process:
    1. Apply lambda-cut to fuzzy set: A_λ = {x | µ_A(x) ≥ λ}
    2. Defuzzify the resulting crisp set using specified method
    
    Args:
        y: Universe of discourse (numpy array)
        mu: Membership values (numpy array)
        lambda_value: Threshold for lambda-cut (0 to 1)
        method: Defuzzification method to apply after cut ('centroid', 'mom', etc.)
    
    Returns:
        Crisp output value (float)
    """
    # Apply lambda-cut
    mu_cut = lambda_cut(mu, lambda_value)
    
    # If cut results in empty set, reduce lambda
    if np.sum(mu_cut) == 0:
        # Find maximum membership and use it
        mu_cut = lambda_cut(mu, np.max(mu) * 0.5)
    
    # Apply selected defuzzification method
    if method == 'centroid' or method == 'cog':
        return centroid(y, mu_cut)
    elif method == 'mom':
        return mean_of_maxima(y, mu_cut)
    elif method == 'fom':
        return first_of_maxima(y, mu_cut)
    elif method == 'lom':
        return last_of_maxima(y, mu_cut)
    else:
        return centroid(y, mu_cut)


def multi_level_lambda_cut(y, mu, lambda_levels=None):
    """
    Multi-level Lambda-cut Defuzzification
    
    Applies multiple lambda cuts and combines results
    Useful for more nuanced defuzzification
    
    Args:
        y: Universe of discourse (numpy array)
        mu: Membership values (numpy array)
        lambda_levels: List of lambda values (default: [0.25, 0.5, 0.75, 1.0])
    
    Returns:
        Crisp output value (float)
    """
    if lambda_levels is None:
        lambda_levels = [0.25, 0.5, 0.75, 1.0]
    
    results = []
    weights = []
    
    for lam in lambda_levels:
        mu_cut = lambda_cut(mu, lam)
        if np.sum(mu_cut) > 0:
            results.append(centroid(y, mu_cut))
            weights.append(lam)  # Higher lambda levels get more weight
    
    if not results:
        return centroid(y, mu)
    
    # Weighted average of results
    return np.average(results, weights=weights)


def get_defuzzification_method(method_name):
    """
    Factory function to get defuzzification method by name
    
    Args:
        method_name: String name of the method
    
    Returns:
        Function reference
    """
    methods = {
        # Centroid methods
        'centroid': centroid,
        'cog': centroid,
        'center_of_gravity': centroid,
        'center_of_area': center_of_area,
        'coa': center_of_area,
        'center_of_sums': center_of_sums,
        'cos': center_of_sums,
        
        # Bisector
        'bisector': bisector,
        
        # Maxima methods (Height method)
        'height': height_method,
        'height_method': height_method,
        'mom': mean_of_maxima,
        'mean_of_maxima': mean_of_maxima,
        'mean_of_maximum': mean_of_maxima,
        'fom': first_of_maxima,
        'first_of_maxima': first_of_maxima,
        'smallest_of_maximum': smallest_of_maximum,
        'som': smallest_of_maximum,
        'lom': last_of_maxima,
        'last_of_maxima': last_of_maxima,
        'largest_of_maximum': largest_of_maximum,
        
        # Weighted average
        'weighted_average': weighted_average,
        'wtaver': weighted_average,
        
        # Lambda-cut
        'lambda_cut': lambda_cut_defuzzification,
        'alpha_cut': lambda_cut_defuzzification,
        'multi_lambda': multi_level_lambda_cut,
    }
    
    return methods.get(method_name.lower(), centroid)


def get_all_methods():
    """
    Get list of all available defuzzification methods
    
    Returns:
        Dictionary with method categories and names
    """
    return {
        'Maxima Methods': [
            ('height', 'Height Method'),
            ('fom', 'First of Maxima (FoM)'),
            ('lom', 'Last of Maxima (LoM)'),
            ('mom', 'Mean of Maxima (MoM)'),
        ],
        'Centroid Methods': [
            ('cog', 'Center of Gravity (CoG)'),
            ('cos', 'Center of Sums (CoS)'),
            ('coa', 'Center of Area (CoA)'),
        ],
        'Other Methods': [
            ('bisector', 'Bisector Method'),
            ('wtaver', 'Weighted Average'),
            ('lambda_cut', 'Lambda-Cut Method'),
        ]
    }
