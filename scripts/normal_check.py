import argparse
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import shapiro, normaltest
import sys

def check_normality(csv_path, column_name, plot=False):
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    if column_name not in df.columns:
        print(f"Column '{column_name}' not found in CSV.")
        print("Available columns:", ", ".join(df.columns))
        sys.exit(1)

    # Convert column to numeric, drop non-numeric and NaNs
    data = pd.to_numeric(df[column_name], errors='coerce').dropna()

    if len(data) < 3:
        print("Not enough valid numeric values to perform tests (need at least 3).")
        sys.exit(1)

    print(f"\nAnalyzing column: {column_name} ({len(data)} valid numeric values)")

    # Shapiro-Wilk Test
    shapiro_stat, shapiro_p = shapiro(data)
    print(f"\nShapiro-Wilk Test:\nStatistic = {shapiro_stat:.4f}, p-value = {shapiro_p:.4f}")
    print("=>", "Data looks normal (fail to reject H0)" if shapiro_p > 0.05 else "Data does NOT look normal (reject H0)")

    # D'Agostino and Pearson’s Test
    normaltest_stat, normaltest_p = normaltest(data)
    print(f"\nD’Agostino and Pearson’s Test:\nStatistic = {normaltest_stat:.4f}, p-value = {normaltest_p:.4f}")
    print("=>", "Data looks normal (fail to reject H0)" if normaltest_p > 0.05 else "Data does NOT look normal (reject H0)")

    # Skewness and Kurtosis
    skewness = data.skew()
    kurtosis = data.kurtosis()
    print(f"\nSkewness: {skewness:.4f}")
    print(f"Kurtosis: {kurtosis:.4f}")
    print("=> Positive skew" if skewness > 0.5 else "=> Negative skew" if skewness < -0.5 else "=> Skew is small")
    print("=> Heavy tails" if kurtosis > 1 else "=> Light tails" if kurtosis < -1 else "=> Kurtosis is close to normal")

    # Optional plotting
    if plot:
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.hist(data, bins=30, edgecolor='k')
        plt.title(f"Histogram: {column_name}")
        plt.xlabel(column_name)
        plt.ylabel("Frequency")

        plt.subplot(1, 2, 2)
        stats.probplot(data, dist="norm", plot=plt)
        plt.title("Q-Q Plot")

        plt.tight_layout()
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="Check if a column in a CSV is normally distributed.")
    parser.add_argument("csv_path", help="Path to the CSV file")
    parser.add_argument("column_name", help="Name of the column to check for normality")
    parser.add_argument("--plot", action="store_true", help="Show histogram and Q-Q plot")
    args = parser.parse_args()

    check_normality(args.csv_path, args.column_name, args.plot)

if __name__ == "__main__":
    main()
