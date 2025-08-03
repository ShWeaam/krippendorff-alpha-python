"""Tests for krippendorff_alpha.core module"""

import pytest
import numpy as np
from krippendorff_alpha.core import krippendorff_alpha


class TestKrippendorffAlpha:
    """Test cases for Krippendorff's Alpha calculation"""
    
    def test_perfect_agreement(self):
        """Test with perfect agreement data"""
        data = [
            [1, 1, 1, 1],
            [2, 2, 2, 2],
            [3, 3, 3, 3]
        ]
        alpha = krippendorff_alpha(data, level='nominal')
        assert alpha == 1.0, f"Expected 1.0, got {alpha}"
    
    def test_no_agreement(self):
        """Test with completely random data"""
        data = [
            [1, 2, 3, 4],
            [4, 3, 2, 1],
            [2, 4, 1, 3]
        ]
        alpha = krippendorff_alpha(data, level='nominal')
        assert alpha <= 0.0, f"Expected <= 0.0, got {alpha}"
    
    def test_high_agreement(self):
        """Test with high agreement data"""
        data = [
            [1, 1, 2, 1],    # Item 1: mostly agree
            [2, 2, 2, 2],    # Item 2: perfect agreement  
            [3, 3, 1, 3],    # Item 3: one disagreement
            [1, 1, 1, 1]     # Item 4: perfect agreement
        ]
        alpha = krippendorff_alpha(data, level='nominal')
        assert 0.8 <= alpha <= 1.0, f"Expected high agreement (0.8-1.0), got {alpha}"
    
    def test_all_measurement_scales(self):
        """Test all measurement scales work"""
        data = [
            [1, 1, 2, 1],
            [2, 2, 2, 2],
            [3, 3, 3, 3]
        ]
        
        for scale in ['nominal', 'ordinal', 'interval', 'ratio']:
            alpha = krippendorff_alpha(data, level=scale)
            assert isinstance(alpha, float), f"Scale {scale} should return float"
            assert 0.0 <= alpha <= 1.0, f"Scale {scale}: alpha should be 0-1, got {alpha}"
    
    def test_missing_values(self):
        """Test handling of missing values"""
        data = [
            [1, None, 2, 1],
            [2, 2, None, 2],
            [3, 3, 3, None]
        ]
        alpha = krippendorff_alpha(data, level='nominal')
        assert isinstance(alpha, float), "Should handle missing values"
    
    def test_bootstrap_confidence_intervals(self):
        """Test bootstrap confidence intervals"""
        data = [
            [1, 1, 2, 1],
            [2, 2, 2, 2],
            [3, 3, 3, 3],
            [1, 1, 1, 1]
        ]
        
        result = krippendorff_alpha(data, level='nominal', bootstrap=100, ci=0.95, seed=42)
        alpha, ci_low, ci_high, boot_samples = result
        
        assert isinstance(alpha, float)
        assert isinstance(ci_low, float)
        assert isinstance(ci_high, float)
        assert len(boot_samples) == 100
        assert ci_low <= alpha <= ci_high
    
    def test_per_item_statistics(self):
        """Test per-item statistics"""
        data = [
            [1, 1, 2, 1],
            [2, 2, 2, 2],
            [3, 3, 3, 3]
        ]
        
        alpha, item_stats = krippendorff_alpha(data, level='nominal', return_items=True)
        
        assert isinstance(alpha, float)
        assert len(item_stats) == 3  # 3 items
        assert 'num_ratings' in item_stats.columns
        assert 'agreement_ratio' in item_stats.columns
    
    def test_custom_missing_value(self):
        """Test custom missing value specification"""
        data = [
            [1, -999, 2, 1],
            [2, 2, -999, 2],
            [3, 3, 3, -999]
        ]
        
        alpha = krippendorff_alpha(data, level='nominal', missing=-999)
        assert isinstance(alpha, float)
    
    def test_edge_cases(self):
        """Test edge cases"""
        # Single item
        data = [[1, 1, 1, 1]]
        alpha = krippendorff_alpha(data, level='nominal')
        assert alpha == 1.0
        
        # Two raters only
        data = [
            [1, 1],
            [2, 2],
            [3, 3]
        ]
        alpha = krippendorff_alpha(data, level='nominal')
        assert alpha == 1.0
    
    def test_invalid_inputs(self):
        """Test invalid input handling"""
        # Empty data
        with pytest.raises((ValueError, IndexError)):
            krippendorff_alpha([], level='nominal')
        
        # Invalid measurement level
        data = [[1, 1, 1, 1]]
        with pytest.raises(ValueError):
            krippendorff_alpha(data, level='invalid')
    
    def test_ordinal_scale_specific(self):
        """Test ordinal scale with ranked data"""
        data = [
            [1, 1, 2, 1],  # Ratings 1-2
            [3, 3, 3, 3],  # All rating 3
            [5, 4, 5, 5],  # Ratings 4-5
        ]
        
        alpha = krippendorff_alpha(data, level='ordinal')
        assert isinstance(alpha, float)
        assert 0.0 <= alpha <= 1.0
    
    def test_reproducible_bootstrap(self):
        """Test that bootstrap results are reproducible with same seed"""
        data = [
            [1, 1, 2, 1],
            [2, 2, 2, 2],
            [3, 3, 3, 3]
        ]
        
        result1 = krippendorff_alpha(data, level='nominal', bootstrap=50, seed=42)
        result2 = krippendorff_alpha(data, level='nominal', bootstrap=50, seed=42)
        
        assert result1[0] == result2[0]  # Same alpha
        assert result1[1] == result2[1]  # Same CI lower
        assert result1[2] == result2[2]  # Same CI upper