#!/usr/bin/env python3
"""
Debug version to manually trace Krippendorff Alpha calculation
"""

import numpy as np
import pandas as pd
from collections import Counter

def debug_krippendorff(data, level='nominal'):
    """
    Debug version of Krippendorff Alpha with step-by-step output
    """
    print(f"=== DEBUG KRIPPENDORFF ALPHA ({level} scale) ===")
    print(f"Input data: {data}")
    
    # Convert to numpy array
    arr = np.array(data, dtype=object)
    n_items, n_raters = arr.shape
    print(f"Shape: {n_items} items × {n_raters} raters")
    
    # Step 1: Collect all valid values
    all_values = []
    valid_pairs = []
    
    for i in range(n_items):
        item_values = [val for val in arr[i] if val is not None and not pd.isna(val)]
        if len(item_values) >= 2:
            all_values.extend(item_values)
            # Collect all pairs for this item
            for a in range(len(item_values)):
                for b in range(a + 1, len(item_values)):
                    valid_pairs.append((item_values[a], item_values[b]))
    
    print(f"All values: {all_values}")
    print(f"Valid pairs: {valid_pairs}")
    
    # Step 2: Value frequencies
    value_counts = Counter(all_values)
    unique_values = list(value_counts.keys())
    counts = list(value_counts.values())
    n_total = len(all_values)
    
    print(f"Value frequencies: {dict(value_counts)}")
    print(f"Total values: {n_total}")
    
    # Step 3: Distance function
    def delta_nominal(v1, v2):
        return 0.0 if v1 == v2 else 1.0
    
    # Step 4: Calculate observed disagreement
    observed_sum = 0.0
    total_pairs = len(valid_pairs)
    
    print(f"\nObserved disagreement calculation:")
    for i, (v1, v2) in enumerate(valid_pairs):
        delta_val = delta_nominal(v1, v2)
        observed_sum += delta_val
        print(f"  Pair {i+1}: δ({v1}, {v2}) = {delta_val}")
    
    d_observed = observed_sum / total_pairs if total_pairs > 0 else 0.0
    print(f"D_observed = {observed_sum} / {total_pairs} = {d_observed:.4f}")
    
    # Step 5: Calculate expected disagreement  
    expected_sum = 0.0
    
    print(f"\nExpected disagreement calculation:")
    print(f"Formula: Σ Σ (n_c × n_c' / (n_total × (n_total - 1))) × δ(c, c')")
    
    for i, v1 in enumerate(unique_values):
        for j, v2 in enumerate(unique_values):
            if i != j:  # Different values
                prob = (counts[i] * counts[j]) / (n_total * (n_total - 1))
                delta_val = delta_nominal(v1, v2)
                contribution = prob * delta_val
                expected_sum += contribution
                print(f"  δ({v1}, {v2}): ({counts[i]} × {counts[j]}) / ({n_total} × {n_total-1}) × {delta_val} = {contribution:.4f}")
            elif counts[i] > 1:  # Same value with multiple instances
                prob = (counts[i] * (counts[i] - 1)) / (n_total * (n_total - 1))
                delta_val = delta_nominal(v1, v2)  # This should be 0
                contribution = prob * delta_val
                expected_sum += contribution
                print(f"  δ({v1}, {v2}) [same]: ({counts[i]} × {counts[i]-1}) / ({n_total} × {n_total-1}) × {delta_val} = {contribution:.4f}")
    
    d_expected = expected_sum
    print(f"D_expected = {d_expected:.4f}")
    
    # Step 6: Calculate alpha
    if d_expected == 0:
        alpha = 1.0 if d_observed == 0 else float('-inf')
    else:
        alpha = 1.0 - (d_observed / d_expected)
    
    print(f"\nFinal calculation:")
    print(f"α = 1 - (D_observed / D_expected)")
    print(f"α = 1 - ({d_observed:.4f} / {d_expected:.4f})")
    print(f"α = {alpha:.4f}")
    
    return alpha

# Test cases
if __name__ == "__main__":
    print("Testing simple cases:\n")
    
    # Test 1: Perfect agreement
    print("TEST 1: Perfect Agreement")
    data1 = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
    alpha1 = debug_krippendorff(data1)
    print(f"Result: α = {alpha1:.4f} (should be 1.0000)\n")
    
    # Test 2: Complete disagreement 
    print("TEST 2: Complete Disagreement")
    data2 = [[1, 2], [2, 1]]
    alpha2 = debug_krippendorff(data2)
    print(f"Result: α = {alpha2:.4f} (should be ≈ 0.0000)\n")
    
    # Test 3: Mixed case
    print("TEST 3: Mixed Agreement")
    data3 = [[1, 1], [1, 2], [2, 2]]
    alpha3 = debug_krippendorff(data3)
    print(f"Result: α = {alpha3:.4f}\n")