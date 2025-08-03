#!/usr/bin/env python3
"""
Basic usage examples for Krippendorff's Alpha calculator
"""

from krippendorff_alpha import krippendorff_alpha, interactive_krippendorff_alpha
from krippendorff_alpha.utils import create_sample_data, get_reliability_interpretation

# Example 1: Basic calculation
print("=== Example 1: Basic Krippendorff's Alpha ===")
data = [
    [1, 1, 2, 1],    # Item 1: mostly agree
    [2, 2, 2, 2],    # Item 2: perfect agreement  
    [3, 3, 1, 3],    # Item 3: one disagreement
    [1, 1, 1, 1]     # Item 4: perfect agreement
]

alpha = krippendorff_alpha(data, level='nominal')
interpretation = get_reliability_interpretation(alpha)

print(f"Data: {data}")
print(f"Alpha: {alpha:.4f}")
print(f"Interpretation: {interpretation['level']} - {interpretation['description']}")
print()

# Example 2: All measurement scales
print("=== Example 2: Different Measurement Scales ===")
for scale in ['nominal', 'ordinal', 'interval', 'ratio']:
    alpha = krippendorff_alpha(data, level=scale)
    print(f"{scale.capitalize():8}: α = {alpha:.4f}")
print()

# Example 3: Bootstrap confidence intervals
print("=== Example 3: Bootstrap Confidence Intervals ===")
result = krippendorff_alpha(
    data, 
    level='nominal',           # measurement scale
    bootstrap=1000,            # bootstrap iterations
    ci=0.95,                  # confidence level
    seed=42                   # for reproducibility
)

alpha, ci_low, ci_high, boot_samples = result
print(f"Alpha: {alpha:.4f}")
print(f"95% CI: [{ci_low:.4f}, {ci_high:.4f}]")
print(f"Bootstrap samples: {len(boot_samples)}")
print()

# Example 4: Per-item statistics
print("=== Example 4: Per-Item Analysis ===")
alpha, item_stats = krippendorff_alpha(
    data, 
    level='nominal',
    return_items=True
)

print(f"Overall Alpha: {alpha:.4f}")
print("\nPer-item statistics:")
print(item_stats)
print()

# Example 5: Missing values
print("=== Example 5: Handling Missing Values ===")
data_with_missing = [
    [1, None, 2, 1],    # Standard missing (None)
    [2, 2, 2, 2],
    [3, 3, -999, 3],    # Custom missing (-999)
    [1, 1, 1, 1]
]

# Using standard missing values
alpha1 = krippendorff_alpha(data_with_missing, level='nominal')
print(f"With standard missing: α = {alpha1:.4f}")

# Using custom missing value
alpha2 = krippendorff_alpha(data_with_missing, level='nominal', missing=-999)
print(f"With custom missing (-999): α = {alpha2:.4f}")
print()

# Example 6: Sample data generation
print("=== Example 6: Sample Data Generation ===")
sample_data = create_sample_data(items=6, raters=3, agreement_level='medium')
alpha = krippendorff_alpha(sample_data, level='nominal')
print(f"Sample data (6 items × 3 raters):")
for i, item in enumerate(sample_data):
    print(f"  Item {i+1}: {item}")
print(f"Alpha: {alpha:.4f}")
print()

# Example 7: Different confidence levels
print("=== Example 7: Different Confidence Levels ===")
for ci_level in [0.80, 0.90, 0.95, 0.99]:
    result = krippendorff_alpha(
        data, 
        level='nominal', 
        bootstrap=200,
        ci=ci_level,
        seed=42
    )
    alpha, ci_low, ci_high, _ = result
    print(f"{ci_level*100:4.0f}% CI: [{ci_low:.3f}, {ci_high:.3f}]")
print()

# Example 8: Large dataset simulation
print("=== Example 8: Large Dataset Example ===")
large_data = create_sample_data(items=50, raters=8, agreement_level='high')
alpha = krippendorff_alpha(large_data, level='ordinal')
interpretation = get_reliability_interpretation(alpha)

print(f"Large dataset: 50 items × 8 raters")
print(f"Alpha: {alpha:.4f}")
print(f"Assessment: {interpretation['level']}")
print(f"Recommendation: {interpretation['recommendation']}")
print()

# Example 9: Interactive configuration (uncomment to use)
print("=== Example 9: Interactive Configuration ===")
print("Uncomment the following lines to try interactive setup:")
print("# config = interactive_krippendorff_alpha()")
print("# result = krippendorff_alpha(your_data, **config)")
print()

print("=== All Examples Complete! ===")
print("For more advanced usage, see the documentation at:")
print("https://github.com/ShWeaam/krippendorff_alpha_calculator")