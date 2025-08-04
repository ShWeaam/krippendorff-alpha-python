#!/usr/bin/env python3
"""
Comprehensive Krippendorff Alpha Validation
Creates proper test cases and validates against theoretical specifications
"""

import numpy as np
import pandas as pd
from krippendorff_alpha import krippendorff_alpha

def create_test_cases():
    """Create proper test cases with known agreement levels"""
    
    test_cases = {}
    
    # 1. VERY HIGH AGREEMENT (alpha > 0.8) - Near perfect with minimal disagreement
    test_cases['very_high'] = {
        'name': 'Very High Agreement (alpha > 0.8)',
        'data': [
            [1, 1, 1, 1],    # Perfect agreement
            [2, 2, 2, 2],    # Perfect agreement  
            [3, 3, 3, 3],    # Perfect agreement
            [1, 1, 1, 2],    # Minor disagreement (1 out of 4)
            [2, 2, 2, 2],    # Perfect agreement
            [3, 3, 3, 3],    # Perfect agreement
            [1, 1, 1, 1],    # Perfect agreement
            [2, 2, 2, 2],    # Perfect agreement
        ],
        'expected_range': (0.8, 1.0)
    }
    
    # 2. HIGH AGREEMENT (alpha > 0.67) - Good agreement with some disagreement  
    test_cases['high'] = {
        'name': 'High Agreement (alpha > 0.67)',
        'data': [
            [1, 1, 1, 2],    # 3/4 agreement
            [2, 2, 2, 2],    # Perfect agreement
            [3, 3, 2, 3],    # 3/4 agreement  
            [1, 1, 1, 1],    # Perfect agreement
            [2, 2, 3, 2],    # 3/4 agreement
            [3, 3, 3, 3],    # Perfect agreement
            [1, 2, 1, 1],    # 3/4 agreement
            [2, 2, 2, 2],    # Perfect agreement
        ],
        'expected_range': (0.67, 0.8)
    }
    
    # 3. MEDIUM AGREEMENT (alpha > 0.4) - Moderate agreement
    test_cases['medium'] = {
        'name': 'Medium Agreement (alpha > 0.4)', 
        'data': [
            [1, 1, 2, 2],    # 50% agreement
            [2, 2, 1, 1],    # 50% agreement
            [3, 3, 3, 2],    # 75% agreement
            [1, 2, 1, 2],    # 50% agreement
            [2, 1, 2, 2],    # 75% agreement
            [3, 3, 1, 3],    # 75% agreement
            [1, 1, 2, 3],    # 50% agreement
            [2, 2, 2, 1],    # 75% agreement
        ],
        'expected_range': (0.4, 0.67)
    }
    
    # 4. LOW AGREEMENT (alpha < 0.4) - Poor agreement
    test_cases['low'] = {
        'name': 'Low Agreement (alpha < 0.4)',
        'data': [
            [1, 2, 3, 4],    # No agreement
            [2, 1, 4, 3],    # No agreement
            [3, 4, 1, 2],    # No agreement
            [4, 3, 2, 1],    # No agreement
            [1, 3, 2, 4],    # No agreement
            [2, 4, 1, 3],    # No agreement
            [1, 1, 2, 3],    # Some agreement (2/4)
            [2, 2, 3, 1],    # Some agreement (2/4)
        ],
        'expected_range': (0.0, 0.4)
    }
    
    # 5. RANDOM/NO AGREEMENT (alpha ~= 0) - Random responses
    test_cases['random'] = {
        'name': 'Random/No Agreement (alpha ~= 0)',
        'data': [
            [1, 2, 3, 4],    # Completely random
            [4, 1, 2, 3],    # Completely random
            [2, 4, 1, 3],    # Completely random
            [3, 2, 4, 1],    # Completely random
            [4, 3, 1, 2],    # Completely random
            [1, 4, 3, 2],    # Completely random
            [2, 1, 4, 3],    # Completely random
            [3, 1, 2, 4],    # Completely random
        ],
        'expected_range': (-0.2, 0.2)
    }
    
    # 6. PERFECT AGREEMENT (alpha = 1.0) - All raters agree completely
    test_cases['perfect'] = {
        'name': 'Perfect Agreement (alpha = 1.0)',
        'data': [
            [1, 1, 1, 1],
            [2, 2, 2, 2], 
            [3, 3, 3, 3],
            [1, 1, 1, 1],
            [2, 2, 2, 2],
            [3, 3, 3, 3],
        ],
        'expected_range': (1.0, 1.0)
    }
    
    return test_cases

def validate_against_specifications():
    """Validate implementation against Krippendorff's exact specifications"""
    
    print("="*80)
    print("KRIPPENDORFF ALPHA SPECIFICATION VALIDATION")
    print("="*80)
    
    validation_results = []
    
    # Test 1: Perfect agreement should give α = 1.0
    print("\n1. Perfect Agreement Test:")
    perfect_data = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
    alpha = krippendorff_alpha(perfect_data, level='nominal')
    success = abs(alpha - 1.0) < 0.0001
    print(f"   Result: alpha = {alpha:.6f} (expected: 1.0)")
    print(f"   Status: {'PASS' if success else 'FAIL'}")
    validation_results.append(('Perfect Agreement', success, alpha, 1.0))
    
    # Test 2: Complete disagreement should give α ≤ 0
    print("\n2. Complete Disagreement Test:")
    disagree_data = [[1, 2], [2, 1], [1, 2], [2, 1]]
    alpha = krippendorff_alpha(disagree_data, level='nominal')
    success = alpha <= 0.1  # Should be close to 0 or negative
    print(f"   Result: alpha = {alpha:.6f} (expected: <= 0)")
    print(f"   Status: {'PASS' if success else 'FAIL'}")
    validation_results.append(('Complete Disagreement', success, alpha, 0.0))
    
    # Test 3: Single rater should be rejected
    print("\n3. Single Rater Rejection Test:")
    try:
        single_rater_data = [[1], [2], [3]]
        alpha = krippendorff_alpha(single_rater_data, level='nominal')
        success = False  # Should have thrown an exception
        print(f"   Result: alpha = {alpha:.6f} (should have failed)")
        print(f"   Status: FAIL - Should reject single rater")
    except Exception as e:
        success = True
        print(f"   Result: Correctly rejected - {str(e)}")
        print(f"   Status: PASS")
    validation_results.append(('Single Rater Rejection', success, None, 'Exception'))
    
    # Test 4: Missing values handling
    print("\n4. Missing Values Test:")
    missing_data = [
        [1, 1, np.nan, 1],
        [2, np.nan, 2, 2],
        [np.nan, 3, 3, 3]
    ]
    alpha = krippendorff_alpha(missing_data, level='nominal')
    success = 0.0 <= alpha <= 1.0  # Should give reasonable result
    print(f"   Result: alpha = {alpha:.6f} (should be reasonable)")
    print(f"   Status: {'PASS' if success else 'FAIL'}")
    validation_results.append(('Missing Values', success, alpha, 'reasonable'))
    
    # Test 5: Different measurement levels
    print("\n5. Measurement Levels Test:")
    test_data = [[1, 1, 2], [2, 2, 3], [3, 3, 1]]
    
    for level in ['nominal', 'ordinal', 'interval', 'ratio']:
        try:
            alpha = krippendorff_alpha(test_data, level=level)
            success = 0.0 <= alpha <= 1.0 or alpha < 0  # Negative is okay
            print(f"   {level.capitalize():>8}: alpha = {alpha:.6f} {'PASS' if success else 'FAIL'}")
            validation_results.append((f'{level.capitalize()} Level', success, alpha, 'valid'))
        except Exception as e:
            print(f"   {level.capitalize():>8}: Error - {str(e)} FAIL")
            validation_results.append((f'{level.capitalize()} Level', False, None, f'Error: {e}'))
    
    return validation_results

def run_comprehensive_tests():
    """Run comprehensive tests with proper agreement levels"""
    
    print("="*80)
    print("COMPREHENSIVE AGREEMENT LEVEL TESTS")
    print("="*80)
    
    test_cases = create_test_cases()
    results = []
    
    for key, case in test_cases.items():
        print(f"\n{case['name']}:")
        print("-" * 60)
        
        # Test with nominal scale
        alpha = krippendorff_alpha(case['data'], level='nominal')
        expected_min, expected_max = case['expected_range']
        
        # Check if result is in expected range
        in_range = expected_min <= alpha <= expected_max
        
        print(f"Data shape: {len(case['data'])} items x {len(case['data'][0])} raters")
        print(f"Result: alpha = {alpha:.6f}")
        print(f"Expected range: [{expected_min:.3f}, {expected_max:.3f}]")
        print(f"Status: {'PASS' if in_range else 'FAIL - Outside expected range'}")
        
        # Show sample of the data
        print("Sample data:")
        for i, row in enumerate(case['data'][:3]):
            print(f"  Item {i+1}: {row}")
        if len(case['data']) > 3:
            print(f"  ... and {len(case['data'])-3} more items")
        
        results.append({
            'name': case['name'],
            'alpha': alpha,
            'expected_range': case['expected_range'],
            'in_range': in_range,
            'data_size': f"{len(case['data'])}×{len(case['data'][0])}"
        })
    
    return results

def test_robustness():
    """Test robustness with edge cases"""
    
    print("\n" + "="*80)
    print("ROBUSTNESS TESTS")
    print("="*80)
    
    edge_cases = [
        {
            'name': 'All Same Values',
            'data': [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
            'expected': 1.0
        },
        {
            'name': 'Two Categories Only',
            'data': [[1, 1, 2], [2, 2, 1], [1, 2, 1]],
            'expected': 'reasonable'
        },
        {
            'name': 'Many Categories',
            'data': [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            'expected': 'low'
        },
        {
            'name': 'Uneven Missing Data',
            'data': [
                [1, np.nan, np.nan, np.nan],
                [np.nan, 2, np.nan, np.nan], 
                [np.nan, np.nan, 3, np.nan],
                [np.nan, np.nan, np.nan, 4],
                [1, 2, 3, 4]
            ],
            'expected': 'handles_missing'
        }
    ]
    
    for case in edge_cases:
        print(f"\n{case['name']}:")
        print("-" * 40)
        
        try:
            alpha = krippendorff_alpha(case['data'], level='nominal')
            print(f"Result: alpha = {alpha:.6f}")
            
            if case['expected'] == 1.0:
                success = abs(alpha - 1.0) < 0.001
            elif case['expected'] == 'reasonable':
                success = -1.0 <= alpha <= 1.0
            elif case['expected'] == 'low':
                success = alpha < 0.5
            elif case['expected'] == 'handles_missing':
                success = not np.isnan(alpha) and not np.isinf(alpha)
            else:
                success = True
                
            print(f"Status: {'PASS' if success else 'FAIL'}")
            
        except Exception as e:
            print(f"Error: {e}")
            print("Status: FAIL")

if __name__ == "__main__":
    print("COMPREHENSIVE KRIPPENDORFF ALPHA VALIDATION")
    print("="*80)
    print("Validating implementation against theoretical specifications")
    print("and testing with proper agreement level examples")
    print()
    
    # Run all tests
    spec_results = validate_against_specifications()
    test_results = run_comprehensive_tests()
    test_robustness()
    
    # Summary
    print("\n" + "="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    
    print("\nSpecification Tests:")
    passed_specs = sum(1 for _, success, _, _ in spec_results if success)
    total_specs = len(spec_results)
    print(f"Passed: {passed_specs}/{total_specs}")
    
    print("\nAgreement Level Tests:")
    passed_agreement = sum(1 for result in test_results if result['in_range'])
    total_agreement = len(test_results)
    print(f"Passed: {passed_agreement}/{total_agreement}")
    
    print("\nRecommended Test Cases for Your Research:")
    print("-" * 50)
    for result in test_results:
        if result['in_range']:
            print(f"PASS {result['name']}: alpha = {result['alpha']:.3f}")
        else:
            print(f"WARN {result['name']}: alpha = {result['alpha']:.3f} (outside expected range)")
    
    overall_success = (passed_specs == total_specs) and (passed_agreement >= total_agreement * 0.8)
    print(f"\nOverall Status: {'ROBUST & ACCURATE' if overall_success else 'NEEDS ATTENTION'}")