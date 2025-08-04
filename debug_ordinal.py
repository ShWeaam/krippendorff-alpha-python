#!/usr/bin/env python3
"""
Debug Krippendorff Alpha Ordinal Distance Function
Compare our implementation with theoretical expectations
"""

import numpy as np
from krippendorff_alpha import krippendorff_alpha
from collections import Counter

def debug_ordinal_distance():
    """Debug the ordinal distance function step by step"""
    
    print("DEBUGGING ORDINAL DISTANCE FUNCTION")
    print("="*50)
    
    # Simple test case with known ordinal structure
    test_data = [
        [1, 1, 2, 1],  # Mostly 1s with one 2
        [2, 2, 2, 2],  # All 2s  
        [3, 3, 3, 3],  # All 3s
        [1, 2, 1, 2],  # Mixed 1s and 2s
        [2, 3, 2, 3],  # Mixed 2s and 3s
    ]
    
    print("Test data:")
    for i, row in enumerate(test_data):
        print(f"  Item {i+1}: {row}")
    
    # Calculate with different scales
    print(f"\nComparison across measurement levels:")
    for level in ['nominal', 'ordinal', 'interval', 'ratio']:
        try:
            alpha = krippendorff_alpha(test_data, level=level)
            print(f"  {level.capitalize():>8}: α = {alpha:.6f}")
        except Exception as e:
            print(f"  {level.capitalize():>8}: Error - {e}")
    
    # Manual ordinal distance calculation for verification
    print(f"\nManual ordinal distance verification:")
    print("-" * 40)
    
    # Collect all values and frequencies
    all_values = []
    for row in test_data:
        all_values.extend(row)
    
    freq = Counter(all_values)
    sorted_vals = sorted(freq.keys())
    n_total = len(all_values)
    
    print(f"Values: {sorted_vals}")
    print(f"Frequencies: {dict(freq)}")
    print(f"Total values: {n_total}")
    
    # Calculate marginal probabilities
    prob = {val: freq[val] / n_total for val in sorted_vals}
    print(f"Probabilities: {prob}")
    
    # Test specific ordinal distances
    print(f"\nOrdinal distance examples:")
    test_pairs = [(1, 2), (1, 3), (2, 3)]
    
    for v1, v2 in test_pairs:
        if v1 in sorted_vals and v2 in sorted_vals:
            i = sorted_vals.index(v1)
            j = sorted_vals.index(v2)
            
            if i > j:
                i, j = j, i
                v1, v2 = v2, v1
            
            # Current implementation: sum of squared probabilities
            distance = 0.0
            print(f"  δ({v1}, {v2}):")
            for k in range(i + 1, j + 1):
                if k < len(sorted_vals):
                    val_k = sorted_vals[k]
                    prob_k = prob[val_k]
                    contribution = prob_k ** 2
                    distance += contribution
                    print(f"    + P({val_k})² = {prob_k:.4f}² = {contribution:.6f}")
            
            print(f"    Total: {distance:.6f}")

def test_alternative_ordinal_formula():
    """Test alternative ordinal distance formulations"""
    
    print(f"\n" + "="*50)
    print("TESTING ALTERNATIVE ORDINAL FORMULATIONS")
    print("="*50)
    
    test_data = [
        [1, 1, 1, 1],
        [2, 2, 2, 2], 
        [3, 3, 3, 3],
        [1, 2, 1, 2],
        [2, 3, 2, 3],
    ]
    
    # Our current implementation
    alpha_current = krippendorff_alpha(test_data, level='ordinal')
    print(f"Current implementation: α = {alpha_current:.6f}")
    
    # Compare with other libraries if available
    try:
        import krippendorff
        data_transposed = np.array(test_data).T
        alpha_ref = krippendorff.alpha(data_transposed, level_of_measurement='ordinal')
        print(f"Reference library: α = {alpha_ref:.6f}")
        diff = abs(alpha_current - alpha_ref)
        print(f"Difference: {diff:.6f}")
        
        if diff > 0.001:
            print("⚠️ SIGNIFICANT DIFFERENCE detected!")
        else:
            print("✅ Results are similar")
            
    except ImportError:
        print("Reference krippendorff library not available")

def test_with_simple_ordinal_case():
    """Test with a very simple ordinal case"""
    
    print(f"\n" + "="*50)
    print("SIMPLE ORDINAL TEST CASE")
    print("="*50)
    
    # Very simple case: just 3 items, 2 raters, 3 ordinal levels
    simple_data = [
        [1, 1],  # Perfect agreement on rank 1
        [2, 2],  # Perfect agreement on rank 2  
        [1, 3],  # Maximum disagreement (rank 1 vs rank 3)
    ]
    
    print("Simple test data:")
    for i, row in enumerate(simple_data):
        print(f"  Item {i+1}: {row}")
    
    alpha = krippendorff_alpha(simple_data, level='ordinal')
    print(f"\nOrdinal alpha: {alpha:.6f}")
    
    # Expected: Some positive agreement due to 2/3 items having perfect agreement
    # But lower than nominal due to the ordinal distance being larger for 1 vs 3
    
    alpha_nominal = krippendorff_alpha(simple_data, level='nominal') 
    print(f"Nominal alpha:  {alpha_nominal:.6f}")
    print(f"Difference:     {alpha_nominal - alpha:.6f}")
    
    if alpha < alpha_nominal:
        print("✅ Ordinal < Nominal (expected for rank-based data)")
    else:
        print("⚠️ Unexpected: Ordinal >= Nominal")

if __name__ == "__main__":
    debug_ordinal_distance()
    test_alternative_ordinal_formula()
    test_with_simple_ordinal_case()