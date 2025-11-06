"""
Fuzzy Rule Base Management Module
Implements fuzzy IF-THEN rules and rule base management for fuzzy inference systems.

Rule format: IF x is A THEN y is B
where A and B are fuzzy sets representing linguistic terms.
"""
import numpy as np
from modules import fuzzy_implications, fuzzy_tnorms


class FuzzyRule:
    """
    Represents a single fuzzy IF-THEN rule
    
    Attributes:
        antecedent: Fuzzy set or label for input (A)
        consequent: Fuzzy set or label for output (B)
        implication_type: Type of implication operator
        tnorm: T-norm operator for conjunction
        weight: Rule weight/importance (0-1)
    """
    
    def __init__(self, antecedent_label, consequent_label, 
                 antecedent_values=None, consequent_values=None,
                 implication_type='mamdani', tnorm='minimum', weight=1.0):
        """
        Initialize fuzzy rule
        
        Args:
            antecedent_label: String label (e.g., "Temperature is High")
            consequent_label: String label (e.g., "Fan is Fast")
            antecedent_values: Optional numpy array of membership values
            consequent_values: Optional numpy array of membership values
            implication_type: 'mamdani', 'larsen', 'zadeh', etc.
            tnorm: T-norm operator name
            weight: Rule importance (default 1.0)
        """
        self.antecedent_label = antecedent_label
        self.consequent_label = consequent_label
        self.antecedent_values = antecedent_values
        self.consequent_values = consequent_values
        self.implication_type = implication_type
        self.tnorm = tnorm
        self.weight = weight
        
        # Get implication and tnorm functions
        self.implication_func = fuzzy_implications.get_implication_method(implication_type)
        self.tnorm_func = fuzzy_tnorms.get_tnorm(tnorm)
    
    def evaluate(self, input_fuzzy_set):
        """
        Evaluate rule with given fuzzy input
        
        Uses Generalized Modus Ponens:
        IF x is A THEN y is B
        x is A'
        ⇒ y is B'
        
        Args:
            input_fuzzy_set: Observed input fuzzy set (A')
        
        Returns:
            Output fuzzy set (B')
        """
        if self.antecedent_values is None or self.consequent_values is None:
            raise ValueError("Rule must have antecedent and consequent values to evaluate")
        
        # Generate implication relation R(x,y)
        R = self.implication_func(self.antecedent_values, self.consequent_values)
        
        # Generalized Modus Ponens: B'(y) = max_x [min(A'(x), R(x,y))]
        # For each output y, find max over all inputs x
        output = np.zeros(len(self.consequent_values))
        
        for j in range(len(self.consequent_values)):
            # For each output element y_j
            conjunction = self.tnorm_func(input_fuzzy_set, R[:, j])
            output[j] = np.max(conjunction)
        
        # Apply rule weight
        output = output * self.weight
        
        return output
    
    def get_relation_matrix(self):
        """
        Get the fuzzy relation matrix R(x,y) for this rule
        
        Returns:
            2D numpy array representing the implication relation
        """
        if self.antecedent_values is None or self.consequent_values is None:
            return None
        
        return self.implication_func(self.antecedent_values, self.consequent_values)
    
    def __str__(self):
        """Human-readable rule representation"""
        return f"IF {self.antecedent_label} THEN {self.consequent_label} (weight={self.weight}, impl={self.implication_type})"
    
    def __repr__(self):
        return self.__str__()


class FuzzyRuleBase:
    """
    Collection of fuzzy rules forming a rule base
    
    Manages multiple rules and provides aggregation of rule outputs.
    """
    
    def __init__(self, aggregation_method='maximum'):
        """
        Initialize rule base
        
        Args:
            aggregation_method: Method to combine rule outputs ('maximum', 'sum', 'probsum')
        """
        self.rules = []
        self.aggregation_method = aggregation_method
    
    def add_rule(self, rule):
        """
        Add a rule to the rule base
        
        Args:
            rule: FuzzyRule object
        """
        if not isinstance(rule, FuzzyRule):
            raise TypeError("Must add FuzzyRule object")
        
        self.rules.append(rule)
    
    def remove_rule(self, index):
        """
        Remove rule at given index
        
        Args:
            index: Index of rule to remove
        """
        if 0 <= index < len(self.rules):
            del self.rules[index]
    
    def clear_rules(self):
        """Remove all rules"""
        self.rules = []
    
    def evaluate_all(self, input_fuzzy_set):
        """
        Evaluate all rules with given input
        
        Args:
            input_fuzzy_set: Observed fuzzy input
        
        Returns:
            List of output fuzzy sets (one per rule)
        """
        outputs = []
        for rule in self.rules:
            try:
                output = rule.evaluate(input_fuzzy_set)
                outputs.append(output)
            except Exception as e:
                print(f"Warning: Rule evaluation failed: {rule} - {e}")
        
        return outputs
    
    def aggregate(self, outputs):
        """
        Aggregate multiple rule outputs into single fuzzy set
        
        Args:
            outputs: List of fuzzy sets (rule outputs)
        
        Returns:
            Aggregated fuzzy set
        """
        if not outputs:
            return np.array([])
        
        outputs_array = np.array(outputs)
        
        if self.aggregation_method == 'maximum' or self.aggregation_method == 'max':
            # Standard FIS aggregation: max(B1', B2', ..., Bn')
            return np.max(outputs_array, axis=0)
        
        elif self.aggregation_method == 'sum':
            # Sum aggregation (may exceed 1)
            return np.sum(outputs_array, axis=0)
        
        elif self.aggregation_method == 'probsum':
            # Probabilistic sum: a + b - ab
            result = outputs_array[0]
            for i in range(1, len(outputs_array)):
                result = result + outputs_array[i] - result * outputs_array[i]
            return np.clip(result, 0, 1)
        
        elif self.aggregation_method == 'mean':
            # Average of all outputs
            return np.mean(outputs_array, axis=0)
        
        else:
            # Default to maximum
            return np.max(outputs_array, axis=0)
    
    def infer(self, input_fuzzy_set):
        """
        Complete inference: evaluate all rules and aggregate
        
        Args:
            input_fuzzy_set: Observed fuzzy input
        
        Returns:
            Aggregated output fuzzy set
        """
        outputs = self.evaluate_all(input_fuzzy_set)
        return self.aggregate(outputs)
    
    def __len__(self):
        """Number of rules in rule base"""
        return len(self.rules)
    
    def __getitem__(self, index):
        """Get rule at index"""
        return self.rules[index]
    
    def __str__(self):
        """Human-readable rule base representation"""
        s = f"Fuzzy Rule Base ({len(self.rules)} rules, aggregation={self.aggregation_method}):\n"
        for i, rule in enumerate(self.rules):
            s += f"  {i+1}. {rule}\n"
        return s


# ========================================
# STANDALONE FUNCTIONS
# ========================================

def create_rule(antecedent_label, consequent_label, 
                antecedent_values=None, consequent_values=None,
                implication_type='mamdani', weight=1.0):
    """
    Factory function to create a fuzzy rule
    
    Args:
        antecedent_label: String label for input
        consequent_label: String label for output
        antecedent_values: Optional fuzzy set values
        consequent_values: Optional fuzzy set values
        implication_type: Implication operator
        weight: Rule weight
    
    Returns:
        FuzzyRule object
    """
    return FuzzyRule(
        antecedent_label, consequent_label,
        antecedent_values, consequent_values,
        implication_type, weight=weight
    )


def combine_rules(rule1, rule2, operator='OR'):
    """
    Combine two rules using logical operator
    
    Args:
        rule1, rule2: FuzzyRule objects
        operator: 'OR' (union) or 'AND' (intersection)
    
    Returns:
        Combined FuzzyRule
    
    Note: This creates a new rule with combined consequents
    """
    if operator.upper() == 'OR':
        # Union of consequents
        combined_label = f"({rule1.consequent_label} OR {rule2.consequent_label})"
        if rule1.consequent_values is not None and rule2.consequent_values is not None:
            combined_values = np.maximum(rule1.consequent_values, rule2.consequent_values)
        else:
            combined_values = None
    
    elif operator.upper() == 'AND':
        # Intersection of consequents
        combined_label = f"({rule1.consequent_label} AND {rule2.consequent_label})"
        if rule1.consequent_values is not None and rule2.consequent_values is not None:
            combined_values = np.minimum(rule1.consequent_values, rule2.consequent_values)
        else:
            combined_values = None
    
    else:
        raise ValueError("Operator must be 'OR' or 'AND'")
    
    # Use antecedent from first rule (assuming same antecedent)
    return FuzzyRule(
        rule1.antecedent_label,
        combined_label,
        rule1.antecedent_values,
        combined_values,
        rule1.implication_type
    )


def rule_if_then_else(A, B, C, A_label="A", B_label="B", C_label="C"):
    """
    Create IF-THEN-ELSE rule
    
    Formula: R = (A×B) ∪ (Ā×C)
    
    Rule: IF x is A THEN y is B ELSE y is C
    
    Args:
        A: Antecedent fuzzy set
        B: Primary consequent fuzzy set (when A is true)
        C: Alternative consequent fuzzy set (when A is false)
        A_label, B_label, C_label: String labels
    
    Returns:
        FuzzyRule representing the IF-THEN-ELSE structure
    """
    # Complement of A
    A_complement = 1 - A
    
    # Create two sub-rules
    rule_then = FuzzyRule(
        A_label, B_label,
        A, B,
        'mamdani'
    )
    
    rule_else = FuzzyRule(
        f"NOT {A_label}", C_label,
        A_complement, C,
        'mamdani'
    )
    
    # Combine with OR
    combined_rule = combine_rules(rule_then, rule_else, operator='OR')
    combined_rule.antecedent_label = A_label
    combined_rule.consequent_label = f"IF {A_label} THEN {B_label} ELSE {C_label}"
    
    return combined_rule


def parse_rule_string(rule_str):
    """
    Parse natural language rule string
    
    Example: "IF Temperature is High THEN Fan is Fast"
    
    Args:
        rule_str: String representation of rule
    
    Returns:
        Tuple (antecedent_label, consequent_label)
    """
    rule_str = rule_str.strip().upper()
    
    if 'IF' not in rule_str or 'THEN' not in rule_str:
        raise ValueError("Rule must contain 'IF' and 'THEN'")
    
    # Split by IF and THEN
    parts = rule_str.split('IF')[1].split('THEN')
    
    antecedent = parts[0].strip()
    consequent = parts[1].strip()
    
    return antecedent, consequent


def create_rule_from_string(rule_str, antecedent_values=None, consequent_values=None,
                            implication_type='mamdani'):
    """
    Create fuzzy rule from natural language string
    
    Args:
        rule_str: String like "IF Temperature is High THEN Fan is Fast"
        antecedent_values: Optional fuzzy set values
        consequent_values: Optional fuzzy set values
        implication_type: Implication operator
    
    Returns:
        FuzzyRule object
    """
    antecedent, consequent = parse_rule_string(rule_str)
    
    return FuzzyRule(
        antecedent, consequent,
        antecedent_values, consequent_values,
        implication_type
    )
