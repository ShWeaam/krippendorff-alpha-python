#!/usr/bin/env python3
"""
Test the corrected ordinal implementation with sample data
"""

from krippendorff_alpha import krippendorff_alpha
from krippendorff_alpha.utils import create_sample_data

def test_ordinal_fix():
    """Test corrected ordinal implementation"""
    
    print("TESTING CORRECTED ORDINAL IMPLEMENTATION")
    print("=" * 60)
    
    # Test with high agreement sample data
    print("High Agreement Sample Data:")
    high_data = create_sample_data(8, 4, agreement_level='high')
    
    print("Data preview:")
    for i, row in enumerate(high_data):
        print(f"  Item {i+1}: {row}")
    print()
    
    # Calculate alpha for all measurement levels
    results = {}
    for level in ['nominal', 'ordinal', 'interval', 'ratio']:
        try:
            alpha = krippendorff_alpha(high_data, level=level)
            results[level] = alpha
            print(f"{level.capitalize():>8}: α = {alpha:.6f}")
        except Exception as e:
            print(f"{level.capitalize():>8}: Error - {e}")
    
    print()
    print("KEY CHANGES:")
    print("- Previous ordinal: α ≈ 0.505 (incorrect formula)")
    print("- Corrected ordinal: α ≈ {:.6f} (Krippendorff 2019 formula)".format(results.get('ordinal', 0)))
    print()
    print("VALIDATION:")
    print("- Ordinal should now match k-alpha.org exactly")
    print("- Test this data at https://www.k-alpha.org/ to confirm")
    print()
    
    # Test with a simple case
    print("Simple 3x2 Test Case:")
    simple_data = [
        [1, 1],
        [2, 2], 
        [3, 3]
    ]
    
    print("Perfect agreement data:")
    for i, row in enumerate(simple_data):
        print(f"  Item {i+1}: {row}")
    print()
    
    for level in ['nominal', 'ordinal', 'interval', 'ratio']:
        try:
            alpha = krippendorff_alpha(simple_data, level=level)
            print(f"{level.capitalize():>8}: α = {alpha:.6f}")
        except Exception as e:
            print(f"{level.capitalize():>8}: Error - {e}")

if __name__ == "__main__":
    test_ordinal_fix()