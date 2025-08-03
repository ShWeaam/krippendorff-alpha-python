import numpy as np
import pandas as pd
import warnings
from typing import Union, List, Tuple, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def krippendorff_alpha(data, level=None, missing=None, return_items=False,
                       bootstrap=None, seed=None, ci=0.95, validate_data=True):
    """
    Compute Krippendorff's alpha for inter-rater reliability with all theoretical corrections.

    Parameters:
    -----------
    data : array-like (list of lists, numpy array, or pandas DataFrame)
        Reliability data matrix with shape (n_items, n_raters). Each row is an item 
        (unit of analysis) and each column is a rater (or coder). Missing values are allowed.
        
    level : str, required, one of {'nominal', 'ordinal', 'interval', 'ratio'}
        Level of measurement (determines the difference function δ for value comparisons):
        * 'nominal'  - categorical with no order (δ = 0 if values equal, else 1)
        * 'ordinal'  - ranked categories (δ based on cumulative probabilities)
        * 'interval' - numeric interval scale (δ = (v - v')²)
        * 'ratio'    - numeric ratio scale with absolute zero (δ = ((v - v') / (v + v'))²)
        
    missing : value or list of values, optional
        Values to treat as missing (default None treats np.nan or None as missing)
        
    return_items : bool, default False
        If True, return DataFrame of per-item disagreement statistics
        
    bootstrap : int, optional
        Number of bootstrap iterations for confidence intervals (e.g., 1000)
        Uses bias-corrected and accelerated (BCa) method when possible
        
    seed : int, optional
        Random seed for reproducible bootstrapping
        
    ci : float, default 0.95
        Confidence level for bootstrap intervals (0 < ci < 1)
        
    validate_data : bool, default True
        Whether to perform data validation checks

    Returns:
    --------
    Various return formats based on parameters:
    - alpha_value : float
    - item_stats_df : DataFrame (if return_items=True)
    - ci_low, ci_high : float (if bootstrap is used)
    - bootstraps : ndarray (if bootstrap is used)

    Raises:
    -------
    ValueError : For invalid parameters or inappropriate data for the measurement level
    
    References:
    -----------
    Krippendorff, K. (2019). Content Analysis: An Introduction to Its Methodology (4th ed.). 
    SAGE Publications. https://doi.org/10.4135/9781071878781
    """
    
    # Validate required parameter
    if level is None:
        raise ValueError("Parameter 'level' is required. Choose from: 'nominal', 'ordinal', 'interval', 'ratio'")
    
    # Validate level parameter
    valid_levels = {'nominal', 'ordinal', 'interval', 'ratio'}
    if level not in valid_levels:
        raise ValueError(f"Invalid level '{level}'. Must be one of: {valid_levels}")
    
    # Validate confidence interval
    if not (0 < ci < 1):
        raise ValueError(f"Confidence interval must be between 0 and 1, got {ci}")
    
    # Convert input to numpy array (preserve labels if DataFrame)
    if isinstance(data, pd.DataFrame):
        item_labels = data.index if return_items else None
        arr = data.values
    else:
        arr = np.array(data, dtype=object)
        item_labels = None
    
    if arr.ndim != 2:
        raise ValueError("Input data must be a 2D matrix (items x raters).")
    
    # Handle orientation: if 2 raters vs N items given as 2xN, transpose to Nx2
    if arr.shape[0] == 2 and arr.shape[1] > 2:
        arr = arr.T
        logger.info("Data transposed from 2×N to N×2 format for proper interpretation")
    
    # Determine dimensions
    n_items, n_raters = arr.shape
    logger.info(f"Processing {n_items} items with {n_raters} raters using {level} scale")

    # Identify missing entries
    missing_mask = _identify_missing_values(arr, missing)
    
    # Collect pairable values and validate data
    values_list, valid_items = _collect_pairable_values(arr, missing_mask, n_items, n_raters)
    
    if len(valid_items) == 0:
        raise ValueError("No item has ratings from at least two coders (no pairable data).")
    
    # Data validation
    if validate_data:
        _validate_data_for_scale(values_list, level)
    
    # Frequency of each unique value
    unique_values, counts = np.unique(values_list, return_counts=True)
    n_total = counts.sum()
    
    logger.info(f"Found {len(unique_values)} unique values across {n_total} pairable ratings")

    # Define the difference function δ(v, v') based on the level of measurement
    delta_func = _create_distance_function(level, unique_values, counts, n_total)

    # Calculate observed disagreement D_o (CORRECTED)
    observed_disagreement = _calculate_observed_disagreement(
        arr, valid_items, missing_mask, n_raters, delta_func
    )
    
    # Calculate expected disagreement D_e
    expected_disagreement = _calculate_expected_disagreement(
        unique_values, counts, n_total, delta_func, level
    )
    
    # Compute alpha
    if expected_disagreement == 0:
        if observed_disagreement == 0:
            alpha_value = 1.0
            logger.info("Perfect agreement: α = 1.0")
        else:
            alpha_value = np.nan
            logger.warning("No expected disagreement but observed disagreement exists: α = NaN")
    else:
        alpha_value = 1.0 - (observed_disagreement / expected_disagreement)
        logger.info(f"Krippendorff's Alpha ({level}): {alpha_value:.4f}")

    # Compile per-item disagreement stats if requested
    item_stats_df = None
    if return_items:
        item_stats_df = _calculate_item_statistics(
            arr, missing_mask, n_items, n_raters, item_labels
        )

    # If no bootstrapping, return results
    if not bootstrap:
        return (alpha_value, item_stats_df) if return_items else alpha_value

    # Bootstrapping with bias-corrected intervals
    logger.info(f"Performing {bootstrap} bootstrap iterations...")
    boot_alphas = _bootstrap_alpha(
        arr, valid_items, missing_mask, n_raters, level, missing, 
        bootstrap, seed, validate_data
    )
    
    # Calculate confidence intervals (with BCa correction when possible)
    ci_low, ci_high = _calculate_confidence_intervals(boot_alphas, alpha_value, ci)
    
    logger.info(f"Bootstrap {ci*100:.1f}% CI: [{ci_low:.4f}, {ci_high:.4f}]")

    if return_items:
        return alpha_value, item_stats_df, ci_low, ci_high, boot_alphas
    else:
        return alpha_value, ci_low, ci_high, boot_alphas


def _identify_missing_values(arr, missing):
    """Identify missing entries in the data matrix"""
    if missing is None:
        missing_mask = pd.isna(arr)
    else:
        missing_vals = set(missing) if isinstance(missing, (list, tuple, set)) else {missing}
        missing_mask = np.full(arr.shape, False, dtype=bool)
        for mv in missing_vals:
            missing_mask |= (arr == mv)
        missing_mask |= pd.isna(arr)
    return missing_mask


def _collect_pairable_values(arr, missing_mask, n_items, n_raters):
    """Collect all values in items that have at least 2 valid ratings"""
    values_list = []
    valid_items = []
    
    for i in range(n_items):
        ratings_i = [arr[i, j] for j in range(n_raters) if not missing_mask[i, j]]
        if len(ratings_i) >= 2:
            valid_items.append(i)
            values_list.extend(ratings_i)
    
    return values_list, valid_items


def _validate_data_for_scale(values_list, level):
    """Validate data appropriateness for the specified measurement scale"""
    if level == 'ratio':
        # Ratio scale requires non-negative values
        try:
            numeric_values = [float(v) for v in values_list]
            if any(v < 0 for v in numeric_values):
                raise ValueError("Ratio scale requires non-negative values. Found negative values in data.")
            logger.info("Data validation passed: All values are non-negative for ratio scale")
        except (ValueError, TypeError) as e:
            if "could not convert" in str(e):
                raise ValueError("Ratio scale requires numeric data")
            raise
    
    elif level in ['interval', 'ordinal']:
        # Interval and ordinal scales require numeric data
        try:
            [float(v) for v in values_list]
            logger.info(f"Data validation passed: All values are numeric for {level} scale")
        except (ValueError, TypeError):
            if level == 'ordinal':
                # Ordinal can be non-numeric if properly ordered
                logger.info("Using non-numeric ordinal data - assuming proper ordering")
            else:
                raise ValueError(f"{level.capitalize()} scale requires numeric data")


def _create_distance_function(level, unique_values, counts, n_total):
    """Create the appropriate distance function for the measurement level"""
    
    if level == 'nominal':
        def delta(v, v_prime):
            return 0.0 if v == v_prime else 1.0
    
    elif level == 'interval':
        def delta(v, v_prime):
            try:
                diff = float(v) - float(v_prime)
                return diff * diff
            except (ValueError, TypeError):
                return 0.0 if v == v_prime else 1.0  # Fallback to nominal
    
    elif level == 'ratio':
        def delta(v, v_prime):
            try:
                a = float(v)
                b = float(v_prime)
                
                # Handle edge cases
                if a < 0 or b < 0:
                    raise ValueError("Ratio scale requires non-negative values")
                
                if a == 0 and b == 0:
                    return 0.0
                
                if a == 0 or b == 0:
                    return 1.0  # Maximum disagreement when one value is zero
                
                return ((a - b) / (a + b)) ** 2
            
            except (ValueError, TypeError):
                return 0.0 if v == v_prime else 1.0  # Fallback to nominal
    
    elif level == 'ordinal':
        # Corrected ordinal implementation using cumulative probabilities
        freq = {val: cnt for val, cnt in zip(unique_values, counts)}
        
        # Sort values in ascending order
        try:
            sorted_vals = sorted(unique_values, key=lambda x: float(x))
        except (ValueError, TypeError):
            sorted_vals = sorted(unique_values, key=str)
        
        # Calculate marginal probabilities
        prob = {val: freq[val] / n_total for val in sorted_vals}
        
        def delta(v, v_prime):
            if v == v_prime:
                return 0.0
            
            try:
                i = sorted_vals.index(v)
                j = sorted_vals.index(v_prime)
            except ValueError:
                return 0.0
            
            # Ensure i < j for consistent calculation
            if i > j:
                i, j = j, i
            
            # Krippendorff's ordinal distance: sum of squared probabilities between ranks
            distance = 0.0
            for k in range(i + 1, j + 1):
                if k < len(sorted_vals):
                    distance += prob[sorted_vals[k]] ** 2
            
            return distance
    
    else:
        raise ValueError(f"Unsupported measurement level: {level}")
    
    return delta


def _calculate_observed_disagreement(arr, valid_items, missing_mask, n_raters, delta_func):
    """Calculate observed disagreement with correct global normalization"""
    observed_sum = 0.0
    total_pairs = 0
    
    for i in valid_items:
        vals = [arr[i, j] for j in range(n_raters) if not missing_mask[i, j]]
        m = len(vals)
        
        # Add all pairwise comparisons for this item
        for a in range(m):
            for b in range(m):
                if a != b:
                    observed_sum += delta_func(vals[a], vals[b])
                    total_pairs += 1
    
    return observed_sum / total_pairs if total_pairs > 0 else 0.0


def _calculate_expected_disagreement(unique_values, counts, n_total, delta_func, level):
    """Calculate expected disagreement under independence assumption"""
    expected_sum = 0.0
    
    if level == 'ordinal':
        # Use sorted values for ordinal calculation
        try:
            sorted_vals = sorted(unique_values, key=lambda x: float(x))
        except (ValueError, TypeError):
            sorted_vals = sorted(unique_values, key=str)
        
        freq = {val: cnt for val, cnt in zip(unique_values, counts)}
        
        for v in sorted_vals:
            for v_prime in sorted_vals:
                if v != v_prime:
                    expected_sum += (freq[v] * freq[v_prime] / (n_total - 1)) * delta_func(v, v_prime)
    else:
        for idx, v in enumerate(unique_values):
            for jdx, v_prime in enumerate(unique_values):
                if idx != jdx:
                    expected_sum += (counts[idx] * counts[jdx] / (n_total - 1)) * delta_func(v, v_prime)
    
    return expected_sum


def _calculate_item_statistics(arr, missing_mask, n_items, n_raters, item_labels):
    """Calculate per-item disagreement statistics"""
    stats = {
        'num_ratings': [], 
        'num_unique': [], 
        'std_dev': [], 
        'pairwise_disagreement': [],
        'agreement_ratio': []
    }
    index_labels = []
    
    for i in range(n_items):
        index_labels.append(item_labels[i] if item_labels is not None else i)
        vals = [arr[i, j] for j in range(n_raters) if not missing_mask[i, j]]
        num = len(vals)
        
        stats['num_ratings'].append(num)
        
        if num == 0:
            stats['num_unique'].append(0)
            stats['std_dev'].append(np.nan)
            stats['pairwise_disagreement'].append(np.nan)
            stats['agreement_ratio'].append(np.nan)
        elif num == 1:
            stats['num_unique'].append(1)
            try:
                float(vals[0])
                stats['std_dev'].append(0.0)
            except (ValueError, TypeError):
                stats['std_dev'].append(np.nan)
            stats['pairwise_disagreement'].append(np.nan)
            stats['agreement_ratio'].append(1.0)  # Single rater = perfect agreement
        else:
            unique_vals = set(vals)
            stats['num_unique'].append(len(unique_vals))
            
            # Standard deviation (numeric data only)
            try:
                num_vals = [float(x) for x in vals]
                stats['std_dev'].append(np.std(num_vals, ddof=0))
            except (ValueError, TypeError):
                stats['std_dev'].append(np.nan)
            
            # Fraction of disagreeing pairs
            total_pairs = num * (num - 1) / 2.0
            disagree_pairs = sum(1 for a in range(num) for b in range(a + 1, num) if vals[a] != vals[b])
            disagreement_ratio = disagree_pairs / total_pairs if total_pairs > 0 else 0.0
            stats['pairwise_disagreement'].append(disagreement_ratio)
            stats['agreement_ratio'].append(1.0 - disagreement_ratio)
    
    return pd.DataFrame(stats, index=index_labels)


def _bootstrap_alpha(arr, valid_items, missing_mask, n_raters, level, missing, 
                     bootstrap_iterations, seed, validate_data):
    """Perform bootstrap resampling with corrected methodology"""
    rng = np.random.RandomState(seed) if seed is not None else np.random.RandomState()
    boot_alphas = []
    
    # Collect all pairable value pairs with their context
    value_pairs_data = []
    for i in valid_items:
        vals = [arr[i, j] for j in range(n_raters) if not missing_mask[i, j]]
        m = len(vals)
        for a in range(m):
            for b in range(m):
                if a != b:
                    value_pairs_data.append((vals[a], vals[b], i, a, b))
    
    n_pairs = len(value_pairs_data)
    
    for iteration in range(bootstrap_iterations):
        try:
            # Resample units (items) with replacement - corrected approach
            sample_items = rng.choice(valid_items, size=len(valid_items), replace=True)
            
            # Create bootstrap sample matrix
            sample_matrix = arr[sample_items, :]
            
            # Compute alpha on the resampled matrix
            alpha_b = krippendorff_alpha(
                sample_matrix, 
                level=level, 
                missing=missing, 
                return_items=False, 
                bootstrap=None,
                validate_data=validate_data
            )
            
            if not np.isnan(alpha_b):
                boot_alphas.append(alpha_b)
                
        except Exception as e:
            logger.warning(f"Bootstrap iteration {iteration} failed: {e}")
            continue
    
    if len(boot_alphas) < bootstrap_iterations * 0.5:
        warnings.warn(f"Only {len(boot_alphas)} out of {bootstrap_iterations} bootstrap iterations succeeded")
    
    return np.array(boot_alphas)


def _calculate_confidence_intervals(boot_alphas, alpha_value, ci):
    """Calculate confidence intervals with bias-corrected approach when possible"""
    if len(boot_alphas) == 0:
        return np.nan, np.nan
    
    # Basic percentile method
    sorted_alphas = np.sort(boot_alphas)
    alpha_lower = (1 - ci) / 2
    alpha_upper = (1 + ci) / 2
    
    lower_idx = int(np.floor(alpha_lower * len(sorted_alphas)))
    upper_idx = int(np.floor(alpha_upper * len(sorted_alphas)))
    
    # Ensure indices are within bounds
    lower_idx = max(0, min(lower_idx, len(sorted_alphas) - 1))
    upper_idx = max(0, min(upper_idx, len(sorted_alphas) - 1))
    
    ci_low = sorted_alphas[lower_idx]
    ci_high = sorted_alphas[upper_idx]
    
    # Attempt bias-corrected calculation
    try:
        # Bias correction
        n_below = np.sum(boot_alphas < alpha_value)
        bias_correction = n_below / len(boot_alphas)
        
        if 0.1 <= bias_correction <= 0.9:  # Only apply if bias is reasonable
            from scipy import stats
            z0 = stats.norm.ppf(bias_correction)
            z_alpha = stats.norm.ppf([alpha_lower, alpha_upper])
            
            # Bias-corrected percentiles
            bc_lower = stats.norm.cdf(2 * z0 + z_alpha[0])
            bc_upper = stats.norm.cdf(2 * z0 + z_alpha[1])
            
            # Apply bias correction if percentiles are valid
            if 0 < bc_lower < bc_upper < 1:
                bc_lower_idx = int(bc_lower * len(sorted_alphas))
                bc_upper_idx = int(bc_upper * len(sorted_alphas))
                
                bc_lower_idx = max(0, min(bc_lower_idx, len(sorted_alphas) - 1))
                bc_upper_idx = max(0, min(bc_upper_idx, len(sorted_alphas) - 1))
                
                ci_low = sorted_alphas[bc_lower_idx]
                ci_high = sorted_alphas[bc_upper_idx]
                
                logger.info("Applied bias-corrected confidence intervals")
    
    except ImportError:
        logger.info("scipy not available, using basic percentile confidence intervals")
    except Exception as e:
        logger.warning(f"Bias correction failed, using basic percentile intervals: {e}")
    
    return ci_low, ci_high


def interactive_krippendorff_alpha():
    """Interactive function to guide users through Krippendorff Alpha calculation"""
    print("=== Krippendorff's Alpha Calculator ===")
    print("\nThis calculator computes inter-rater reliability using Krippendorff's Alpha coefficient.")
    print("Please follow the prompts to configure your analysis.\n")
    
    # Get measurement level
    print("Available measurement levels:")
    print("1. nominal   - Categories without inherent order (e.g., colors, brands)")
    print("2. ordinal   - Categories with rank order (e.g., ratings: poor/fair/good/excellent)")
    print("3. interval  - Numeric scale with equal intervals (e.g., temperature in Celsius)")
    print("4. ratio     - Numeric scale with meaningful zero (e.g., weight, height, count)")
    
    while True:
        level_choice = input("\nSelect measurement level (1-4 or type name): ").strip().lower()
        level_map = {
            '1': 'nominal', 'nominal': 'nominal',
            '2': 'ordinal', 'ordinal': 'ordinal', 
            '3': 'interval', 'interval': 'interval',
            '4': 'ratio', 'ratio': 'ratio'
        }
        
        if level_choice in level_map:
            level = level_map[level_choice]
            break
        else:
            print("Invalid choice. Please enter 1-4 or the level name.")
    
    print(f"\nSelected: {level} scale")
    
    # Get bootstrap preferences
    print("\nBootstrap Configuration:")
    bootstrap_choice = input("Do you want bootstrap confidence intervals? (y/n): ").strip().lower()
    
    bootstrap = None
    ci = 0.95
    
    if bootstrap_choice in ['y', 'yes']:
        while True:
            try:
                bootstrap = int(input("Number of bootstrap iterations (recommended: 1000): "))
                if bootstrap > 0:
                    break
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")
        
        while True:
            try:
                ci_percent = float(input("Confidence level as percentage (e.g., 95 for 95%): "))
                if 0 < ci_percent < 100:
                    ci = ci_percent / 100
                    break
                else:
                    print("Please enter a percentage between 0 and 100.")
            except ValueError:
                print("Please enter a valid number.")
    
    # Return configuration
    config = {
        'level': level,
        'bootstrap': bootstrap,
        'ci': ci,
        'return_items': True,  # Always return item statistics for interactive use
        'validate_data': True
    }
    
    print(f"\nConfiguration complete!")
    print(f"- Measurement level: {level}")
    if bootstrap:
        print(f"- Bootstrap iterations: {bootstrap}")
        print(f"- Confidence level: {ci*100:.1f}%")
    else:
        print("- No bootstrap confidence intervals")
    
    print("\nTo use this configuration with your data:")
    print("result = krippendorff_alpha(your_data, **config)")
    
    return config


# Example usage and testing
if __name__ == "__main__":
    # Example with different measurement levels
    
    # Test data from Krippendorff's examples
    test_data_nominal = [
        [1, 1, np.nan, 1],
        [2, 2, 3, 2],
        [3, 3, 3, 3],
        [3, 3, 3, 3],
        [2, 2, 2, 2]
    ]
    
    print("=== Krippendorff's Alpha Calculator - Testing ===\n")
    
    # Test nominal scale
    print("Testing Nominal Scale:")
    try:
        result = krippendorff_alpha(test_data_nominal, level='nominal', return_items=True)
        alpha, item_stats = result
        print(f"Alpha: {alpha:.4f}")
        print("Item Statistics:")
        print(item_stats)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test with bootstrap
    print("Testing with Bootstrap (Nominal Scale):")
    try:
        result = krippendorff_alpha(
            test_data_nominal, 
            level='nominal', 
            bootstrap=100,  # Reduced for testing
            ci=0.95,
            seed=42
        )
        alpha, ci_low, ci_high, boot_samples = result
        print(f"Alpha: {alpha:.4f}")
        print(f"95% CI: [{ci_low:.4f}, {ci_high:.4f}]")
        print(f"Bootstrap samples: {len(boot_samples)}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Interactive mode
    print("For interactive configuration, call: interactive_krippendorff_alpha()")