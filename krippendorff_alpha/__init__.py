"""
Krippendorff's Alpha for Inter-Rater Reliability

A comprehensive, theoretically correct implementation of Krippendorff's Alpha coefficient
following Klaus Krippendorff's "Content Analysis: An Introduction to Its Methodology" (4th Edition, 2019).

This package provides:
- All 4 measurement scales (nominal, ordinal, interval, ratio)
- Bootstrap confidence intervals with bias correction
- Comprehensive data validation
- Interactive configuration
- Per-item statistics and detailed analysis
- Flexible input formats (lists, arrays, DataFrames)

Example:
    >>> from krippendorff_alpha import krippendorff_alpha
    >>> data = [[1, 1, 2, 1], [2, 2, 2, 2], [3, 3, 1, 3]]
    >>> alpha = krippendorff_alpha(data, level='nominal')
    >>> print(f"Alpha: {alpha:.4f}")
    Alpha: 0.9763
"""

__version__ = "1.0.0"
__author__ = "Wild Boars Research Team"
__email__ = "research@wildboars.org"
__license__ = "MIT"

# Import main functions
from .core import krippendorff_alpha, interactive_krippendorff_alpha
from .validators import validate_data, validate_scale
from .utils import load_csv, save_results

# Import result classes
from .core import KAlphaResult

__all__ = [
    'krippendorff_alpha',
    'interactive_krippendorff_alpha', 
    'validate_data',
    'validate_scale',
    'load_csv',
    'save_results',
    'KAlphaResult'
]