# CRITICAL CALCULATION ERRORS FOUND

## Issues Identified:

### 1. **DOUBLE-COUNTING ERROR** (Lines 319-323 in core.py)
```python
# WRONG: Counts each pair twice
for a in range(m):
    for b in range(m):
        if a != b:
            observed_sum += delta_func(vals[a], vals[b])
            total_pairs += 1
```

**Problem**: This counts delta(A,B) AND delta(B,A), doubling the disagreement.

### 2. **EXPECTED DISAGREEMENT ERROR** (Lines 342-344, 347-349)
```python
# WRONG: Also double-counts pairs
for v in sorted_vals:
    for v_prime in sorted_vals:
        if v != v_prime:
            expected_sum += (freq[v] * freq[v_prime] / (n_total - 1)) * delta_func(v, v_prime)
```

**Problem**: Same double-counting issue + wrong normalization.

### 3. **PERFORMANCE ISSUE**
- O(n²) loops for large datasets
- 150 items × 236 raters = 35,400 values
- Pairwise comparisons = massive computation

## Root Cause:
Both observed and expected disagreement are doubled, but the ratio D_o/D_e might still be wrong due to different normalization factors, leading to artificially high alpha values.