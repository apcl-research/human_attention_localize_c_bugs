import argparse
import os
import pickle
import csv
import re
from datetime import datetime

def unpickle_and_convert(input_file, output_directory):
    # Load the pickle file
    with open(input_file, 'rb') as f:
        data = pickle.load(f)
        print(data)
    
    for k in data: 
        d = data[k]
    
        # Extract column names from the first dictionary (assuming all rows have the same columns)
        if data:
            col_names = d[0].keys()
            print(f"col_names: {col_names}")
            
            # Generate output file name with timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_filename = f"{os.path.basename(input_file).replace('.pkl', '.csv')}"
            output_path = os.path.join(output_directory, output_filename)
            
            # Open the output CSV file
            with open(output_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=col_names)
                
                # Write the header (column names)
                writer.writeheader()
                
                # Write the rows (each dictionary in the list)
                for row in d:
                    writer.writerow(row)
            print(f"Saved: {output_path}")

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Unpickle all files in a directory that match a pattern and output their contents to CSV files.")
    
    # Add arguments for input directory, pattern filter, and output directory
    parser.add_argument('input_directory', type=str, help="Directory containing input pickle files")
    parser.add_argument('pattern', type=str, help="Pattern filter for input files")
    parser.add_argument('output_directory', type=str, help="Directory to save output CSV files")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Process all matching files in the directory
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)
    
    for filename in os.listdir(args.input_directory):
        if re.search(args.pattern, filename) and filename.endswith(".pkl"):
            input_path = os.path.join(args.input_directory, filename)
            unpickle_and_convert(input_path, args.output_directory)

if __name__ == "__main__":
    main()
