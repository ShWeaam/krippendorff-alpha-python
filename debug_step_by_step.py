#!/usr/bin/env python3
"""
Step-by-step debug of Krippendorff Alpha calculation to find the error
"""

import numpy as np
import pandas as pd
from collections import Counter

def debug_krippendorff_detailed(data, level='nominal'):
    """
    Manual step-by-step calculation following Krippendorff's exact formulation
    """
    print(f"=== DETAILED KRIPPENDORFF ALPHA DEBUG ({level} scale) ===")
    
    # Convert to numpy array
    arr = np.array(data, dtype=object)
    n_items, n_raters = arr.shape
    print(f"Data shape: {n_items} items × {n_raters} raters")
    
    # Step 1: Identify missing values
    missing_mask = np.array([[pd.isna(val) or val is None for val in row] for row in arr])
    print(f"Missing values: {missing_mask.sum()} out of {n_items * n_raters}")
    
    # Step 2: Collect all pairable values (from items with 2+ ratings)
    all_values = []
    valid_pairs = []
    
    print("\nPairable values by item:")
    for i in range(n_items):
        item_values = [arr[i, j] for j in range(n_raters) if not missing_mask[i, j]]
        if len(item_values) >= 2:
            all_values.extend(item_values)
            print(f"  Item {i+1}: {item_values} ({len(item_values)} values)")
            # Count unique pairs for this item
            for a in range(len(item_values)):
                for b in range(a + 1, len(item_values)):
                    valid_pairs.append((item_values[a], item_values[b]))
        else:
            print(f"  Item {i+1}: {item_values} (skipped - need 2+ values)")
    
    print(f"\nTotal pairable values: {len(all_values)}")
    print(f"Total unique pairs: {len(valid_pairs)}")
    
    # Step 3: Value frequencies
    value_counts = Counter(all_values)
    unique_values = sorted(value_counts.keys())
    print(f"\nValue frequencies:")
    for val in unique_values:
        print(f"  {val}: {value_counts[val]} times")
    
    n_total = len(all_values)
    print(f"Total values (n): {n_total}")
    
    # Step 4: Distance function
    def delta_nominal(v1, v2):
        return 0.0 if v1 == v2 else 1.0
    
    # Step 5: Calculate OBSERVED disagreement
    print(f"\n=== OBSERVED DISAGREEMENT ===")
    observed_sum = 0.0
    
    print("Pair-by-pair calculation:")
    for i, (v1, v2) in enumerate(valid_pairs):
        delta_val = delta_nominal(v1, v2)
        observed_sum += delta_val
        if i < 10 or delta_val > 0:  # Show first 10 or disagreements
            print(f"  Pair {i+1}: delta({v1}, {v2}) = {delta_val}")
    
    d_observed = observed_sum / len(valid_pairs) if valid_pairs else 0.0
    print(f"\nD_observed = {observed_sum} / {len(valid_pairs)} = {d_observed:.6f}")
    
    # Step 6: Calculate EXPECTED disagreement (Krippendorff's formula)
    print(f"\n=== EXPECTED DISAGREEMENT ===")
    print("Krippendorff formula: D_e = Sum_c Sum_c' [n_c * n_c' / (n * (n-1))] * delta(c, c')")
    print("where for c != c': use n_c * n_c'")
    print("      for c = c': use n_c * (n_c - 1)")
    
    expected_sum = 0.0
    
    for i, v1 in enumerate(unique_values):
        for j, v2 in enumerate(unique_values):
            n_c = value_counts[v1]
            n_c_prime = value_counts[v2]
            
            if i != j:  # Different values
                numerator = n_c * n_c_prime
                prob = numerator / (n_total * (n_total - 1))
                delta_val = delta_nominal(v1, v2)
                contribution = prob * delta_val
                expected_sum += contribution
                print(f"  delta({v1}, {v2}): ({n_c} x {n_c_prime}) / ({n_total} x {n_total-1}) x {delta_val} = {contribution:.6f}")
            
            elif i == j and n_c > 1:  # Same value, multiple instances
                numerator = n_c * (n_c - 1)
                prob = numerator / (n_total * (n_total - 1))
                delta_val = delta_nominal(v1, v2)  # Should be 0
                contribution = prob * delta_val
                expected_sum += contribution
                print(f"  delta({v1}, {v2}) [same]: ({n_c} x {n_c-1}) / ({n_total} x {n_total-1}) x {delta_val} = {contribution:.6f}")
    
    d_expected = expected_sum
    print(f"\nD_expected = {d_expected:.6f}")
    
    # Step 7: Calculate alpha
    print(f"\n=== ALPHA CALCULATION ===")
    if d_expected == 0:
        alpha = 1.0 if d_observed == 0 else float('-inf')
        print(f"D_expected = 0, alpha = {alpha}")
    else:
        alpha = 1.0 - (d_observed / d_expected)
        print(f"alpha = 1 - (D_observed / D_expected)")
        print(f"alpha = 1 - ({d_observed:.6f} / {d_expected:.6f})")
        print(f"alpha = 1 - {d_observed/d_expected:.6f}")
        print(f"alpha = {alpha:.6f}")
    
    return alpha

# Test with k-alpha.org sample data
if __name__ == "__main__":
    sample_data = [
        [1, 1, np.nan, 1],
        [2, 2, 3, 2], 
        [3, 3, 3, 3],
        [3, 3, 3, 3],
        [2, 2, 2, 2],
        [1, 2, 3, 4],
        [4, 4, 4, 4], 
        [1, 1, 2, 1],
        [2, 2, 2, 2],
        [np.nan, 5, 5, 5],
        [np.nan, np.nan, 1, 1],
        [np.nan, 3, np.nan, np.nan]
    ]
    
    print("Testing k-alpha.org sample data:")
    print("Expected result: alpha ~= 0.33")
    print("Current result from our implementation: alpha ~= 0.72")
    print()
    
    manual_alpha = debug_krippendorff_detailed(sample_data)
    print(f"\n*** MANUAL CALCULATION RESULT: alpha = {manual_alpha:.6f} ***")