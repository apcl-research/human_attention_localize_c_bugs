import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import argparse

def compute_pearson_with_significance(csv_path, alpha=0.05):
    # Load CSV and extract 6 columns starting from column C
    df = pd.read_csv(csv_path)
    selected = df.iloc[:, 2:8].copy()
    print(f"Selected columns: {selected.columns.tolist()}")

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
    parser.add_argument('--alpha', type=float, default=0.05, help='Significance level for hypothesis testing (default: 0.05).')

    args = parser.parse_args()
    print(f"Computing Pearson correlation for {args.csv_path} with alpha = {args.alpha}")

    compute_pearson_with_significance(args.csv_path, args.alpha)

if __name__ == '__main__':
    main()
