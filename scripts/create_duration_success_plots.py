import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import os
from datetime import datetime
import numpy as np 

def convert_duration(duration_str):
    """
    Convert a duration string in the format "M:SS.s" (e.g., "9:00.0") to a float representing minutes.
    If the value is already numeric, it returns it as a float.
    """
    try:
        if isinstance(duration_str, str) and ":" in duration_str:
            parts = duration_str.split(":")
            if len(parts) >= 2:
                minutes = float(parts[0])
                seconds = float(parts[1])
                return minutes + seconds / 60.0
        return float(duration_str)
    except Exception as e:
        print(f"Error converting duration '{duration_str}': {e}")
        return None

def create_plot(df, bug_to_x, label, csv_index, output_dir, official_bug_names_csv): 
    official_bug_names_df = pd.read_csv(official_bug_names_csv, header=None)  # No header row assumed
    official_bug_names = dict(zip(official_bug_names_df[0], official_bug_names_df[1]))  # Convert two columns into key-value pairs

    # Map x values to official bug names
    x_labels = [official_bug_names.get(str(val), str(val)) for val in official_bug_names]  # Default to the original value if not found

    plt.figure(figsize=(10, 6))

    # Iterate over each row to plot points.
    for _, row in df.iterrows():
        bug = row.iloc[0]
        participant = row.iloc[1]
        try: 
            where_conf = float(row.iloc[csv_index]) 
        except Exception as e: 
            print(f"Could not convert to int for row: {row}")
            continue 
        duration = convert_duration(row.iloc[8])
        if duration is None:
            continue

        # Skip rows where the score is exactly 3.
        if where_conf == 3:
            continue

        # Determine the color based on score.
        if where_conf >= 4:
            color = "green"
        elif where_conf <= 2:
            color = "red"
        else:
            print(f"Reached not >= 4 or <= 2 or == 3, so cell has X")
            continue

        # Map the bug name to an x position.
        x = bug_to_x[bug]

        # Plot the scatter point and label it with the participant id.
        plt.scatter(x, duration, color=color)
        plt.text(x, duration, str(participant), fontsize=8, ha="right", va="bottom")

    # Create a legend for the color coding.
    high_patch = mlines.Line2D([], [], color="green", marker='o', linestyle='None',
                                 markersize=8, label=f"{label} >= 4")
    low_patch = mlines.Line2D([], [], color="red", marker='o', linestyle='None',
                                markersize=8, label=f"{label} <= 2")
    plt.legend(handles=[high_patch, low_patch])

    # Set the x-axis ticks to show the bug names.
    #plt.xticks(list(bug_to_x.values()), list(bug_to_x.keys()), rotation=45)
    # Set new x-axis labels in the scatter plot
    plt.xticks(ticks=np.arange(len(x_labels)), labels=x_labels, rotation=45, ha="right")
    plt.xlabel("Bug Name")
    plt.ylabel("Duration (minutes)")
    plt.title(f"Bug Duration by {label}")
    plt.tight_layout()
    
    # Save the plot with a descriptive name and a timestamp.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{label.replace(' ', '_')}_{timestamp}.png"
    save_path = os.path.join(output_dir, filename)
    plt.savefig(save_path)
    print(f"Scatter plot saved to: {save_path}")
    
    plt.show()

def create_box_plot_by_bug(df, label, csv_index, output_dir, official_bug_names_csv):
    """
    For each bug, create side-by-side box plots comparing durations for successful (>=4)
    and failure (<=2) participants.
    """
    official_bug_names_df = pd.read_csv(official_bug_names_csv, header=None)  # No header row assumed
    official_bug_names = dict(zip(official_bug_names_df[0], official_bug_names_df[1]))  # Convert two columns into key-value pairs

    # Map x values to official bug names
    x_labels = [official_bug_names.get(str(val), str(val)) for val in official_bug_names]  # Default to the original value if not found
    # Get the list of unique bugs (preserving the original order).
    bug_names = df.iloc[:, 0].unique().tolist()
    # Prepare lists to hold durations per bug.
    success_data = []
    failure_data = []
    
    # Loop through each bug.
    for bug in bug_names:
        df_bug = df[df.iloc[:, 0] == bug]
        success = []
        failure = []
        for _, row in df_bug.iterrows():
            try:
                score = float(row.iloc[csv_index])
            except Exception as e:
                continue
            if score == 3:
                continue
            duration = convert_duration(row.iloc[8])
            if duration is None:
                continue
            if score >= 4:
                success.append(duration)
            elif score <= 2:
                failure.append(duration)
        success_data.append(success)
        failure_data.append(failure)
    
    # Create positions for box plots.
    n = len(bug_names)
    # For each bug index, we offset positions for the two groups.
    positions_success = [i - 0.2 for i in range(n)]
    positions_failure = [i + 0.2 for i in range(n)]
    
    plt.figure(figsize=(12, 6))
    # Plot box plots for successful group.
    bp_success = plt.boxplot(success_data, positions=positions_success, widths=0.3, patch_artist=True, manage_ticks=False)
    # Plot box plots for failure group.
    bp_failure = plt.boxplot(failure_data, positions=positions_failure, widths=0.3, patch_artist=True, manage_ticks=False)
    
    # Set colors.
    for patch in bp_success['boxes']:
        patch.set_facecolor("green")
    for patch in bp_failure['boxes']:
        patch.set_facecolor("red")
    
    # Set x-ticks at the center of each pair.
    #plt.xticks(range(n), bug_names, rotation=45)
    # Set new x-axis labels in the scatter plot
    plt.xticks(ticks=np.arange(len(x_labels)), labels=x_labels, rotation=45, ha="right")
    plt.xlabel("Bug Name")
    plt.ylabel("Duration (minutes)")
    plt.title(f"Box Plot of Duration by {label} for Each Bug")
    
    # Create a custom legend.
    patch_success = mpatches.Patch(color="green", label="Successful (>=4)")
    patch_failure = mpatches.Patch(color="red", label="Failure (<=2)")
    plt.legend(handles=[patch_success, patch_failure])
    
    plt.tight_layout()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"BoxPlot_By_Bug_{label.replace(' ', '_')}_{timestamp}.png"
    save_path = os.path.join(output_dir, filename)
    plt.savefig(save_path)
    print(f"Box plot by bug saved to: {save_path}")
    plt.show()

def main():
    # TODO: Save these in a folder 
    # TODO: put the code name and the official name on the y axis 
    # TODO: allow to change the thresholds 
    # Set up command line argument parsing.
    parser = argparse.ArgumentParser(
        description="Scatter and box plots of bug duration with coloring based on confidence scores."
    )
    parser.add_argument("csv_file", help="Path to the CSV file")
    parser.add_argument('official_bug_names_csv', type=str, help='Path to the CSV file containing official bug names mapping.')
    args = parser.parse_args()

    # Read the CSV file.
    df = pd.read_csv(args.csv_file)

    # Determine the output directory (directory where the CSV file is located).
    output_dir = os.path.dirname(os.path.abspath(args.csv_file))
    if output_dir == "":
        output_dir = "."

    # Create a mapping from bug name to an x-axis position (for scatter plots).
    bug_names = df.iloc[:, 0].unique().tolist()
    bug_to_x = {bug: i for i, bug in enumerate(bug_names)}

    # Create scatter plots.
    create_plot(df, bug_to_x, "Where Confidence", 5, output_dir, args.official_bug_names_csv)
    create_plot(df, bug_to_x, "Where Accuracy", 7, output_dir, args.official_bug_names_csv)
    
    # Create box plots for each bug.
    create_box_plot_by_bug(df, "Where Confidence", 5, output_dir, args.official_bug_names_csv)
    create_box_plot_by_bug(df, "Where Accuracy", 7, output_dir, args.official_bug_names_csv)

if __name__ == "__main__":
    main()
