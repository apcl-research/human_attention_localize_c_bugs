import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import argparse

def compute_pearson_with_significance(csv_path, start_col=2, end_col=None, alpha=0.05):
    """
    Compute Pearson correlation matrix for a variable number of columns.
    
    Args:
        csv_path (str): Path to the CSV file
        start_col (int): Starting column index (0-based, default: 2 for column C)
        end_col (int): Ending column index (exclusive, default: None for all remaining columns)
        alpha (float): Significance level for hypothesis testing (default: 0.05)
    """
    # Load CSV
    df = pd.read_csv(csv_path)
    
    # Determine column range
    if end_col is None:
        end_col = len(df.columns)
    
    # Validate column indices
    if start_col < 0 or start_col >= len(df.columns):
        raise ValueError(f"start_col {start_col} is out of range. CSV has {len(df.columns)} columns.")
    if end_col <= start_col or end_col > len(df.columns):
        raise ValueError(f"end_col {end_col} is invalid. Must be > start_col ({start_col}) and <= {len(df.columns)}")
    
    # Extract selected columns
    selected = df.iloc[:, start_col:end_col].copy()
    print(f"Selected columns {start_col} to {end_col-1} (0-based): {selected.columns.tolist()}")
    print(f"Number of columns: {len(selected.columns)}")

    # Replace 'X' with NaN and convert to numeric
    selected = selected.replace('X', np.nan).apply(pd.to_numeric, errors='coerce')

    cols = selected.columns
    n = len(cols)

    # Initialize matrices
    corr_matrix = pd.DataFrame(np.nan, columns=cols, index=cols)
    pval_matrix = pd.DataFrame(np.nan, columns=cols, index=cols)
    sig_matrix = pd.DataFrame(False, columns=cols, index=cols)

    # Compute Pearson correlations and p-values
    for i in range(n):
        for j in range(n):
            col1 = selected.iloc[:, i]
            col2 = selected.iloc[:, j]
            valid = col1.notna() & col2.notna()

            if valid.sum() >= 2:
                r, p = pearsonr(col1[valid], col2[valid])
                corr_matrix.iloc[i, j] = r
                pval_matrix.iloc[i, j] = p
                sig_matrix.iloc[i, j] = p < alpha

    # Print results
    print("\nPearson Correlation Coefficient Matrix:")
    print(corr_matrix.round(3))

    print("\nP-value Matrix:")
    print(pval_matrix.round(4))

    print(f"\nSignificant Correlations (alpha = {alpha}):")
    print(sig_matrix)

    return corr_matrix, pval_matrix, sig_matrix

def main():
    parser = argparse.ArgumentParser(description='Compute Pearson correlation matrix from a CSV file.')
    parser.add_argument('csv_path', help='Path to the CSV file.')
    parser.add_argument('--start-col', type=int, default=2, 
                       help='Starting column index (0-based, default: 2 for column C).')
    parser.add_argument('--end-col', type=int, default=None,
                       help='Ending column index (exclusive, default: None for all remaining columns).')
    parser.add_argument('--alpha', type=float, default=0.05, 
                       help='Significance level for hypothesis testing (default: 0.05).')

    args = parser.parse_args()
    
    print(f"Computing Pearson correlation for {args.csv_path}")
    print(f"Column range: {args.start_col} to {args.end_col if args.end_col else 'end'}")
    print(f"Alpha: {args.alpha}")

    try:
        compute_pearson_with_significance(args.csv_path, args.start_col, args.end_col, args.alpha)
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

if __name__ == '__main__':
    main()
