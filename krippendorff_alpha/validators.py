"""
Data validation utilities for Krippendorff's Alpha calculation.
"""

import numpy as np
import pandas as pd
from typing import List, Union, Any

def validate_scale(level: str) -> str:
    """
    Validate measurement scale parameter.
    
    Args:
        level: Measurement scale ('nominal', 'ordinal', 'interval', 'ratio')
        
    Returns:
        Validated scale string
        
    Raises:
        ValueError: If scale is invalid
    """
    valid_scales = {'nominal', 'ordinal', 'interval', 'ratio'}
    if level not in valid_scales:
        raise ValueError(f"Invalid measurement scale '{level}'. Must be one of: {valid_scales}")
    return level

def validate_data(data: List[List[Union[int, str]]], level: str) -> None:
    """
    Validate data appropriateness for the specified measurement scale.
    
    Args:
        data: Input data matrix
        level: Measurement scale
        
    Raises:
        ValueError: If data is inappropriate for the measurement scale
    """
    # Get all non-missing values
    values_list = []
    for row in data:
        for val in row:
            if val != '' and val != 'NA' and not pd.isna(val):
                values_list.append(val)
    
    if not values_list:
        raise ValueError("No valid data values found")
    
    if level == 'ratio':
        # Ratio scale requires non-negative values
        try:
            numeric_values = [float(v) for v in values_list]
            if any(v < 0 for v in numeric_values):
                raise ValueError("Ratio scale requires non-negative values. Found negative values in data.")
        except (ValueError, TypeError) as e:
            if "could not convert" in str(e):
                raise ValueError("Ratio scale requires numeric data")
            raise
    
    elif level in ['interval', 'ordinal']:
        # Interval and ordinal scales require numeric data
        try:
            [float(v) for v in values_list]
        except (ValueError, TypeError):
            if level == 'ordinal':
                # Ordinal can be non-numeric if properly ordered
                pass
            else:
                raise ValueError(f"{level.capitalize()} scale requires numeric data")

def validate_confidence_interval(ci: float) -> float:
    """
    Validate confidence interval parameter.
    
    Args:
        ci: Confidence level (0 < ci < 1)
        
    Returns:
        Validated confidence interval
        
    Raises:
        ValueError: If confidence interval is invalid
    """
    if not (0 < ci < 1):
        raise ValueError(f"Confidence interval must be between 0 and 1, got {ci}")
    return ci

def validate_bootstrap_params(bootstrap: int, seed: Union[int, None]) -> tuple:
    """
    Validate bootstrap parameters.
    
    Args:
        bootstrap: Number of bootstrap iterations
        seed: Random seed
        
    Returns:
        Tuple of validated parameters
        
    Raises:
        ValueError: If parameters are invalid
    """
    if bootstrap <= 0:
        raise ValueError("Bootstrap iterations must be positive")
    
    if seed is not None and not isinstance(seed, int):
        raise ValueError("Random seed must be an integer or None")
    
    return bootstrap, seed