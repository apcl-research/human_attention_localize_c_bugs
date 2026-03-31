import pandas as pd
import argparse
import sys
import numpy as np
from sklearn.metrics import cohen_kappa_score

def calculate_agreement(file_path, col1, col2):
    try:
        # 1. Load data
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        # 2. Clean and Force Numeric
        # This handles the "mix of targets" error by ensuring everything is a float first
        df[col1] = pd.to_numeric(df[col1], errors='coerce')
        df[col2] = pd.to_numeric(df[col2], errors='coerce')
        
        # Drop rows where either grader is missing a score
        valid_data = df[[col1, col2]].dropna().copy()

        if len(valid_data) == 0:
            print("Error: No valid numeric data found in those columns.")
            return
        y_true = valid_data[col1].astype(str)
        y_pred = valid_data[col2].astype(str)
        print(f"y_true (Grader 1): {y_true.tolist()}\n y_pred (Grader 2): {y_pred.tolist()}")
      
        # 4. Calculate Weighted Kappa
        kappa = cohen_kappa_score(
            y_true, 
            y_pred, 
            weights='quadratic'
        )

        # 5. Identify Discrepancies (Difference >= 1.0)
        valid_data['diff'] = abs(valid_data[col1] - valid_data[col2])

        # 6. Final Report
        print("\n" + "="*45)
        print(f"PRE-DISCUSSION AGREEMENT REPORT")
        print("="*45)
        print(f"Items Analyzed: {len(valid_data)}")
        print(f"Weighted Kappa: {kappa:.4f}")
        
        if kappa > 0.75:
            print("Status:         EXCELLENT (Strong Alignment)")
        elif kappa > 0.40:
            print("Status:         MODERATE (Discussion Required)")
        else:
            print("Status:         POOR (Major Calibration Needed)")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path to spreadsheet")
    parser.add_argument("col1", help="Name of Grader 1 column")
    parser.add_argument("col2", help="Name of Grader 2 column")
    args = parser.parse_args()

    calculate_agreement(args.file, args.col1, args.col2)