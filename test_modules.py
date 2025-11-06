"""
Module Connection Test
Tests that all modules can be imported and their key functions work
"""
import sys
import numpy as np

def test_imports():
    """Test that all modules can be imported"""
    print("=" * 60)
    print("TESTING MODULE IMPORTS")
    print("=" * 60)
    
    try:
        from modules import fuzzy_sets
        print("✅ fuzzy_sets imported successfully")
    except Exception as e:
        print(f"❌ fuzzy_sets import failed: {e}")
        return False
    
    try:
        from modules import fuzzy_membership
        print("✅ fuzzy_membership imported successfully")
    except Exception as e:
        print(f"❌ fuzzy_membership import failed: {e}")
        return False
    
    try:
        from modules import fuzzy_relations
        print("✅ fuzzy_relations imported successfully")
    except Exception as e:
        print(f"❌ fuzzy_relations import failed: {e}")
        return False
    
    try:
        from modules import fuzzy_implications
        print("✅ fuzzy_implications imported successfully")
    except Exception as e:
        print(f"❌ fuzzy_implications import failed: {e}")
        return False
    
    try:
        from modules import defuzzification
        print("✅ defuzzification imported successfully")
    except Exception as e:
        print(f"❌ defuzzification import failed: {e}")
        return False
    
    try:
        from modules import fuzzy_tnorms
        print("✅ fuzzy_tnorms imported successfully")
    except Exception as e:
        print(f"❌ fuzzy_tnorms import failed: {e}")
        return False
    
    try:
        from modules import fuzzy_inference
        print("✅ fuzzy_inference imported successfully")
    except Exception as e:
        print(f"❌ fuzzy_inference import failed: {e}")
        return False
    
    try:
        from modules import fuzzy_rules
        print("✅ fuzzy_rules imported successfully")
    except Exception as e:
        print(f"❌ fuzzy_rules import failed: {e}")
        return False
    
    return True


def test_basic_functionality():
    """Test basic functionality of each module"""
    print("\n" + "=" * 60)
    print("TESTING BASIC FUNCTIONALITY")
    print("=" * 60)
    
    from modules import fuzzy_sets, fuzzy_membership, fuzzy_relations
    from modules import fuzzy_implications, defuzzification, fuzzy_tnorms
    from modules import fuzzy_inference, fuzzy_rules
    
    # Test fuzzy_sets
    try:
        A = np.array([0.2, 0.5, 0.8, 1.0])
        B = np.array([0.3, 0.6, 0.7, 0.9])
        result = fuzzy_sets.union(A, B)
        assert result is not None
        print("✅ fuzzy_sets.union() works")
    except Exception as e:
        print(f"❌ fuzzy_sets.union() failed: {e}")
    
    # Test fuzzy_membership
    try:
        x = 5
        result = fuzzy_membership.triangular(x, 0, 5, 10)
        assert result is not None
        print("✅ fuzzy_membership.triangular() works")
    except Exception as e:
        print(f"❌ fuzzy_membership.triangular() failed: {e}")
    
    # Test fuzzy_relations
    try:
        R = np.array([[0.2, 0.5], [0.8, 0.3]])
        S = np.array([[0.6, 0.4], [0.7, 0.9]])
        result = fuzzy_relations.max_min_composition(R, S)
        assert result is not None
        print("✅ fuzzy_relations.max_min_composition() works")
    except Exception as e:
        print(f"❌ fuzzy_relations.max_min_composition() failed: {e}")
    
    # Test fuzzy_implications
    try:
        A = np.array([0.2, 0.5, 0.8])
        B = np.array([0.3, 0.6, 0.9])
        result = fuzzy_implications.mamdani_implication(A, B)
        assert result is not None
        print("✅ fuzzy_implications.mamdani_implication() works")
    except Exception as e:
        print(f"❌ fuzzy_implications.mamdani_implication() failed: {e}")
    
    # Test defuzzification
    try:
        y = np.linspace(0, 10, 50)
        mu = np.random.rand(50)
        result = defuzzification.centroid(y, mu)
        assert result is not None
        print("✅ defuzzification.centroid() works")
    except Exception as e:
        print(f"❌ defuzzification.centroid() failed: {e}")
    
    # Test lambda_cut_defuzzification
    try:
        y = np.linspace(0, 10, 50)
        mu = np.random.rand(50)
        result = defuzzification.lambda_cut_defuzzification(y, mu, 0.5)
        assert result is not None
        print("✅ defuzzification.lambda_cut_defuzzification() works")
    except Exception as e:
        print(f"❌ defuzzification.lambda_cut_defuzzification() failed: {e}")
    
    # Test fuzzy_tnorms
    try:
        result = fuzzy_tnorms.minimum_tnorm(0.7, 0.5)
        assert result == 0.5
        print("✅ fuzzy_tnorms.minimum_tnorm() works")
    except Exception as e:
        print(f"❌ fuzzy_tnorms.minimum_tnorm() failed: {e}")
    
    # Test fuzzy_inference
    try:
        A_prime = np.array([0.2, 0.5, 0.8, 1.0])
        R = np.outer(A_prime, A_prime)
        result = fuzzy_inference.generalized_modus_ponens(A_prime, R)
        assert result is not None
        print("✅ fuzzy_inference.generalized_modus_ponens() works")
    except Exception as e:
        print(f"❌ fuzzy_inference.generalized_modus_ponens() failed: {e}")
    
    # Test fuzzy_rules
    try:
        A = np.array([0.0, 0.5, 1.0, 0.5, 0.0])
        B = np.array([0.0, 0.3, 0.7, 1.0, 0.8])
        rule = fuzzy_rules.FuzzyRule("Low", "Slow", A, B, 'mamdani')
        print("✅ fuzzy_rules.FuzzyRule() works")
    except Exception as e:
        print(f"❌ fuzzy_rules.FuzzyRule() failed: {e}")


def test_defuzzification_methods():
    """Test all defuzzification methods"""
    print("\n" + "=" * 60)
    print("TESTING ALL DEFUZZIFICATION METHODS")
    print("=" * 60)
    
    from modules import defuzzification
    
    y = np.linspace(0, 100, 50)
    mu = np.random.rand(50)
    
    methods = [
        'height', 'fom', 'lom', 'mom',
        'centroid', 'cog', 'cos', 'coa',
        'bisector', 'wtaver'
    ]
    
    for method in methods:
        try:
            func = defuzzification.get_defuzzification_method(method)
            if method == 'cos':
                # CoS needs list of arrays
                result = func(y, [mu])
            else:
                result = func(y, mu)
            assert result is not None
            print(f"✅ {method}: {result:.2f}")
        except Exception as e:
            print(f"❌ {method} failed: {e}")
    
    # Test lambda-cut separately
    try:
        result = defuzzification.lambda_cut_defuzzification(y, mu, 0.5, 'centroid')
        assert result is not None
        print(f"✅ lambda_cut: {result:.2f}")
    except Exception as e:
        print(f"❌ lambda_cut failed: {e}")


def test_factory_functions():
    """Test all factory/getter functions"""
    print("\n" + "=" * 60)
    print("TESTING FACTORY FUNCTIONS")
    print("=" * 60)
    
    from modules import fuzzy_tnorms, fuzzy_implications, defuzzification, fuzzy_inference
    
    # Test T-norm getter
    try:
        tnorm = fuzzy_tnorms.get_tnorm('minimum')
        assert callable(tnorm)
        print("✅ fuzzy_tnorms.get_tnorm() works")
    except Exception as e:
        print(f"❌ fuzzy_tnorms.get_tnorm() failed: {e}")
    
    # Test implication getter
    try:
        impl = fuzzy_implications.get_implication_method('mamdani')
        assert callable(impl)
        print("✅ fuzzy_implications.get_implication_method() works")
    except Exception as e:
        print(f"❌ fuzzy_implications.get_implication_method() failed: {e}")
    
    # Test defuzzification getter
    try:
        defuzz = defuzzification.get_defuzzification_method('centroid')
        assert callable(defuzz)
        print("✅ defuzzification.get_defuzzification_method() works")
    except Exception as e:
        print(f"❌ defuzzification.get_defuzzification_method() failed: {e}")
    
    # Test inference getter
    try:
        inf = fuzzy_inference.get_inference_method('gmp')
        assert callable(inf)
        print("✅ fuzzy_inference.get_inference_method() works")
    except Exception as e:
        print(f"❌ fuzzy_inference.get_inference_method() failed: {e}")


if __name__ == "__main__":
    print("\n" + "🧪 FUZZY SYSTEM MODULE CONNECTION TEST" + "\n")
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Fix imports before continuing.")
        sys.exit(1)
    
    # Test basic functionality
    test_basic_functionality()
    
    # Test defuzzification methods
    test_defuzzification_methods()
    
    # Test factory functions
    test_factory_functions()
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS COMPLETED!")
    print("=" * 60)
