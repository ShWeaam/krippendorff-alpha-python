#!/usr/bin/env python3
"""
Properly Calibrated Krippendorff Alpha Examples
Creates test data with accurate agreement levels for research use
"""

import numpy as np
from krippendorff_alpha import krippendorff_alpha

def create_calibrated_examples():
    """Create properly calibrated examples with verified agreement levels"""
    
    examples = {}
    
    # VERY HIGH AGREEMENT (alpha > 0.8) - Mostly perfect with minimal disagreement
    examples['very_high'] = {
        'name': 'Very High Agreement',
        'data': [
            [1, 1, 1, 1],    # Perfect
            [2, 2, 2, 2],    # Perfect  
            [3, 3, 3, 3],    # Perfect
            [1, 1, 1, 1],    # Perfect
            [2, 2, 2, 2],    # Perfect
            [3, 3, 3, 3],    # Perfect
            [1, 1, 1, 2],    # Minor disagreement (25%)
            [2, 2, 2, 1],    # Minor disagreement (25%)
            [3, 3, 3, 2],    # Minor disagreement (25%)
            [1, 1, 1, 1],    # Perfect
        ],
        'target_range': (0.8, 1.0),
        'description': 'Mostly perfect agreement with minimal disagreement'
    }
    
    # HIGH AGREEMENT (alpha 0.67-0.8) - Good agreement with some disagreement
    examples['high'] = {
        'name': 'High Agreement', 
        'data': [
            [1, 1, 1, 1],    # Perfect
            [2, 2, 2, 2],    # Perfect
            [1, 1, 1, 2],    # 75% agreement
            [2, 2, 2, 1],    # 75% agreement  
            [3, 3, 3, 3],    # Perfect
            [1, 1, 2, 1],    # 75% agreement
            [2, 2, 1, 2],    # 75% agreement
            [3, 3, 3, 3],    # Perfect
            [1, 1, 1, 1],    # Perfect
            [2, 2, 2, 2],    # Perfect
        ],
        'target_range': (0.67, 0.8),
        'description': 'Good agreement with some systematic disagreement'
    }
    
    # MEDIUM AGREEMENT (alpha 0.4-0.67) - Moderate agreement 
    examples['medium'] = {
        'name': 'Medium Agreement',
        'data': [
            [1, 1, 1, 2],    # 75% agreement
            [2, 2, 1, 2],    # 75% agreement
            [1, 1, 2, 1],    # 75% agreement
            [2, 2, 2, 1],    # 75% agreement
            [1, 2, 1, 1],    # 75% agreement
            [2, 1, 2, 2],    # 75% agreement
            [1, 1, 2, 2],    # 50% agreement
            [2, 2, 1, 1],    # 50% agreement
            [1, 2, 1, 2],    # 50% agreement
            [2, 1, 2, 1],    # 50% agreement
        ],
        'target_range': (0.4, 0.67),
        'description': 'Moderate agreement with balanced disagreement'
    }
    
    # LOW AGREEMENT (alpha 0.0-0.4) - Poor but not random
    examples['low'] = {
        'name': 'Low Agreement',
        'data': [
            [1, 2, 1, 2],    # 50% agreement
            [2, 1, 2, 1],    # 50% agreement
            [1, 2, 3, 1],    # 50% agreement (2 agree)
            [2, 1, 3, 2],    # 50% agreement (2 agree)
            [1, 3, 2, 1],    # 50% agreement (2 agree) 
            [2, 3, 1, 2],    # 50% agreement (2 agree)
            [1, 2, 3, 4],    # No agreement
            [2, 1, 4, 3],    # No agreement
            [3, 4, 1, 2],    # No agreement
            [4, 3, 2, 1],    # No agreement
        ],
        'target_range': (0.0, 0.4),
        'description': 'Poor agreement with mixed patterns'
    }
    
    # MINIMAL AGREEMENT (alpha around 0) - Near random
    examples['minimal'] = {
        'name': 'Minimal Agreement',
        'data': [
            [1, 2, 3, 4],    # Completely random
            [4, 1, 2, 3],    # Completely random
            [2, 4, 1, 3],    # Completely random
            [3, 2, 4, 1],    # Completely random
            [1, 3, 4, 2],    # Completely random
            [4, 2, 3, 1],    # Completely random
            [2, 1, 4, 3],    # Completely random
            [3, 4, 2, 1],    # Completely random
        ],
        'target_range': (-0.2, 0.2),
        'description': 'Random or near-random responses'
    }
    
    # SYSTEMATIC DISAGREEMENT (alpha < 0) - Worse than random
    examples['systematic_disagreement'] = {
        'name': 'Systematic Disagreement',
        'data': [
            [1, 2, 3, 4],    # Systematic pattern 1
            [2, 3, 4, 1],    # Systematic pattern 2
            [3, 4, 1, 2],    # Systematic pattern 3
            [4, 1, 2, 3],    # Systematic pattern 4
            [1, 2, 3, 4],    # Repeat pattern
            [2, 3, 4, 1],    # Repeat pattern
            [3, 4, 1, 2],    # Repeat pattern
            [4, 1, 2, 3],    # Repeat pattern
        ],
        'target_range': (-0.5, 0.0),
        'description': 'Systematic disagreement worse than random'
    }
    
    return examples

def test_all_examples():
    """Test all calibrated examples and report results"""
    
    print("CALIBRATED KRIPPENDORFF ALPHA EXAMPLES")
    print("="*80)
    print("These examples provide properly calibrated agreement levels for research")
    print()
    
    examples = create_calibrated_examples()
    results = []
    
    for key, example in examples.items():
        print(f"{example['name']}:")
        print("-" * 60)
        
        # Calculate alpha
        alpha = krippendorff_alpha(example['data'], level='nominal')
        target_min, target_max = example['target_range']
        
        # Check if in target range
        in_range = target_min <= alpha <= target_max
        
        print(f"Data: {len(example['data'])} items x {len(example['data'][0])} raters")
        print(f"Result: alpha = {alpha:.6f}")
        print(f"Target range: [{target_min:.3f}, {target_max:.3f}]")
        print(f"Status: {'EXCELLENT' if in_range else 'NEEDS ADJUSTMENT'}")
        print(f"Description: {example['description']}")
        
        # Show first few items as examples
        print("Sample data:")
        for i, row in enumerate(example['data'][:4]):
            print(f"  Item {i+1}: {row}")
        if len(example['data']) > 4:
            print(f"  ... and {len(example['data'])-4} more items")
        
        print()
        
        results.append({
            'name': example['name'],
            'alpha': alpha,
            'target_range': example['target_range'],
            'in_range': in_range,
            'data': example['data']
        })
    
    # Summary
    print("="*80)
    print("CALIBRATION SUMMARY")
    print("="*80)
    
    successful = [r for r in results if r['in_range']]
    needs_work = [r for r in results if not r['in_range']]
    
    print(f"Successfully calibrated: {len(successful)}/{len(results)}")
    print()
    
    if successful:
        print("READY FOR RESEARCH USE:")
        for r in successful:
            print(f"  {r['name']}: alpha = {r['alpha']:.3f}")
        print()
    
    if needs_work:
        print("NEED ADJUSTMENT:")
        for r in needs_work:
            target_min, target_max = r['target_range']
            print(f"  {r['name']}: alpha = {r['alpha']:.3f} (target: [{target_min:.3f}, {target_max:.3f}])")
        print()
    
    return results

def recommend_for_research():
    """Recommend the best examples for research use"""
    
    print("RESEARCH RECOMMENDATIONS")
    print("="*80)
    
    results = test_all_examples()
    successful = [r for r in results if r['in_range']]
    
    if successful:
        print("Use these examples for your research:")
        print()
        
        for r in successful:
            alpha_category = ""
            if r['alpha'] >= 0.8:
                alpha_category = "EXCELLENT reliability"
            elif r['alpha'] >= 0.67:
                alpha_category = "GOOD reliability" 
            elif r['alpha'] >= 0.4:
                alpha_category = "MODERATE reliability"
            elif r['alpha'] >= 0.0:
                alpha_category = "POOR reliability"
            else:
                alpha_category = "SYSTEMATIC DISAGREEMENT"
            
            print(f"{r['name']}: alpha = {r['alpha']:.3f} ({alpha_category})")
        
        print()
        print("These data sets demonstrate the full range of inter-rater reliability")
        print("and can be used to validate your Krippendorff alpha calculations.")
    
    else:
        print("No examples are properly calibrated yet. Need to adjust the test data.")

if __name__ == "__main__":
    recommend_for_research()