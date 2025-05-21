#!/usr/bin/env python3
import argparse
import csv
import glob
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

def graph_stats(file_types_order, args): 
    color_map = {
        "all": "blue",
        "success": "green",
        "fail": "red",
        "confident": "green",
        "unsure": "red"
    }
    # Dictionary to hold data from each file type.
    # Structure: data_dict[file_type] = { bug: {"y": y_value, "participants": participants_value}, ... }
    data_dict = {}
    # Set to track all unique bug labels.
    all_bugs = set()

    # Process each file type in order.
    for file_type in file_types_order:
        # Look for CSV files with the exact file ending.
        pattern = os.path.join(args.folder, f"*_{file_type}.csv")
        matching_files = glob.glob(pattern)
        if not matching_files:
            print(f"No CSV file found for file type '{file_type}' with pattern {pattern}.")
            continue
        # Use the first matching file (modify this if you expect multiple files per type).
        csv_file = matching_files[0]
        
        with open(csv_file, mode='r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            header = next(reader)  # Read header row.
            next(reader)           # Skip the second row (not relevant).
            
            # Find column indices.
            try:
                bug_index = header.index("Bug")
            except ValueError:
                print(f"Column 'Bug' not found in {csv_file}. Skipping.")
                continue
            
            try:
                y_index = header.index(args.y_column)
            except ValueError:
                print(f"Column '{args.y_column}' not found in {csv_file}. Skipping.")
                continue
            if not args.no_participant_label: 
                try:
                    part_index = header.index("Number of Participants")
                except ValueError:
                    print(f"Column 'Number of Participants' not found in {csv_file}. Skipping.")
                    continue
            
            file_data = {}
            for row in reader:
                # Check if row has enough columns.
                if not args.no_participant_label: 
                    if len(row) <= max(bug_index, y_index, part_index):
                        continue
                else: 
                    if len(row) <= max(bug_index, y_index):
                        continue
                bug = row[bug_index]
                try:
                    y_value = float(row[y_index])
                except ValueError:
                    y_value = 0  # Default to 0 if conversion fails.
                # We keep the participants value as string (or convert to int if appropriate)
                if not args.no_participant_label: 
                    try:
                        participants = int(row[part_index])
                    except ValueError:
                        participants = row[part_index]
                    
                    file_data[bug] = {"y": y_value, "participants": participants}
                else: 
                    file_data[bug] = {"y": y_value}
                all_bugs.add(bug)
            
            data_dict[file_type] = file_data

    if not data_dict:
        print("No valid CSV data found.")
        exit(1)

    # Create a sorted list of all bugs.
    all_bugs = sorted(all_bugs)
    n_bugs = len(all_bugs)
    n_types = len(file_types_order)

    # Prepare the x-axis and calculate bar width.
    x = np.arange(n_bugs)
    bar_width = 0.8 / n_types

    # Set up the plot.
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot data for each file type in the specified order.
    for i, file_type in enumerate(file_types_order):
        if file_type not in data_dict:
            continue  # Skip missing file types.
        file_data = data_dict[file_type]
        
        # Align y values for all bugs, defaulting to 0 if missing.
        y_values = [file_data.get(bug, {"y": 0})["y"] for bug in all_bugs]
    
        # Calculate horizontal offset for grouped bars.
        offset = (i - (n_types - 1) / 2) * bar_width
        bars = ax.bar(x + offset, y_values, width=bar_width, 
                      label=file_type.capitalize(), color=color_map[file_type])  # <== Assign color dynamically
        
        if not args.no_participant_label: 
            # Also align participant values.
            participants_values = [file_data.get(bug, {}).get("participants", "") for bug in all_bugs]
            # Add text labels for the "Number of Participants" on top of each bar.
            for bar, part in zip(bars, participants_values):
                height = bar.get_height()
                # Only annotate if there's a non-empty participant value.
                if part != "" and args.no_participant_label == False:
                    ax.text(bar.get_x() + bar.get_width() / 2, height, str(part),
                            ha='center', va='bottom', fontsize=8)

    official_bug_names_df = pd.read_csv(args.official_bug_names_csv, header=None)  # No header row assumed
    official_bug_names = dict(zip(official_bug_names_df[0], official_bug_names_df[1]))  # Convert two columns into key-value pairs

    # Map x values to official bug names
    x_labels = [f"{official_bug_names.get(str(val), str(val))} ({str(val)})" for val in all_bugs]  # Default to the original value if not found
    #x_labels = [f"{official_bug_names.get(str(val), str(val))} ({val})" for val in set(all_bugs)]

    # Set the x-axis labels.
    ax.set_xticks(x)
    # Set new x-axis labels in the scatter plot
    ax.set_xticklabels(x_labels, rotation=45, ha="right")
    #ax.set_xticklabels(all_bugs, rotation=45, ha="right")
    ax.set_xlabel("Bug")
    ax.set_ylabel(args.y_column)
    ax.set_title(f"{args.y_column}")
    ax.legend(title="Data Type")
    plt.tight_layout()

    # Save the figure to the same folder as input data.
    output_name = "_".join(file_types_order)
    output_path = os.path.join(args.folder, f"{output_name}_comparison_plot.png")
    plt.savefig(output_path, dpi=300)
    print(f"Plot saved to {output_path}")

    # Show the plot.
    #plt.show()

# Set up command-line argument parsing.
parser = argparse.ArgumentParser(description="Plot grouped bar charts from specific CSV files with participant labels.")
parser.add_argument("folder", help="Folder containing the CSV files")
parser.add_argument("y_column", help="Column name to be used for the y-axis")
parser.add_argument('official_bug_names_csv', type=str, help='Path to the CSV file containing official bug names mapping.')
parser.add_argument("--no_participant_label", help="Don't put number of participants on top of bars", action="store_true")
args = parser.parse_args()

# Define the file types in the exact order for the graph.
file_type_groups = [
    ["all", "success", "fail", "confident", "unsure"],
    ["success", "fail"],
    ["confident", "unsure"]
]

for file_types_order in file_type_groups:
    graph_stats(file_types_order, args)