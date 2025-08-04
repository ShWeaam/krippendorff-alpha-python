"""
Utility functions for Krippendorff's Alpha package.
"""

import pandas as pd
import numpy as np
import json
from typing import List, Union, Dict, Any, Optional
from pathlib import Path

def load_csv(file_path: str, separator: str = 'auto') -> List[List[Union[int, str]]]:
    """
    Load data from CSV file with automatic separator detection.
    
    Args:
        file_path: Path to CSV file
        separator: Column separator ('auto', ',', ';', '\t')
        
    Returns:
        Data matrix as list of lists
        
    Example:
        >>> data = load_csv('ratings.csv')
        >>> alpha = krippendorff_alpha(data, level='nominal')
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Auto-detect separator
    if separator == 'auto':
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            if ';' in first_line:
                separator = ';'
            elif '\t' in first_line:
                separator = '\t'
            else:
                separator = ','
    
    df = pd.read_csv(file_path, sep=separator, header=None)
    data = []
    
    for _, row in df.iterrows():
        parsed_row = []
        for val in row:
            if pd.isna(val) or val == 'NA' or val == '':
                parsed_row.append('NA')
            else:
                try:
                    parsed_row.append(int(float(val)))
                except (ValueError, TypeError):
                    parsed_row.append('NA')
        data.append(parsed_row)
    
    return data

def save_results(results: Dict[str, Any], file_path: str, format: str = 'json') -> None:
    """
    Save Krippendorff Alpha results to file.
    
    Args:
        results: Results dictionary
        file_path: Output file path
        format: Output format ('json', 'csv', 'txt')
        
    Example:
        >>> alpha, ci_low, ci_high, _ = krippendorff_alpha(data, level='nominal', bootstrap=1000)
        >>> results = {'alpha': alpha, 'ci_low': ci_low, 'ci_high': ci_high}
        >>> save_results(results, 'alpha_results.json')
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    if format.lower() == 'json':
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
    
    elif format.lower() == 'csv':
        df = pd.DataFrame([results])
        df.to_csv(file_path, index=False)
    
    elif format.lower() == 'txt':
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Krippendorff's Alpha Results\n")
            f.write("=" * 30 + "\n")
            for key, value in results.items():
                f.write(f"{key}: {value}\n")
    
    else:
        raise ValueError(f"Unsupported format: {format}")

def format_results(alpha: float, ci_low: Optional[float] = None, ci_high: Optional[float] = None, 
                  level: Optional[str] = None, items: Optional[int] = None, raters: Optional[int] = None) -> str:
    """
    Format Krippendorff Alpha results for display.
    
    Args:
        alpha: Alpha coefficient
        ci_low: Lower confidence interval bound
        ci_high: Upper confidence interval bound
        level: Measurement scale
        items: Number of items
        raters: Number of raters
        
    Returns:
        Formatted results string
    """
    result_lines = []
    result_lines.append("Krippendorff's Alpha Results")
    result_lines.append("=" * 30)
    
    if level:
        result_lines.append(f"Measurement Scale: {level.capitalize()}")
    if items:
        result_lines.append(f"Items: {items}")
    if raters:
        result_lines.append(f"Raters: {raters}")
    
    result_lines.append(f"Alpha: {alpha:.4f}")
    
    if ci_low is not None and ci_high is not None:
        result_lines.append(f"95% CI: [{ci_low:.4f}, {ci_high:.4f}]")
    
    # Reliability interpretation
    if alpha >= 0.80:
        interpretation = "Acceptable (≥0.80)"
    elif alpha >= 0.67:
        interpretation = "Tentative (0.67-0.80)" 
    else:
        interpretation = "Unacceptable (<0.67)"
    
    result_lines.append(f"Reliability: {interpretation}")
    
    return "\n".join(result_lines)

def create_sample_data(n_items: int = 10, n_raters: int = 4, 
                      scale_values: Optional[List[int]] = None, 
                      agreement_level: str = 'medium') -> List[List[int]]:
    """
    Create sample data for testing and demonstration with realistic reliability patterns.
    
    Args:
        n_items: Number of items
        n_raters: Number of raters
        scale_values: Possible values (default: [1, 2, 3, 4, 5])
        agreement_level: 'high', 'medium', 'low'
        
    Returns:
        Sample data matrix
        
    Example:
        >>> data = create_sample_data(n_items=5, n_raters=3, agreement_level='high')
        >>> alpha = krippendorff_alpha(data, level='ordinal')
    """
    if scale_values is None:
        scale_values = [1, 2, 3, 4, 5]
    
    np.random.seed(42)  # For reproducible examples
    data = []
    
    # Create more realistic agreement patterns based on research literature
    if agreement_level == 'high':
        # Target: α ≈ 0.80-0.95 (acceptable reliability)
        agreement_strength = 0.9  # 90% perfect agreement
        systematic_bias = 0.05    # 5% systematic disagreement (±1 scale point)
        random_error = 0.05       # 5% random error
    elif agreement_level == 'medium':
        # Target: α ≈ 0.50-0.70 (marginal reliability)
        agreement_strength = 0.6  # 60% perfect agreement
        systematic_bias = 0.2     # 20% systematic disagreement 
        random_error = 0.2        # 20% random error
    else:  # low
        # Target: α ≈ 0.10-0.40 (poor reliability)
        agreement_strength = 0.3  # 30% perfect agreement
        systematic_bias = 0.3     # 30% systematic disagreement
        random_error = 0.4        # 40% random error (nearly random)
    
    for item_idx in range(n_items):
        # Choose a "true" value for this item
        true_value = np.random.choice(scale_values)
        item_ratings = []
        
        for rater_idx in range(n_raters):
            rand = np.random.random()
            
            if rand < agreement_strength:
                # Perfect agreement - use true value
                rating = true_value
            elif rand < agreement_strength + systematic_bias:
                # Systematic bias - consistent shift (simulate rater bias)
                bias_direction = 1 if rater_idx % 2 == 0 else -1  # Alternating bias
                bias_magnitude = 1 if agreement_level != 'low' else np.random.randint(1, 3)
                
                true_idx = scale_values.index(true_value)
                biased_idx = true_idx + (bias_direction * bias_magnitude)
                biased_idx = max(0, min(len(scale_values) - 1, biased_idx))
                rating = scale_values[biased_idx]
            else:
                # Random error - completely random rating
                rating = np.random.choice(scale_values)
            
            item_ratings.append(rating)
        
        data.append(item_ratings)
    
    return data

def get_reliability_interpretation(alpha: float) -> Dict[str, str]:
    """
    Get reliability interpretation following Krippendorff (2019) guidelines.
    
    Args:
        alpha: Alpha coefficient
        
    Returns:
        Dictionary with interpretation details
    """
    if alpha >= 0.80:
        return {
            'level': 'Acceptable',
            'description': 'Reliable for most research purposes',
            'recommendation': 'Proceed with analysis',
            'color': 'green'
        }
    elif alpha >= 0.67:
        return {
            'level': 'Tentative', 
            'description': 'Draw only tentative conclusions',
            'recommendation': 'Consider additional data collection',
            'color': 'orange'
        }
    else:
        return {
            'level': 'Unacceptable',
            'description': 'Insufficient reliability for research',
            'recommendation': 'Improve coding scheme or rater training',
            'color': 'red'
        }

def check_data_quality(data: List[List[Union[int, str]]]) -> Dict[str, Any]:
    """
    Analyze data quality and provide recommendations.
    
    Args:
        data: Input data matrix
        
    Returns:
        Data quality report
    """
    n_items = len(data)
    n_raters = len(data[0]) if data else 0
    
    # Count missing values
    total_cells = n_items * n_raters
    missing_count = 0
    for row in data:
        for val in row:
            if val == 'NA' or val == '' or pd.isna(val):
                missing_count += 1
    
    missing_percentage = (missing_count / total_cells) * 100 if total_cells > 0 else 0
    
    # Count items with sufficient raters
    sufficient_items = 0
    for row in data:
        valid_ratings = sum(1 for val in row if val != 'NA' and val != '' and not pd.isna(val))
        if valid_ratings >= 2:
            sufficient_items += 1
    
    # Get unique values
    unique_values = set()
    for row in data:
        for val in row:
            if val != 'NA' and val != '' and not pd.isna(val):
                unique_values.add(val)
    
    return {
        'n_items': n_items,
        'n_raters': n_raters,
        'total_cells': total_cells,
        'missing_count': missing_count,
        'missing_percentage': missing_percentage,
        'sufficient_items': sufficient_items,
        'insufficient_items': n_items - sufficient_items,
        'unique_values': len(unique_values),
        'values_range': f"{min(unique_values)} - {max(unique_values)}" if unique_values else "N/A"
    }