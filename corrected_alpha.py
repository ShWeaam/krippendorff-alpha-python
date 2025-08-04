#!/usr/bin/env python3
"""
CORRECTED Krippendorff Alpha Implementation
Based on theoretical research - the issue is likely in expected disagreement calculation
"""

import numpy as np
import pandas as pd
from collections import Counter

def corrected_krippendorff_alpha(data, level='nominal'):
    """
    Corrected implementation based on research findings
    The key insight: expected disagreement calculation may be wrong
    """
    print(f"=== CORRECTED KRIPPENDORFF ALPHA ({level} scale) ===")
    
    # Convert to numpy array
    arr = np.array(data, dtype=object)
    n_items, n_raters = arr.shape
    print(f"Data shape: {n_items} items × {n_raters} raters")
    
    # Identify missing values
    missing_mask = np.array([[pd.isna(val) or val is None for val in row] for row in arr])
    
    # Collect pairable values - this is crucial
    all_pairable_values = []
    coincidence_pairs = []  # Store (v1, v2) pairs for coincidence matrix
    
    print("\nCollecting pairable values:")
    for i in range(n_items):
        item_values = [arr[i, j] for j in range(n_raters) if not missing_mask[i, j]]
        if len(item_values) >= 2:
            all_pairable_values.extend(item_values)
            print(f"  Item {i+1}: {item_values}")
            
            # Create coincidence pairs (including both directions for coincidence matrix)
            for a in range(len(item_values)):
                for b in range(len(item_values)):
                    if a != b:  # Different positions (Krippendorff counts all directed pairs)
                        coincidence_pairs.append((item_values[a], item_values[b]))
    
    n_pairable = len(all_pairable_values)
    print(f"Total pairable values: {n_pairable}")
    print(f"Total coincidence pairs: {len(coincidence_pairs)}")
    
    # Value frequencies
    value_counts = Counter(all_pairable_values)
    unique_values = sorted(value_counts.keys())
    print(f"Value frequencies: {dict(value_counts)}")
    
    # Distance function
    def delta_nominal(v1, v2):
        return 0.0 if v1 == v2 else 1.0
    
    # OBSERVED DISAGREEMENT using coincidence pairs
    print(f"\n=== OBSERVED DISAGREEMENT (Coincidence Method) ===")
    observed_sum = 0.0
    
    for v1, v2 in coincidence_pairs:
        observed_sum += delta_nominal(v1, v2)
    
    d_observed = observed_sum / len(coincidence_pairs) if coincidence_pairs else 0.0
    print(f"D_observed = {observed_sum} / {len(coincidence_pairs)} = {d_observed:.6f}")
    
    # EXPECTED DISAGREEMENT - Corrected version
    print(f"\n=== EXPECTED DISAGREEMENT (Corrected) ===")
    print("Using marginal probabilities from pairable values")
    
    expected_sum = 0.0
    
    # Krippendorff's method: use marginal probabilities
    for v1 in unique_values:
        for v2 in unique_values:
            if v1 != v2:  # Only different values contribute to disagreement
                # Probability of drawing v1 then v2 from the marginal distribution  
                p_v1 = value_counts[v1] / n_pairable
                p_v2 = value_counts[v2] / n_pairable
                
                # For coincidence matrix: probability of (v1, v2) pair
                prob_pair = p_v1 * p_v2
                
                contribution = prob_pair * delta_nominal(v1, v2)
                expected_sum += contribution
                
                print(f"  P({v1}, {v2}): {p_v1:.4f} × {p_v2:.4f} × {delta_nominal(v1, v2)} = {contribution:.6f}")
    
    d_expected = expected_sum
    print(f"D_expected = {d_expected:.6f}")
    
    # Calculate alpha
    print(f"\n=== ALPHA CALCULATION ===")
    if d_expected == 0:
        alpha = 1.0 if d_observed == 0 else float('-inf')
    else:
        alpha = 1.0 - (d_observed / d_expected)
        print(f"alpha = 1 - ({d_observed:.6f} / {d_expected:.6f})")
        print(f"alpha = 1 - {d_observed/d_expected:.6f}")
        print(f"alpha = {alpha:.6f}")
    
    return alpha

def alternative_expected_disagreement(data, level='nominal'):
    """
    Alternative calculation using different expected disagreement formula
    """
    print(f"\n=== ALTERNATIVE EXPECTED DISAGREEMENT CALCULATION ===")
    
    # Same setup as before
    arr = np.array(data, dtype=object)
    n_items, n_raters = arr.shape
    missing_mask = np.array([[pd.isna(val) or val is None for val in row] for row in arr])
    
    all_pairable_values = []
    observed_pairs = []
    
    for i in range(n_items):
        item_values = [arr[i, j] for j in range(n_raters) if not missing_mask[i, j]]
        if len(item_values) >= 2:
            all_pairable_values.extend(item_values)
            # Count actual pairs (not coincidence pairs)
            for a in range(len(item_values)):
                for b in range(a + 1, len(item_values)):
                    observed_pairs.append((item_values[a], item_values[b]))
    
    n_pairable = len(all_pairable_values)
    value_counts = Counter(all_pairable_values)
    
    def delta_nominal(v1, v2):
        return 0.0 if v1 == v2 else 1.0
    
    # Observed disagreement (unique pairs only)
    observed_sum = sum(delta_nominal(v1, v2) for v1, v2 in observed_pairs)
    d_observed = observed_sum / len(observed_pairs) if observed_pairs else 0.0
    
    # Expected disagreement - Method 2: sampling without replacement
    print("Method: Sampling without replacement from marginal distribution")
    expected_sum = 0.0
    
    unique_values = sorted(value_counts.keys())
    for v1 in unique_values:
        for v2 in unique_values:
            if v1 != v2:
                # Probability of sampling v1 first, then v2 (without replacement)
                p_v1_first = value_counts[v1] / n_pairable
                p_v2_second = value_counts[v2] / (n_pairable - 1)
                
                prob_pair = p_v1_first * p_v2_second
                contribution = prob_pair * delta_nominal(v1, v2)
                expected_sum += contribution
                
                print(f"  P({v1} then {v2}): ({value_counts[v1]}/{n_pairable}) × ({value_counts[v2]}/{n_pairable-1}) × 1 = {contribution:.6f}")
    
    d_expected_alt = expected_sum
    print(f"Alternative D_expected = {d_expected_alt:.6f}")
    
    alpha_alt = 1.0 - (d_observed / d_expected_alt) if d_expected_alt > 0 else 1.0
    print(f"Alternative alpha = 1 - ({d_observed:.6f} / {d_expected_alt:.6f}) = {alpha_alt:.6f}")
    
    return alpha_alt

# Test with sample data
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
    
    print("Testing corrected implementation:")
    print("Expected from k-alpha.org: ~0.33")
    print("Current implementation gives: ~0.72")
    print()
    
    alpha1 = corrected_krippendorff_alpha(sample_data)
    alpha2 = alternative_expected_disagreement(sample_data)
    
    print(f"\n*** RESULTS SUMMARY ***")
    print(f"Corrected Method 1: alpha = {alpha1:.6f}")
    print(f"Alternative Method 2: alpha = {alpha2:.6f}")
    print(f"Target value: ~0.33")