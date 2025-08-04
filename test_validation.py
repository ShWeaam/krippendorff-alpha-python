#!/usr/bin/env python3
"""
Quick validation test for Krippendorff Alpha calculations
"""

def test_perfect_agreement():
    """Test case that should give α = 1.0"""
    data = [
        [1, 1, 1, 1],
        [2, 2, 2, 2], 
        [3, 3, 3, 3],
        [1, 1, 1, 1]
    ]
    return data

def test_no_agreement():
    """Test case that should give α ≈ 0.0"""
    data = [
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [2, 4, 1, 3],
        [3, 1, 4, 2]
    ]
    return data

def test_krippendorff_example():
    """Example from Krippendorff's book (nominal scale)"""
    # This is a known example that should give α ≈ 0.691
    data = [
        [1, None, 3, 1],
        [2, 2, 3, 2],
        [3, 3, 3, 3],
        [3, 3, 3, 3],
        [2, 2, 3, 2],
        [1, 2, 3, 3],
        [4, 4, 4, 4],
        [1, 1, 2, 1],
        [2, 2, 2, 2],
        [None, 5, 5, 5]
    ]
    return data

def manual_calculation_check():
    """Manual calculation for a simple 2x2 case"""
    # Simple case: 2 items, 2 raters, values [1,2]
    data = [
        [1, 1],  # Perfect agreement
        [1, 2]   # Complete disagreement  
    ]
    
    print("Manual Check - Simple 2x2 case:")
    print("Data:", data)
    print("Expected: α ≈ 0.0 (half agree, half disagree)")
    
    # Manual calculation:
    # Observed: δ(1,1) + δ(1,2) = 0 + 1 = 1, so D_o = 1/2 = 0.5
    # Expected: P(1)*P(1)*δ(1,1) + P(1)*P(2)*δ(1,2) + P(2)*P(1)*δ(2,1) + P(2)*P(2)*δ(2,2)
    #          = (3/4)*(2/3)*0 + (3/4)*(1/3)*1 + (1/4)*(2/3)*1 + (1/4)*(1/3)*0
    #          = 0 + 1/4 + 1/6 + 0 = 3/12 + 2/12 = 5/12 ≈ 0.417
    # Alpha = 1 - (0.5 / 0.417) = 1 - 1.2 = -0.2
    
    return data

if __name__ == "__main__":
    print("=== Krippendorff Alpha Validation Tests ===")
    
    try:
        from krippendorff_alpha import krippendorff_alpha
        from krippendorff_alpha.utils import create_sample_data
        
        # Test 1: Perfect agreement
        print("\n1. Perfect Agreement Test:")
        data1 = test_perfect_agreement()
        alpha1 = krippendorff_alpha(data1, level='nominal')
        print(f"   Data: {data1}")
        print(f"   Alpha: {alpha1:.4f} (should be 1.0000)")
        
        # Test 2: No agreement
        print("\n2. No Agreement Test:")
        data2 = test_no_agreement() 
        alpha2 = krippendorff_alpha(data2, level='nominal')
        print(f"   Data: {data2}")
        print(f"   Alpha: {alpha2:.4f} (should be ≈ 0.0000)")
        
        # Test 3: Manual check
        print("\n3. Manual Calculation Check:")
        data3 = manual_calculation_check()
        alpha3 = krippendorff_alpha(data3, level='nominal')
        print(f"   Alpha: {alpha3:.4f} (manual calculation predicts ≈ -0.2)")
        
        # Test 4: Sample data
        print("\n4. Sample Data Tests:")
        for level in ['high', 'medium', 'low']:
            sample_data = create_sample_data(n_items=8, n_raters=4, agreement_level=level)
            alpha = krippendorff_alpha(sample_data, level='nominal')
            print(f"   {level.capitalize()} agreement: α = {alpha:.4f}")
            
        # Test 5: Krippendorff example
        print("\n5. Krippendorff Book Example:")
        data5 = test_krippendorff_example()
        alpha5 = krippendorff_alpha(data5, level='nominal')
        print(f"   Alpha: {alpha5:.4f} (should be ≈ 0.691)")
        
    except ImportError as e:
        print(f"Error importing: {e}")
        print("Run this from the package directory or install the package")
    except Exception as e:
        print(f"Calculation error: {e}")
        import traceback
        traceback.print_exc()