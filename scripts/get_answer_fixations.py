import pickle
from statistics import mean, median
import argparse
import csv
import os 
import logging 
from datetime import datetime, timedelta
import pandas as pd 
from collections import Counter
import matplotlib.pyplot as plt
import logging
from matplotlib.patches import Patch
import csv
import numpy as np 
import copy
import math 
from scipy.stats import shapiro, mannwhitneyu, ttest_ind
import seaborn as sns
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches


def save_dicts_to_csv(data, filename):
    """
    Save a list of dictionaries to a CSV file.

    Parameters:
        data (list of dict): The data to write.
        filename (str): The path to the CSV file to save.
    """
    if not data:
        logging.info("No data to save.")
        return

    # Get the headers from the keys of the first dictionary
    fieldnames = data[0].keys()

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)

    logging.info(f"Saved {len(data)} rows to {filename}")

def get_duration(accuracy_duration_data, target_p, target_b): 
    for task in accuracy_duration_data: 
        if task["Bug"] == target_b and task["Participant ID"] == target_p: 
            return task["Duration"]
        
def get_accuracy(accuracy_duration_data, target_p, target_b): 
    for task in accuracy_duration_data: 
        if task["Bug"] == target_b and task["Participant ID"] == target_p: 
            #logging.info(f"Accuracy for {target_p} and {target_b}: {task['Where_Accuracy']}")
            return task["Where_Accuracy"]
    logging.error(f"Could not find accuracy for {target_p} and {target_b}")
        
def get_dicts_from_csv(file, accuracy_data=False, skip_fireflyp11=False): 
    # Get accuracy data
    with open(file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        if skip_fireflyp11 and accuracy_data:
            #data = [print(row) for row in reader]
            data = [row for row in reader if f"{row['Bug']}_{row['Participant ID']}" != "firefly_p11"]
        else: 
            data = list(reader)
    return data

def convert_system_to_datetime(system_time): 
    #logging.info(f"Converting system time: {system_time}")
    system_time = float(system_time) / 1000.0
    time = datetime.fromtimestamp(float(system_time))
    return time

def format_time(seconds):
    """Format seconds as mm:ss (omit hours)"""
    minutes = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{minutes:02}:{secs:02}"


def make_task_data(participant, bug, total_fixation, total_fixation_duration, correct_count, correct_duration, accuracy_duration_data, title="all", buffer=0): 
    task_data = {"participant": participant, 
                    "bug": bug,
                    "buffer": buffer,
                    "total_fixations": total_fixation,
                    "total_fixation_duration": total_fixation_duration,
                    "line": title,
                    "correct_fixations":  correct_count,
                    "correct_fixation_duration": correct_duration,
                    "where_accuracy": get_accuracy(accuracy_duration_data, participant, bug),
                    "task_duration": get_duration(accuracy_duration_data, participant, bug)
    }
    return task_data 

def get_ylim(y): 
    sorted_values = sorted(y)  # Returns a new sorted list
    n = len(sorted_values)
    index = math.ceil(0.99 * n) - 1
    cutoff = sorted_values[index]
    return cutoff

def make_chart(bug, participant, lines, correct_lines, output_dir, accuracy_duration_data, buffer=0):
    x = []
    heights = []
    colors = []
    correct_count = 0 
    correct_duration = 0 
    total_fixation_duration = 0 
    

    correct_lines_count = copy.deepcopy(correct_lines)
    for cl in correct_lines_count: 
        cl["count"] = 0
        cl["duration"] = 0

    for i,line in enumerate(lines):
        if i == 0: 
            start_time = convert_system_to_datetime(int(line["system_time"])) 
        x_val = (convert_system_to_datetime(int(line["system_time"])) - start_time).total_seconds()
        height = int(line["duration"]) 
        total_fixation_duration += height

        # Check if the line is the correct line (or within the buffer)
        correct_color = "gray"
        for cl in correct_lines_count: 
            #print(f"{i} Checking if participant looked at line {cl['line_num']}")
            is_correct = (
                line["fixation_target"] == cl["file"] and
                int(cl["line_num"]) - buffer <= line["line_num"] <= int(cl["line_num"]) + buffer
            )

            if is_correct:
                logging.debug(f"Participant {participant} for bug {bug} looked at the correct line!")
                correct_count += 1 
                correct_duration += line["duration"]
                correct_color = cl["color"]
                cl["count"] += 1 
                cl["duration"] += line["duration"]
                break

        x.append(x_val)
        heights.append(height)
        colors.append(correct_color if is_correct else "gray")

    #plt.figure(figsize=(5, 2.5))
    plt.figure(figsize=(5, 3.5))
    
    x0 = x[0]
    xlen = x[len(x)-1]
    xdiff = xlen - x0 
    xwidth = xdiff / len(x)
    bars = plt.bar(x, heights, color=colors, width=xwidth)
    plt.xlabel("Time Since First Fixation (minutes)")
    ylabel = plt.ylabel("Fixation Duration (ms)")
    ylabel.set_position((-0.1, 0.50))  # Lower than default
    #plt.title(f"Fixation Durations for Participant {participant} on Bug {bug} with Buffer={buffer}", pad=20)
    # Determine tick positions every 30 seconds
    start_time = min(x)
    end_time = max(x)
    tick_positions = np.arange(start_time, end_time + 1, 120)  # Every 30 seconds
    # Set custom ticks for x-axis
    plt.xticks(tick_positions, [format_time(tick) for tick in tick_positions], rotation=45)
    legend_elements = [
        Patch(facecolor='gray', label='Other Fixation')
    ]
    for cl in correct_lines_count: 
        legend_elements.append(Patch(facecolor=cl["color"], label=f'{cl["file"]}:{cl["line_num"]}'))
    
    #plt.legend(handles=legend_elements, loc='upper right')
    # plt.legend(
    #     handles=legend_elements,
    #     title="Correct Lines",
    #     loc='center left',
    #     bbox_to_anchor=(1.02, 0.5),  # just outside the right of the axes
    #     borderaxespad=0,
    #     frameon=False  # optional
    # )
    # plt.tight_layout(rect=[0, 0, 1, 1])

    if bug == "weevil": 
        legend_cols = 2
    else: 
        legend_cols = 4
    plt.legend(
        handles=legend_elements,
        loc='lower center',
        bbox_to_anchor=(0.42, 1.01),
        columnspacing=0.4,
        ncol=legend_cols,            # Adjust based on number of items
        frameon=False,     # Optional
        title="Fixation Lines"
    )
    #plt.tight_layout(rect=[0, 0, 1, 1])
    plt.subplots_adjust(left=0.15, right=0.95, top=0.8, bottom=0.2)


    y_cutoff = get_ylim(heights)
    #y_cutoff = 20000
    logging.debug(f"ycutoff: {y_cutoff}")
    plt.ylim(0,y_cutoff)
    for bar in bars:
            height = bar.get_height()
            if height > y_cutoff:
                barx = bar.get_x()
                width = bar.get_width()
                plt.text(barx + width/2, y_cutoff, f'*', ha='center', va='top', fontsize=12, rotation=90)
                #plt.text(barx + width/2, y_cutoff + y_cutoff*0.07, f'{int(height)}', ha='center', va='top', fontsize=12, rotation=90)

    output_path = f"{output_dir}/{participant}_{bug}_Buffer{buffer}.pdf"
    plt.savefig(output_path)
    logging.info(f"Plot saved to {output_path}")
    #plt.show() 
    plt.close()

    task_datas = [] 
    task_datas.append(make_task_data(participant, bug, len(x), total_fixation_duration, correct_count, correct_duration, accuracy_duration_data, title="all", buffer=buffer))
    for cl in correct_lines_count: 
        task_datas.append(make_task_data(participant, bug, len(x), total_fixation_duration, cl["count"], cl["duration"], accuracy_duration_data, title=f"{cl["file"]}:{cl["line_num"]}", buffer=buffer))
    return task_datas

def get_correct_lines(correct_lines_data, bug):
    correct_lines = []
    for line in correct_lines_data: 
        if line["bug"] == bug: 
            correct_lines.append(line)
    return correct_lines
                
def make_charts(flines, output_dir, accuracy_duration_data, correct_lines_data, buffer=0): 
    summary = []

    for bug in flines: 
        bug_dir = f"{output_dir}/{bug}"
        os.mkdir(bug_dir)
        correct_lines = get_correct_lines(correct_lines_data, bug)
        for participant in flines[bug]: 
            #print(f"Correct lines: {correct_lines}")
            logging.info(f"Creating chart for {bug}, {participant}")
            task_datas = make_chart(bug, participant, flines[bug][participant], correct_lines, bug_dir, accuracy_duration_data, buffer=buffer)
            for task_data in task_datas: 
                summary.append(task_data)
    return summary 

def get_lines(bug, flines, participant_id, session, data): 
    if bug not in flines.keys(): 
        logging.warning(f"add_line_counts: BUG {bug} NOT IN KEYS!")

    fixation_lines = [] 
    for fixation in data[session]: 
        if fixation["duration"] < 60000: # discard fixations longer than 1 min
            fixation_lines.append({"system_time": fixation['system_time'], "fixation_target":fixation['fixation_target'],"line_num":fixation['source_file_line'], "token": fixation['token'], "duration":fixation["duration"], "source_file_col":fixation["source_file_col"], "x":fixation["x"], "y":fixation["y"], 'right_pupil_diameter': fixation['right_pupil_diameter'], 'left_pupil_diameter': fixation['left_pupil_diameter']})

    if participant_id in flines[bug]: 
            logging.info(f"add_line_counts: Found second database for participant {participant_id} and bug {bug}: {session}")
            logging.info(f"add_line_counts: Previous length was {len(flines[bug][participant_id])}, current length: {len(fixation_lines)}")
            flines[bug][participant_id].extend(fixation_lines)
            logging.info(f"add_line_counts: Now {participant_id} length of flines[{bug}][{participant_id}] is {len(flines[bug][participant_id])}")
    else: 
        flines[bug][participant_id] = fixation_lines
    return flines

def parse_data(data, skip_fireflyp11=False): 
    bug_names = ["ladybug", "stonefly", "hornet", "praying_mantis", "firefly", "silverfish", "spider", "weevil"]
    flines = {bug: {} for bug in bug_names}

    for session in data:
        logging.info("\n")
        logging.info(f"session: {session}")
        try: 
            bug = data[session][0]["bug_name"]
            participant_id = data[session][0]["participant_id"]
            if skip_fireflyp11 and participant_id == 'p11' and bug == "firefly":
                logging.info(f"Skipping participant 11 for firefly")
                continue
            logging.info(f"bug name: {bug}, participant_id: {participant_id}")
            flines = get_lines(bug, flines, participant_id, session, data)
        except Exception as e: 
            logging.error(f"Could not get data for session: {session} because: {e}")
        
    return flines 

def load_data(input_filename): 
    data = pickle.load(open(input_filename, "rb"))
    return data 

def make_correct_percent_by_accuracy(data, save_name): 
    print("In make_correct_percent_by_accuracy")
    print(data)
    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Convert relevant columns to numeric
    df['total_fixations'] = pd.to_numeric(df['total_fixations'], errors='coerce')
    df['correct_fixations'] = pd.to_numeric(df['correct_fixations'], errors='coerce')
    df['where_accuracy'] = pd.to_numeric(df['where_accuracy'], errors='coerce')

    # Compute percent_correct
    df['percent_correct'] = df['correct_fixations'] / df['total_fixations']

    # Filter for 'line' == 'all'
    df_all = df[df['line'] == 'all'].copy()

    # Create a label for x-axis
    df_all['participant_bug'] = df_all['participant'] + ' - ' + df_all['bug']

    # Sort by where_accuracy
    df_all.sort_values('where_accuracy', inplace=True)

    # Normalize where_accuracy for colormap
    norm = mcolors.Normalize(vmin=df_all['where_accuracy'].min(), vmax=df_all['where_accuracy'].max())
    colors = cm.viridis(norm(df_all['where_accuracy']))

    # Plotting
    plt.figure(figsize=(4.86, 2.66))
    bars = plt.bar(
        df_all['participant_bug'],
        df_all['percent_correct'],
        color=colors
    )

    # Create legend manually using rounded accuracy values
    unique_acc = sorted(df_all['where_accuracy'].unique())
    legend_patches = [
        mpatches.Patch(color=cm.viridis(norm(acc)), label=f'{acc:.2f}')
        for acc in unique_acc
    ]
    #plt.legend(handles=legend_patches, title="Where Accuracy")
    
    plt.legend(
        handles=legend_patches,
        title="Where Accuracy",
        bbox_to_anchor=(1.05, 1),  # Move legend outside plot
        loc='upper left',
        borderaxespad=0.
    )
    
    # Formatting
    #plt.xticks(rotation=30, ha='right', fontsize=8)
    plt.xticks([])
    plt.ylabel('Percent Correct Fixations')
    #plt.title('Percent Correct by Participant-Bug, Color-coded by Where Accuracy')
    # Format y-axis as percentages
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
    plt.tight_layout()
    #plt.show()
    plt.savefig(f"{save_name}.png")
    plt.savefig(f"{save_name}.svg")
    plt.savefig(f"{save_name}.pdf")
    return df 
    

  

def create_summary(flines, output_dir, accuracy_duration_data, correct_lines_data, buffer=0): 
    buffer_dir = f"{output_dir}/buffer{buffer}"
    os.mkdir(buffer_dir)
    summary = make_charts(flines, buffer_dir, accuracy_duration_data, correct_lines_data, buffer=buffer)
    #print(summary)
    df = make_correct_percent_by_accuracy(summary, f"{buffer_dir}/correct_percent_by_accuracy")
    summary_output_file = f"{buffer_dir}/summary_buffer{buffer}.csv"
    #save_dicts_to_csv(summary, summary_output_file)
    df.to_csv(summary_output_file, index=False)

def flatten_flines(flines, accuracy_duration_data): 
    flattened = []

    for bug, participants in flines.items():
        for participant, fixations in participants.items():
            for fixation in fixations:
                row = {
                    'bug': bug,
                    'participant': participant,
                    **fixation  # merge fixation data into the row
                }
                flattened.append(row)

    df = pd.DataFrame(flattened)
    df = df.sort_values(by=['bug', 'participant', 'system_time']) \
       .reset_index(drop=True)

    df['Where_Accuracy'] = None
    df['Where_Accuracy'] = df.apply(
        lambda row: get_accuracy(accuracy_duration_data, row['participant'], row['bug']),
        axis=1
    )
    
    return df 

def add_significant_dwells(df): 
    df['significant_dwell'] = (df['same_line_fixations_next_30s'] > 4) | (df['same_line_duration_next_30s'] > 4000)
    return df 

def add_next_fixation_same(df):
    # Compare each row with the next row
    df['next_bug'] = df['bug'].shift(-1)
    df['next_participant'] = df['participant'].shift(-1)
    df['next_target'] = df['fixation_target'].shift(-1)
    df['next_line'] = df['line_num'].shift(-1)
    df['next_token'] = df['token'].shift(-1)
    df['next_col'] = df['source_file_col'].shift(-1)
    df['next_x'] = df['x'].shift(-1)
    df['next_y'] = df['y'].shift(-1)

    # Basic sameness checks
    same_context = (
        (df['bug'] == df['next_bug']) &
        (df['participant'] == df['next_participant']) &
        (df['fixation_target'] == df['next_target'])
    )

    df['next_fixation_same_line'] = same_context & (df['line_num'] == df['next_line'])

    df['next_fixation_same_token'] = (
        df['next_fixation_same_line'] &
        (df['token'] == df['next_token'])
    )

    # Calculate line distance if in same file context
    df['line_distance_to_next'] = abs(df['next_line'] - df['line_num'])
    df.loc[~same_context, 'line_distance_to_next'] = None  # or np.nan to ignore across files

    # Calculate col distance if in the same line 
    df['col_distance_to_next'] = abs(df['next_col'] - df['source_file_col'])
    df.loc[~df['next_fixation_same_line'], 'col_distance_to_next'] = None  # or np.nan to ignore across files

    # Calculate euclidean distance if in the same file context 
    df['euclidean_distance_to_next'] = np.sqrt(
        (df['next_x'] - df['x'])**2 +
        (df['next_y'] - df['y'])**2
    )
    df.loc[~same_context, 'euclidean_distance_to_next'] = None  # or np.nan to ignore across files

    # Calculate x difference if in the same file 
    df['x_diff_to_next_same_file'] = df['next_x'] - df['x']
    df.loc[~same_context, 'x_diff_to_next_same_file'] = None  # or np.nan to ignore across files

    # Calculate y difference if in the same file    
    df['y_diff_to_next_same_file'] = df['next_y'] - df['y']
    df.loc[~same_context, 'y_diff_to_next_same_file'] = None  # or np.nan to ignore across files

    # TODO: do we maybe only want to do this if they are actually looking in a different spot? 
    # Calculate angle 
    df['angle_to_next_same_file'] = (((np.arctan2(df['y_diff_to_next_same_file'], df['x_diff_to_next_same_file'])) * 180 / np.pi) + 360) % 360 # convert to [0, 360]
    df.loc[~same_context, 'angle_to_next_same_file'] = None  # or np.nan to ignore across files

    # Bin into 8 directions
    bins = [0, 45, 90, 135, 180, 225, 270, 315, 360]
    labels = ['right', 'up_right', 'up', 'up_left', 'left', 'down_left', 'down', 'down_right']

    df['direction_to_next_same_file'] = pd.cut(df['angle_to_next_same_file'], bins=bins, labels=labels, right=False, include_lowest=True)
    df.loc[~same_context, 'direction_to_next_same_file'] = None  # or np.nan to ignore across files


    # Calculate x and y difference and angle even if not in same file 
    df['x_diff_to_next'] = df['next_x'] - df['x']
    df['y_diff_to_next'] = df['next_y'] - df['y']

    df['angle_to_next'] = (((np.arctan2(df['y_diff_to_next'], df['x_diff_to_next'])) * 180 / np.pi) + 360) % 360 # convert to [0, 360]
    df['direction_to_next'] = pd.cut(df['angle_to_next'], bins=bins, labels=labels, right=False, include_lowest=True)

    # Clean up helper columns
    df.drop(columns=['next_bug', 'next_participant', 'next_target', 'next_line', 'next_token', 'next_col', 'next_x', 'next_y'], inplace=True)

    return df

def add_next_file_different(df): 
    file_list = ["StudyProcedure.c", "StudyInstructions.c", "ladybug.c", "stonefly.c", "hornet.c", "silverfish.c", "praying_mantis.c", "spider.c", "weevil.c", "firefly.c", "pre-study.c", "post-study.c"]
    # Shift to get the next row values
    df['next_bug'] = df['bug'].shift(-1)
    df['next_participant'] = df['participant'].shift(-1)
    df['next_target'] = df['fixation_target'].shift(-1)

    # Check for same bug and participant but different file
    same_task = (df['bug'] == df['next_bug']) & (df['participant'] == df['next_participant'])
    file_changed = df['fixation_target'] != df['next_target']
    switch_happened = same_task & file_changed
    df['next_fixation_different_file'] = switch_happened

    # Determine if switch is to or from a file in the list, but between files in the list don't count 
    df['code_report_switch'] = (switch_happened & df['fixation_target'].isin(file_list) & ~df['next_target'].isin(file_list)) | (switch_happened & ~df['fixation_target'].isin(file_list) & df['next_target'].isin(file_list))
    
    # Optionally, drop helper columns
    df.drop(columns=['next_bug', 'next_participant', 'next_target'], inplace=True)

    return df

def get_count_and_percentage(df, accuracy_duration_data, dwells=False): 
    # Step 1: Add temporary Boolean columns for each direction
    direction_labels = df['direction_to_next_same_file'].dropna().unique()

    for direction in direction_labels:
        col_name_same_file = f'is_{direction}_same_file'
        df[col_name_same_file] = df['direction_to_next_same_file'] == direction
        col_name = f'is_{direction}'
        df[col_name] = df['direction_to_next'] == direction

    # Step 2: Group by 'bug' and 'participant'
    grouped = df.groupby(['bug', 'participant'])

    # Step 3: Create direction-related aggregation dictionary
    direction_agg_same_file = {
        f'is_{direction}_count_same_file': (f'is_{direction}_same_file', 'sum')
        for direction in direction_labels
    }
    direction_agg = {
        f'is_{direction}_count': (f'is_{direction}', 'sum')
        for direction in direction_labels
    }

    # Calculate the count of True values in 'next_fixation_same_line' and 'next_fixation_same_token'
    if dwells: 
        result = grouped.agg(
            count_same_line=('next_fixation_same_line', 'sum'),      # Count of True in next_fixation_same_line
            count_same_token=('next_fixation_same_token', 'sum'),    # Count of True in next_fixation_same_token
            count_diff_file=('next_fixation_different_file', 'sum'),          # Count of True in next_fixation_different_file
            count_code_report_switch=('code_report_switch', 'sum'),          # Count of True in code_report_switch
            count_significant_dwells=('significant_dwell', 'sum'),  # Count of significant dwells
            average_line_distance=('line_distance_to_next', 'mean'),  # Average line distance
            average_col_distance=('col_distance_to_next', 'mean'),    # Average column distance
            average_euclidean_distance=('euclidean_distance_to_next', 'mean'),  # Average Euclidean distance
            average_left_pupil_diameter=('left_pupil_diameter', 'mean'),  # Average left pupil diameter
            average_right_pupil_diameter=('right_pupil_diameter', 'mean'),  # Average right pupil diameter
            total_count=('next_fixation_same_line', 'size'),          # Total count of rows
            **direction_agg_same_file,  # Add the direction counts
            **direction_agg
        )
        result['significant_dwells_normalized_by_total_fixations'] = result['count_significant_dwells'] / result['total_count'] * 100
    else: 
        result = grouped.agg(
            count_same_line=('next_fixation_same_line', 'sum'),      # Count of True in next_fixation_same_line
            count_same_token=('next_fixation_same_token', 'sum'),    # Count of True in next_fixation_same_token
            count_diff_file=('next_fixation_different_file', 'sum'),          # Count of True in next_fixation_different_file
            count_code_report_switch=('code_report_switch', 'sum'),          # Count of True in code_report_switch
            average_line_distance=('line_distance_to_next', 'mean'),  # Average line distance
            average_col_distance=('col_distance_to_next', 'mean'),    # Average column distance
            average_euclidean_distance=('euclidean_distance_to_next', 'mean'),  # Average Euclidean distance
            average_left_pupil_diameter=('left_pupil_diameter', 'mean'),  # Average left pupil diameter
            average_right_pupil_diameter=('right_pupil_diameter', 'mean'),  # Average right pupil diameter
            total_count=('next_fixation_same_line', 'size'),          # Total count of rows
            **direction_agg_same_file,  # Add the direction counts
            **direction_agg
        )

    print(result)
    # Calculate the percentage for each
    result['percentage_next_line_same'] = (result['count_same_line'] / result['total_count']) * 100
    result['percentage_next_token_same'] = (result['count_same_token'] / result['total_count']) * 100
    result['percentage_next_file_diff'] = (result['count_diff_file'] / result['total_count']) * 100
    result['percentage_code_report_switch'] = (result['count_code_report_switch'] / result['total_count']) * 100
    
    for direction in direction_labels:
        col_name_same_file = f'is_{direction}_count_same_file'
        result[f'percentage_{direction}_same_file'] = (result[col_name_same_file] / result['total_count']) * 100
        col_name = f'is_{direction}_count'
        result[f'percentage_{direction}'] = (result[col_name] / result['total_count']) * 100

    # Reset index for better readability (optional)
    result.reset_index(inplace=True)
    
    # Initialize the column with NaNs
    result['Where_Accuracy'] = None
    result['Where_Accuracy'] = result.apply(
        lambda row: get_accuracy(accuracy_duration_data, row['participant'], row['bug']),
        axis=1
    )
    
    return result 

def add_dwell_counts(df):
    # Convert system time to datetime if not already done
    if 'datetime' not in df.columns:
        df['datetime'] = df['system_time'].apply(convert_system_to_datetime)

    # Sort to ensure correct ordering
    df = df.sort_values(by=['bug', 'participant', 'datetime']).reset_index(drop=True)

    counts = []
    durations = []


    for i, row in df.iterrows():
        current_time = row['datetime']
        bug = row['bug']
        participant = row['participant']
        line_num = row['line_num']
        target = row['fixation_target']

        # Filter down to same bug + participant
        window = df[
            (df['bug'] == bug) &
            (df['participant'] == participant) &
            (df['datetime'] >= current_time) & 
            (df['datetime'] <= current_time + timedelta(seconds=30))
        ]

        # restrict to same line+file
        same_line = window[
            (window['line_num'] == line_num) &
            (window['fixation_target'] == target)
        ]

        counts.append(len(same_line))
        durations.append(same_line['duration'].sum())

    df['same_line_fixations_next_30s'] = counts
    df['same_line_duration_next_30s'] = durations

    return df

def report_duplicates(df):
    # Define the columns that should uniquely identify a fixation
    key_cols = ['bug', 'participant', 'system_time', 
                'fixation_target', 'line_num', 'token', 'duration']

    # Find rows that are exact duplicates on those keys
    dup_mask = df.duplicated(subset=key_cols, keep=False)
    dup_rows = df[dup_mask]

    if dup_rows.empty:
        print("✅ No duplicates found.")
        return

    # Count duplicates per bug/participant
    counts = dup_rows.groupby(['bug', 'participant']).size().reset_index(name='dup_count')

    # Report
    print("⚠️ Found duplicates for these bug/participant combos:")
    for _, row in counts.iterrows():
        print(f"  • bug={row['bug']}, participant={row['participant']} → {row['dup_count']} duplicate rows")

    # (Optional) Show the actual duplicated rows
    print("\nHere are the duplicated rows (first 10 shown):")
    print(dup_rows.sort_values(by=key_cols).head(10))

def cohen_d(x, y):
    """Cohen's d for effect size"""
    nx, ny = len(x), len(y)
    pooled_std = np.sqrt(((nx - 1) * np.std(x, ddof=1) ** 2 + (ny - 1) * np.std(y, ddof=1) ** 2) / (nx + ny - 2))
    return (np.mean(x) - np.mean(y)) / pooled_std

def rank_biserial(u_stat, n1, n2):
    """Rank biserial effect size from Mann-Whitney U"""
    return 1 - (2 * u_stat) / (n1 * n2)

def plot_for_fig8(metric, df_filtered, graph_filename, low_threshold=2, high_threshold=4): 
    # Make boxplot
    plt.figure(figsize=(2.75, 2.5))  # Adjust size as needed

    sns.boxplot(data=df_filtered, x=f'Accuracy_Group', y=metric, order=[f'Low (≤{low_threshold})', f'High (≥{high_threshold})'])
    #plt.title(f"{metric} Distribution by {split} Group")
    #plt.xlabel(f"{split} Group")
    plt.xlabel('')
    plt.ylabel('Mean Euclidean Dist.', fontweight='bold') # this is hardcoded 

    plt.tight_layout()
    plt.savefig(f"{graph_filename}_fig8.svg")
    plt.close()

def divide_by_accuracy(df, metrics, graph_filename, low_threshold=2, high_threshold=4, fig8=False, skip_fireflyp11=False): 
    if skip_fireflyp11:
        df = df[~((df['participant'] == 'p11') & (df['bug'] == 'firefly'))]
    # Create task identifier
    df['task'] = df['bug'].astype(str) + "_" + df['participant'].astype(str)

    # Filter for low and high accuracy
    df['Where_Accuracy'] = df['Where_Accuracy'].astype(float)
    low_df = df[df['Where_Accuracy'] <= low_threshold].copy()
    high_df = df[df['Where_Accuracy'] >= high_threshold].copy()

    # Store results
    results = []

    for metric in metrics:
        low_vals = np.abs(low_df[metric].dropna())
        high_vals = np.abs(high_df[metric].dropna())

        test_less = mannwhitneyu(low_vals, high_vals, alternative='less')
        stat_name_less = "Mann-Whitney U Less Side p-value"
        stat_value_less = test_less.pvalue

        test_greater = mannwhitneyu(low_vals, high_vals, alternative='greater')
        stat_name_greater = "Mann-Whitney U Greater Side p-value"
        stat_value_greater = test_greater.pvalue

        results.append({
            'metric': metric,
            'mean_low': np.mean(low_vals),
            'mean_high': np.mean(high_vals),
            'median_low': np.median(low_vals),
            'median_high': np.median(high_vals),
            'std_low': np.std(low_vals),
            'std_high': np.std(high_vals),
            f'{stat_name_less}': stat_value_less,
            f'{stat_name_greater}': stat_value_greater
        })

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)

    # Print summary
    #print(results_df.sort_values('p_value'))

    # --- Plotting ---
    # Melt for seaborn
    # Filter only rows that are low or high
    df_filtered = df[(df['Where_Accuracy'] <= low_threshold) | (df['Where_Accuracy'] >= high_threshold)].copy()

    # Label them
    df_filtered['Accuracy_Group'] = df_filtered['Where_Accuracy'].apply(
        lambda x: f'Low (≤{low_threshold})' if x <= low_threshold else f'High (≥{high_threshold})'
    )
    # Make boxplots
    plt.figure(figsize=(18, 10))
    print(f"length of metrics: {len(metrics)}")
    for i, metric in enumerate(metrics, 1):  # Plotting first 6 as an example
        plt.subplot(5, 6, i)
        sns.boxplot(data=df_filtered, x='Accuracy_Group', y=metric)
        plt.title(metric)
        plt.xlabel("")
        plt.tight_layout()

    plt.suptitle("Metric Distributions by Accuracy Group", fontsize=16, y=1.02)
    plt.savefig(f"{graph_filename}.svg")
    plt.close()

    print(metrics) 
    if fig8:
        plot_for_fig8('average_euclidean_distance', df_filtered, graph_filename, low_threshold=low_threshold, high_threshold=high_threshold)
    return results_df

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Get how many times each participant looked at correct bug location from pkl.")
    
    # Add arguments for input and output files
    parser.add_argument('input_file', type=str, help="Input file")
    parser.add_argument('duration_file', type=str, help="Duration file")
    parser.add_argument('correct_lines_file', type=str, help="Correct lines file")
    #parser.add_argument('--includes_md', action='store_true', help="Input file includes markdown files")
    parser.add_argument("--buffer", type=int, default=0, help="Buffer range around the correct line (default: 0)")
    parser.add_argument("--skip_timelines", action="store_true", help="Skip creating timelines")
    parser.add_argument("--skip_dwell", action="store_true", help="Skip getting dwell information")
    parser.add_argument("--low_threshold", type=int, default=2, help="Unsuccessful Accuracy Threshold (default: 2)")
    parser.add_argument("--high_threshold", type=int, default=4, help="Successful Accuracy Threshold (default: 4)")
    parser.add_argument("--skip_p11firefly", default=False, action="store_true", help="Don't include p11 firefly data")
    
    # TODO: add ability to specify previously computed .csv file?
    # TODO: --includes_md what was I intending to use this flag for? 

    args = parser.parse_args()
    input_stem = os.path.splitext(os.path.basename(args.input_file))[0]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"{timestamp}_get_answer_fixations_{input_stem}_outputs"
    os.mkdir(output_dir)
    output_stem = f"{output_dir}/{input_stem}"
    default_log = f"{output_stem}_get_answer_fixations.log" 
    print(f"Log: {default_log}")

    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(default_log),
                        logging.StreamHandler()
                    ])

   
    data = load_data(args.input_file)
    accuracy_duration_data = get_dicts_from_csv(args.duration_file, accuracy_data=True, skip_fireflyp11=args.skip_p11firefly)
    correct_lines_data = get_dicts_from_csv(args.correct_lines_file, args.skip_p11firefly)
    
    flines = parse_data(data, args.skip_p11firefly)
    if args.skip_timelines == False:
        for i in range(0,(args.buffer)+1): 
            create_summary(flines, output_dir, accuracy_duration_data, correct_lines_data, buffer=i)
    
    df = flatten_flines(flines, accuracy_duration_data)
    report_duplicates(df)
    if args.skip_p11firefly:
        df = df[~((df['participant'] == 'p11') & (df['bug'] == 'firefly'))]
        print(f"Removed p11 firefly data")
        print(df)
    df = add_next_fixation_same(df)
    if args.skip_dwell == False:
        df = add_dwell_counts(df)
        df = add_significant_dwells(df)
    else: 
        logging.info("Skipping dwell counts")
    df = add_next_file_different(df)
    metrics = ['line_distance_to_next', 
                'col_distance_to_next', 
                'euclidean_distance_to_next', 
                'x_diff_to_next_same_file', 
                'y_diff_to_next_same_file', 
                'x_diff_to_next', 
                'y_diff_to_next',
                'right_pupil_diameter',
                'left_pupil_diameter']
    if args.skip_dwell == False:
        metrics.extend(['same_line_fixations_next_30s', 'same_line_duration_next_30s']) 
    divided_df = divide_by_accuracy(df, metrics, f"{output_dir}/{input_stem}_divided_per_fixation_by_accuracy", low_threshold=args.low_threshold, high_threshold=args.high_threshold, fig8=False, skip_fireflyp11=args.skip_p11firefly)
    df.to_csv(f"{output_dir}/{input_stem}_next_fixation_similarity.csv", index=False)
    divided_df.to_csv(f"{output_dir}/{input_stem}_divided_per_fixation_by_accuracy.csv", index=False)


    count_and_percentage = get_count_and_percentage(df, accuracy_duration_data, not args.skip_dwell) # group data by task 
    metrics = [
        'average_line_distance',
        'average_col_distance',
        'average_euclidean_distance',
        'average_left_pupil_diameter',
        'average_right_pupil_diameter',
        'percentage_next_line_same',
        'percentage_next_token_same',
        'percentage_next_file_diff',
        'percentage_code_report_switch'
    ]
    direction_labels = df['direction_to_next_same_file'].dropna().unique()
    for direction in direction_labels:
        col_name = f'percentage_{direction}_same_file'
        metrics.append(col_name)
        col_name = f'percentage_{direction}'
        metrics.append(col_name)
    if args.skip_dwell == False:
        metrics.append('significant_dwells_normalized_by_total_fixations')
    
    # so first, we took the average or percentage for each task 
    # now, we take the average of those averages or percentages after sorting by accuracy 
    # a more appropriate suffix might be something like "average_of_task_averages_divided_by_accuracy"
    divided = divide_by_accuracy(count_and_percentage, metrics, f"{output_dir}/{input_stem}_divided_by_accuracy", low_threshold=args.low_threshold, high_threshold=args.high_threshold, fig8=True, skip_fireflyp11=args.skip_p11firefly)
    count_and_percentage.to_csv(f"{output_dir}/{input_stem}_next_fixation_similarity_percent.csv", index=False)
    divided.to_csv(f"{output_dir}/{input_stem}_divided_by_accuracy.csv", index=False)



if __name__ == "__main__":
    main()