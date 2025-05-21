import argparse
import pickle
import csv

def unpickle_and_convert(input_file, output_file):
    # Load the pickle file
    with open(input_file, 'rb') as f:
        data = pickle.load(f)
        #print(data)
        
    
    for k in data: 
        d = data[k]
        print(f"key: {k}")
        print(f"len(d): {len(d)}")
        if len(d) == 0:
            print(f"WARNING: skipping {k}")
            continue
    
        # Extract column names from the first dictionary (assuming all rows have the same columns)
        if data:
            col_names = d[0].keys()
            #print(f"col_names: {col_names}")
            
            # Open the output CSV file
            with open(output_file, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=col_names)
                
                # Write the header (column names)
                writer.writeheader()
                
                # Write the rows (each dictionary in the list)
                for row in d:
                    writer.writerow(row)

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Unpickle a file and output its contents to a CSV file.")
    
    # Add arguments for input and output files
    parser.add_argument('input_file', type=str, help="Input pickle file")
    parser.add_argument('output_file', type=str, help="Output CSV file")
    
    # Parse the arguments
    args = parser.parse_args()

    # Unpickle the file and convert to CSV
    unpickle_and_convert(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
