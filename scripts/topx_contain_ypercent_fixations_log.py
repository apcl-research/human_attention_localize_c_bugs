import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse
import numpy as np
import logging
import math
import csv 
from natsort import natsorted

def calculate_top_units(data, percentage, unit, count_col_name, curr_data=None):
    """
    Determines the number of units that contain the given percentage of the total fixations.
    """
    data_sorted = data.sort_values(by=count_col_name, ascending=False)
    
    total_fixations = data_sorted[count_col_name].sum()
    target_fixations = (percentage / 100) * total_fixations
    
    cumulative_fixations = data_sorted[count_col_name].cumsum()
    num_units = (cumulative_fixations <= target_fixations).sum() + 1  # Include the first unit exceeding the threshold
    
    max_count = max(data[count_col_name])
    if curr_data != None: 
        curr_data["total_fixations"] = int(total_fixations)
        curr_data["target_fixations"] = int(target_fixations)
        curr_data["num_units"] = int(num_units) 
        curr_data[f"total_{unit}"] = len(data_sorted)
        curr_data["percent_of_units"] = int(num_units) / len(data_sorted)
    return num_units, data_sorted, curr_data, max_count

def plot_fixation_distribution(data, bug, participant, percentage, output_dir, official_bug_names, unit, count_col_name, unit_col_name):
    """
    Generates and saves a bar plot of fixations per unit for a given participant and bug.
    """
    curr_data = {"bug": bug, "participant": participant}
    num_units, sorted_units, curr_data, max_count = calculate_top_units(data, percentage, unit, count_col_name, curr_data)
    
    plt.figure(figsize=(12, 6))
    plt.bar(sorted_units[unit_col_name], sorted_units[count_col_name], color='gray')
    plt.bar(sorted_units[unit_col_name][:num_units], sorted_units[count_col_name][:num_units], color='skyblue')
    if unit == "functions": 
        plt.xticks(rotation=45, ha='right')
    else: 
        plt.xticks([])
    plt.xlabel(unit_col_name)
    plt.ylabel('Fixation Count')
    official_bug = official_bug_names[bug]
    plt.title(f'{official_bug} - {participant} Top {num_units} {unit} out of {len(sorted_units)} Contain {percentage}% of Fixations')
    logging.info(f"{bug} - {participant} Top {num_units} {unit} out of {len(sorted_units)} Contain {percentage}% of Fixations")
    plt.tight_layout()
    
    # Save the plot
    plot_filename = f'{bug}_{official_bug}_{participant}_{percentage}percent.png'
    plt.savefig(os.path.join(output_dir, plot_filename))
    plt.close()
    
    return curr_data

def plot_bug_summary(bug_data, bug, percentage, output_dir, official_bug_names, unit, count_col_name, unit_max, y_cutoff=150):
    """
    Creates a single figure for each bug with subplots for each participant.
    Each subplot shows a maximum of unit_max individual units on the x-axis.
    If there are more than unit_max units, all remaining unit fixations are summed 
    and displayed as an additional bar. The x-axis labels will be "m1", "m2", etc.,
    and the extra bar will be labeled "m26-<total units>".
    """
    official_bug_name = official_bug_names[bug]

    # Determine maximum number of bars among participants after x-axis cutoff
    max_units = 0
    participant_sorted_units = {}
    participant_top_counts = {}
    bug_max = y_cutoff 
    for participant, data in bug_data.items():
        num_top, sorted_units, _, max_count = calculate_top_units(data, percentage, unit, count_col_name)
        if max_count > bug_max:
            bug_max = max_count
        participant_sorted_units[participant] = sorted_units
        participant_top_counts[participant] = num_top
        # If more than unit_max units, we'll display unit_max plus one extra "Other" bar.
        current_count = min(len(sorted_units), unit_max) + (1 if len(sorted_units) > unit_max else 0)
        max_units = max(max_units, current_count)
    
    bar_width = 0.8
    num_participants = len(bug_data)
    cols = min(3, num_participants)
    rows = math.ceil(num_participants / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 2.25, rows * 2.1), squeeze=False)
    
    def draw_break_marker(ax, x, width, y_cutoff):
        marker_gap = 4.2     # vertical distance below y_cutoff where marker starts
        marker_width = width * 0.8  # horizontal length of marker
        marker_slope = 2     # vertical rise for the marker
        
        y_start = y_cutoff - marker_gap
        x_start = x + width * 0.1
        ax.plot([x_start, x_start + marker_width],
                [y_start, y_start + marker_slope],
                color='black', lw=1, clip_on=False)
        ax.plot([x_start, x_start + marker_width],
                [y_start + 2, y_start + 2 + marker_slope],
                color='black', lw=1, clip_on=False)
    
    # Loop through each participant's subplot
    participant_sorted_units_items = natsorted(participant_sorted_units.items())
    for ax, (participant, sorted_units) in zip(axes.flatten(), participant_sorted_units_items):
        total_units = len(sorted_units)
        # If more than unit_max units, combine units from index unit_max onward
        if total_units > unit_max:
            top_data = sorted_units.iloc[:unit_max]
            remaining_data = sorted_units.iloc[unit_max:]
            extra_sum = remaining_data[count_col_name].sum()
            counts_to_plot = np.concatenate([top_data[count_col_name].to_numpy(), [extra_sum]])
            labels = [f"{unit[0]}{i+1}" for i in range(unit_max)] + [f"{unit[0]}{unit_max}-{total_units}"]
        else:
            counts_to_plot = sorted_units[count_col_name].to_numpy()
            labels = [f"f{i+1}" for i in range(total_units)]
        
        n = len(counts_to_plot)
        x_positions = np.arange(n)  # positions for bars
        
        # Plot gray bars for all units (or the summed extra bar)
        bars = ax.bar(x_positions, counts_to_plot, width=bar_width, color='gray', align='edge')
        # Highlight top units in blue.
        # If more than unit_max units, highlight only up to the unit_maxth bar.
        adjusted_top = min(participant_top_counts[participant], unit_max)
        ax.bar(x_positions[:adjusted_top], counts_to_plot[:adjusted_top], width=bar_width, color='skyblue', align='edge')

        
        ax.set_yscale('log')
        print(f"bug: {bug} bug_max: {bug_max}")
        ax.set_ylim(1, bug_max*1.2)
        ax.set_xlim(0, max_units)
        
        if total_units > unit_max:
            ax.set_xticks([x_positions[-1]])
            #ax.set_xticklabels([labels[-1]])
            ax.set_xticklabels([labels[-1]], fontsize=12)
            ax.bar(x_positions[-1], counts_to_plot[-1], width=bar_width, color='black', align='edge')
        else:  
            ax.set_xticklabels([])
        
        ax.set_title(f'{participant}: Top {adjusted_top}/{total_units} {unit}')
        #ax.set_title(f'{participant}: Top {adjusted_top}/{total_units} {unit}', fontsize=14)
        #ax.set_ylabel('Fixation Count', fontsize=12)
        ax.tick_params(axis='y', labelsize=12)
        
    for row in range(rows):
        axes[row, 0].set_ylabel('Fixation Count', fontsize=12)

    # Hide any unused subplots.
    for ax in axes.flatten()[len(bug_data):]:
        ax.axis('off')
    
   

    #fig.suptitle(f'Bug {official_bug_name} - Fixation Distribution ({percentage}%)', y=0.98)
    #fig.suptitle(f'Bug {official_bug_name} - Fixation Distribution ({percentage}%)', fontsize=18, y=0.98)
    #fig.subplots_adjust(top=0.85)
    plt.tight_layout()
    
    # Save the summary figure in both PNG and SVG formats.
    plot_filename = f'{bug}_{official_bug_name}_{unit}_summary_{percentage}percent_log'
    plt.savefig(os.path.join(output_dir, plot_filename+'.png'))
    plt.savefig(os.path.join(output_dir, plot_filename+'.svg'))
    plt.savefig(os.path.join(output_dir, plot_filename+'.pdf'))
    plt.close()

def save_dicts_to_csv(filename, data): 
    # Writing to CSV
    with open(filename, mode="w", newline="") as file:
        # Get fieldnames from the first dictionary
        fieldnames = data[0].keys()
        # Create DictWriter object
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # Write header
        writer.writeheader()
        # Write rows
        writer.writerows(data)

def main():
    """
    Parses command line arguments, reads the CSV file, processes fixation data, and generates plots.
    """
    parser = argparse.ArgumentParser(description='Process fixation data from a CSV file.')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file containing fixation data.')
    parser.add_argument('official_bug_names_csv', type=str, help='Path to the CSV file containing official bug names mapping.')
    parser.add_argument('--percentage', type=float, default=75, help='Percentage of fixations to consider (default: 75).')
    parser.add_argument('--unit', type=str, default="Functions", help='What type of data to graph. Options: Functions, Lines')
    parser.add_argument('--unit_max', type=int, default=25, help='Maximum number of units to display in the plot (default: 25).')
    args = parser.parse_args()

    if args.unit == "Functions":
        count_col_name = "Fixation Method Count"
        unit_col_name = "Fixation Method"
        unit = "fixations"
        y_cutoff = 100
    elif args.unit == "Lines":
        count_col_name = "Fixation Line Count"
        unit_col_name = "Fixation Line"
        unit = "lines"
        y_cutoff = 0
    else: 
        raise ValueError("Invalid tally type. Use 'Functions' or 'Lines'.")
    
    input_dir = os.path.dirname(os.path.abspath(args.csv_file))
    output_dir = os.path.join(input_dir, f'{unit}_fixation_plots_{args.percentage}')
    os.makedirs(output_dir, exist_ok=True)

    log_file = f"{output_dir}/topx_contain_ypercent_fixations.log"
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_file),
                            logging.StreamHandler()
                        ])
    
    agg_data = []
    df = pd.read_csv(args.csv_file)

    official_bug_names_df = pd.read_csv(args.official_bug_names_csv, header=None)  # No header row assumed
    official_bug_names = dict(zip(official_bug_names_df[0], official_bug_names_df[1]))  # Convert two columns into key-value pairs
    
    bug_participant_data = {}

    for (bug, participant), group in df.groupby(['Bug', 'Participant ID']):
        bug_participant_data.setdefault(bug, {})[participant] = group
        curr_data = plot_fixation_distribution(group, bug, participant, args.percentage, output_dir, official_bug_names, unit, count_col_name, unit_col_name)
        agg_data.append(curr_data)

    for bug, participant_data in bug_participant_data.items():
        plot_bug_summary(participant_data, bug, args.percentage, output_dir, official_bug_names, unit, count_col_name, args.unit_max, y_cutoff)

    logging.info(f"Plots saved in {output_dir}")
    
    # Specify the CSV file name
    filename = f"{output_dir}/aggregate_data.csv"
    save_dicts_to_csv(filename, agg_data)

    bug_names = ["ladybug", "stonefly", "hornet", "praying_mantis", "firefly", "silverfish", "spider", "weevil"]

    stats = {bug: [] for bug in bug_names}
    for task in agg_data: 
        bug_name = task["bug"]
        stats[bug_name].append(task) 
    

    results = []
    all_num_units = []
    all_percent_of_units = []

    for bug, entries in stats.items():
        num_units = [entry["num_units"] for entry in entries]
        percent_of_units = [entry["percent_of_units"] for entry in entries]
        all_num_units.extend(num_units)
        all_percent_of_units.extend(percent_of_units)
        results.append({
            "bug": bug,
            f"num_{unit}_mean": np.mean(num_units),
            f"num_{unit}_min": np.min(num_units),
            f"num_{unit}_max": np.max(num_units),
            f"num_{unit}_stddev": np.std(num_units, ddof=1),  # Using sample standard deviation
            f"percent_of_{unit}_mean": np.mean(percent_of_units),
            f"percent_of_{unit}_min": np.min(percent_of_units),
            f"percent_of_{unit}_max": np.max(percent_of_units),
            f"percent_of_{unit}_stddev": np.std(percent_of_units, ddof=1)
        })

    # Compute overall statistics
    all_num_units = np.array(all_num_units)
    all_percent_of_units = np.array(all_percent_of_units)

    results.append({
        "bug": "all_bugs", 
        f"num_{unit}_mean": np.mean(all_num_units),
        f"num_{unit}_min": np.min(all_num_units),
        f"num_{unit}_max": np.max(all_num_units),
        f"num_{unit}_stddev": np.std(all_num_units, ddof=1),
        f"percent_of_{unit}_mean": np.mean(all_percent_of_units),
        f"percent_of_{unit}_min": np.min(all_percent_of_units),
        f"percent_of_{unit}_max": np.max(all_percent_of_units),
        f"percent_of_{unit}_stddev": np.std(all_percent_of_units, ddof=1)
    }) 

    print(results)
    # Specify the CSV file name
    filename = f"{output_dir}/aggregate_data_stats.csv"
    save_dicts_to_csv(filename, results)

if __name__ == "__main__":
    main()