import pickle
from statistics import mean, median
import argparse
import csv
import os 
import logging 
from datetime import datetime
import pandas as pd 
from collections import Counter
import statistics 
from scipy.stats import shapiro, mannwhitneyu, ttest_ind
import seaborn as sns
import numpy as np 
import matplotlib.pyplot as plt



def get_fixation_counts(bug, fcount, participant_id, session, data): 
    if bug not in fcount.keys(): 
        logging.warning(f"BUG {bug} NOT IN KEYS!")
        
    if participant_id in fcount[bug]: 
            logging.info(f"Found second database for participant {participant_id} and bug {bug}: {session}")
            fcount[bug][participant_id] += len(data[session])
    else: 
        logging.debug(f"adding data for bug {bug} and participant {participant_id}...")
        fcount[bug][participant_id] = len(data[session])
    return fcount 

def get_fixation_durations(bug, fduration, participant_id, session, data): 
    if bug not in fduration.keys(): 
        logging.warning(f"BUG {bug} NOT IN KEYS!")

    fixation_durations = [] 
    for fixation in data[session]: 
        if fixation["duration"] < 60000: # discard fixations longer than 1 minute 
            fixation_durations.append(fixation["duration"])

    logging.info(f"Participant {participant_id} during session {session} had {len(fixation_durations)} fixations with an average duration of {mean(fixation_durations)}")
    logging.info(f"Participant {participant_id} during session {session} had {len(fixation_durations)} fixations with an minimum duration of {min(fixation_durations)}")
    logging.info(f"Participant {participant_id} during session {session} had {len(fixation_durations)} fixations with an maximum duration of {max(fixation_durations)}")
    

    if participant_id in fduration[bug]: 
            logging.info(f"Found second database for participant {participant_id} and bug {bug}: {session}")
            fduration[bug][participant_id].extend(fixation_durations)
            logging.info(f"Now {participant_id} length of fduration[{bug}][{participant_id}] is {len(fduration[bug][participant_id])}")
    else: 
        fduration[bug][participant_id] = fixation_durations
    return fduration

def get_line_counts(bug, flines, participant_id, session, data): 
    if bug not in flines.keys(): 
        logging.warning(f"add_line_counts: BUG {bug} NOT IN KEYS!")

    fixation_lines = [] 
    for fixation in data[session]: 
        if fixation["duration"] < 60000: # discard fixations longer than 1 minute 
            fixation_lines.append(fixation['fixation_target']+str(fixation['source_file_line']))

    logging.info(f"add_line_counts: Participant {participant_id} during session {session} visited {len(fixation_lines)}, including {len(set(fixation_lines))} unique lines")
    

    if participant_id in flines[bug]: 
            logging.info(f"add_line_counts: Found second database for participant {participant_id} and bug {bug}: {session}")
            logging.info(f"add_line_counts: Previous length was {len(flines[bug][participant_id])}, current length: {len(fixation_lines)}")
            flines[bug][participant_id].extend(fixation_lines)
            logging.info(f"add_line_counts: Now {participant_id} length of flines[{bug}][{participant_id}] is {len(flines[bug][participant_id])}")
    else: 
        flines[bug][participant_id] = fixation_lines
    return flines

def get_words(bug, fwords, participant_id, session, data): 
    if bug not in fwords.keys(): 
        logging.warning(f"add_regressions: BUG {bug} NOT IN KEYS!")

    words = [] 
    for fixation in data[session]: 
        if fixation["duration"] < 60000 and fixation['token'] == None: 
            logging.warning(f"Token missing for bug {bug}, participant {participant_id}, session {session}, file: {fixation['fixation_target']}")
        if fixation["duration"] < 60000 and fixation['token'] != None: # discard fixations longer than 1 minute and fixations without a token 
            words.append(fixation['fixation_target']+str(fixation['source_file_line'])+fixation['token']) 

    logging.info(f"add_regressions: Participant {participant_id} during session {session} visited {len(words)}, including {len(set(words))} unique words")

    if participant_id in fwords[bug]: 
            logging.info(f"add_regressions: Found second database for participant {participant_id} and bug {bug}: {session}")
            logging.info(f"add_regressions: Previous length was {len(fwords[bug][participant_id])}, current length: {len(words)}")
            fwords[bug][participant_id].extend(words)
            logging.info(f"add_regressions: Now {participant_id} length of fwords[{bug}][{participant_id}] is {len(fwords[bug][participant_id])}")
    else: 
        fwords[bug][participant_id] = words
    return fwords

def get_methods(bug, fmethods, participant_id, session, data): 
    if bug not in fmethods.keys(): 
        logging.warning(f"get_methods: BUG {bug} NOT IN KEYS!")

    methods = [] 
    for fixation in data[session]: 
        if fixation["duration"] < 60000 and fixation['token'] == None: 
            logging.warning(f"Token missing for bug {bug}, participant {participant_id}, session {session}, file: {fixation['fixation_target']}")
        if fixation["duration"] < 60000 and fixation['token'] != None: # discard fixations longer than 1 minute and fixations without a token 
            astpath = fixation['xpath'].split("/")
            methodpos = ""
            for ast in astpath:
                if "src:function" in ast:
                    methodpos = ast
            
            if methodpos == "":
                continue			# not inside a function

            methods.append(fixation['fixation_target']+methodpos)  # file name + method location makes unique method string
        

    logging.info(f"get_methods: Participant {participant_id} during session {session} visited {len(methods)} methods, including {len(set(methods))} unique methods")

    if participant_id in fmethods[bug]: 
            logging.info(f"get_methods: Found second database for participant {participant_id} and bug {bug}: {session}")
            logging.info(f"get_methods: Previous length was {len(fmethods[bug][participant_id])}, current length: {len(methods)}")
            fmethods[bug][participant_id].extend(methods)
            logging.info(f"get_methods: Now {participant_id} length of fmethods[{bug}][{participant_id}] is {len(fmethods[bug][participant_id])}")
    else: 
        fmethods[bug][participant_id] = methods
    return fmethods

def get_agg_stats(fixation_agg, writer, islist=False): 
    for bug in fixation_agg:
            if len(fixation_agg[bug]) > 0: 
                if islist == True: 
                    num = len(fixation_agg[bug])
                    min_val = min(fixation_agg[bug])
                    max_val = max(fixation_agg[bug])
                    mean_val = mean(fixation_agg[bug])
                    median_val = median(fixation_agg[bug])
                else: 
                    num = len(fixation_agg[bug].values())
                    min_val = min(fixation_agg[bug].values())
                    max_val = max(fixation_agg[bug].values())
                    mean_val = mean(fixation_agg[bug].values())
                    median_val = median(fixation_agg[bug].values())
                
                # Write statistics for each bug
                writer.writerow([bug, num, min_val, max_val, mean_val, median_val])

def save_stats(output_filename, col_headers, fixation_agg=None, success_ps=None, fail_ps=None,  confident_ps=None, unsure_ps=None, islist=False): 
    # Save statistics to CSV (for min, max, mean, median)
    with open(output_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(col_headers)  # Write header row

        if fixation_agg != None:
            writer.writerow(["All Participants"])
            get_agg_stats(fixation_agg, writer, islist)
        if success_ps != None: 
            writer.writerow(["Successful Participants"])
            get_agg_stats(success_ps, writer, islist)
        if fail_ps != None:
            writer.writerow(["Failed Participants"])
            get_agg_stats(fail_ps, writer, islist)
        if confident_ps != None:
            writer.writerow(["Confident Participants"])
            get_agg_stats(confident_ps, writer, islist)
        if unsure_ps != None:
            writer.writerow(["Unsure Participants"])
            get_agg_stats(unsure_ps, writer, islist)
        
def get_success_or_fail(success, fail, accuracy_data, bug, participant_id, col): 
    for row in accuracy_data: 
        logging.debug(f"comparing {bug} to {row['Bug']} and {participant_id} to {row['Participant ID']}")
        if row["Bug"] == bug and row["Participant ID"] == participant_id: 
            try: 
                if float(row[col]) >= success: 
                    return True 
                elif float(row[col]) <= fail:
                    return False 
                else: 
                    logging.info(f"Participant {participant_id} for bug {bug} was neither successful nor failed at {col}")
                    return None
            except Exception as e: 
                logging.error(f"Could not convert {row[col]} to float for participant {participant_id} and bug {bug}")
                return None
    logging.error(f"Could not find accuracy data {col} for participant {participant_id} and bug {bug}")
    exit(1) 

def create_rq3_dicts(dat, success, fail, accuracy_data, bug, participant_id, fixation_agg, success_ps, fail_ps, confident_ps, unsure_ps): 
    # if p was successful, add data to success_ps 
    if get_success_or_fail(success, fail, accuracy_data, bug, participant_id, "Where_Accuracy") == True:
        success_ps[bug][participant_id] = dat

    # if p failed, add data to fail_ps 
    elif get_success_or_fail(success, fail, accuracy_data, bug, participant_id, "Where_Accuracy") == False:
        fail_ps[bug][participant_id] = dat

    # if p were confident, add to confident_ps
    if get_success_or_fail(success, fail, accuracy_data, bug, participant_id, "Where_Confidence") == True:
        confident_ps[bug][participant_id] = dat

    # if p were unsure, add to unsure_ps
    elif get_success_or_fail(success, fail, accuracy_data, bug, participant_id, "Where_Confidence") == False:
        unsure_ps[bug][participant_id] = dat
    return success_ps, fail_ps, confident_ps, unsure_ps

def save_per_bug(raw_output_filename, fixation_agg, col_headers, accuracy_data=None, success_ps=None, fail_ps=None, success=None, fail=None, confident_ps=None, unsure_ps=None, stat_type='count'): 
    logging.debug(f"types: {stat_type}")
    with open(raw_output_filename, mode='w', newline='') as raw_file:
        writer = csv.writer(raw_file)
        writer.writerow(col_headers)  # Write header row
        
        for bug in fixation_agg:
            if stat_type == 'count': 
                logging.debug(f"Stat type is count!")
                for participant_id, dat in fixation_agg[bug].items():
                    writer.writerow([bug, participant_id, dat])
                    success_ps, fail_ps, confident_ps, unsure_ps = create_rq3_dicts(dat, success, fail, accuracy_data, bug, participant_id, fixation_agg, success_ps, fail_ps, confident_ps, unsure_ps)
            elif stat_type == 'duration': 
                for participant_id, dat in fixation_agg[bug].items():
                    writer.writerow([bug, participant_id, mean(dat), min(dat), max(dat)])
            elif stat_type == 'lines': 
                logging.debug(f"Stat type is lines!")
                for participant_id in fixation_agg[bug]:
                    for dat in fixation_agg[bug][participant_id]: 
                        writer.writerow([bug, participant_id, dat[0], dat[1]])
    return success_ps, fail_ps, confident_ps, unsure_ps

def save_duration_stats(output_dir, input_stem, col_headers, bug_names, fduration, base="fduration", success=4, fail=2, accuracy_data=None, accuracy_dict=None): 
    durations_per_bug = {}
    success_durations_per_bug = {} 
    fail_durations_per_bug = {}
    confident_durations_per_bug = {} 
    unsure_durations_per_bug = {}

    duration_means_per_bug = {bug: {} for bug in bug_names}
    success_duration_means_per_bug = {bug: {} for bug in bug_names}
    fail_duration_means_per_bug = {bug: {} for bug in bug_names}
    confident_duration_means_per_bug = {bug: {} for bug in bug_names}
    unsure_duration_means_per_bug = {bug: {} for bug in bug_names}

    for bug in fduration: 
        all_bug_durations = [] 
        success_durations = []
        fail_durations = [] 
        confident_durations = []
        unsure_durations = []
        for participant in fduration[bug]: 
            # Put all durations for 1 bug in list (for all participants)
            all_bug_durations.extend(fduration[bug][participant])
            # Add durations to success/fail, confident/unsure lists 
             # if p was successful, add data to success_ps 
            if get_success_or_fail(success, fail, accuracy_data, bug, participant, "Where_Accuracy") == True:
                success_durations.extend(fduration[bug][participant])

            # if p failed, add data to fail_ps 
            elif get_success_or_fail(success, fail, accuracy_data, bug, participant, "Where_Accuracy") == False:
                fail_durations.extend(fduration[bug][participant])

            # if p were confident, add to confident_ps
            if get_success_or_fail(success, fail, accuracy_data, bug, participant, "Where_Confidence") == True:
                confident_durations.extend(fduration[bug][participant])

            # if p were unsure, add to unsure_ps
            elif get_success_or_fail(success, fail, accuracy_data, bug, participant, "Where_Confidence") == False:
                unsure_durations.extend(fduration[bug][participant])

            # Get mean of durations for each bug & participant combination
            duration_means_per_bug[bug][participant] = mean(fduration[bug][participant]) 
            # Now do that for success/fail, confident/unsure 
            success_duration_means_per_bug, fail_duration_means_per_bug, confident_duration_means_per_bug, unsure_duration_means_per_bug = create_rq3_dicts(mean(fduration[bug][participant]) , success, fail, accuracy_data, bug, participant, fduration, success_duration_means_per_bug, fail_duration_means_per_bug, confident_duration_means_per_bug, unsure_duration_means_per_bug)

        durations_per_bug[bug] = all_bug_durations
        success_durations_per_bug[bug] = success_durations
        fail_durations_per_bug[bug] = fail_durations
        confident_durations_per_bug[bug] = confident_durations
        unsure_durations_per_bug[bug] = unsure_durations

   
    col_headers = ['Bug', 'Participant ID', 'Mean Fixation Duration', 'Where_Accuracy', 'Where_Confidence']
    save_all_intermediates(output_dir, input_stem, col_headers, base="fduration_means_per_bug", all=duration_means_per_bug, success=success_duration_means_per_bug, fail=fail_duration_means_per_bug, confident=confident_duration_means_per_bug, unsure=unsure_duration_means_per_bug, accuracy_dict=accuracy_dict, islist=False)

    col_headers = ['Bug', 'Number of Fixations', 'Min Fixation Duration', 'Max Fixation Duration', 'Mean Fixation Duration', 'Median Fixation Duration']
    save_all_stats_variations(output_dir, input_stem, col_headers, base="fdurations_per_bug", all=durations_per_bug, success=success_durations_per_bug, fail=fail_durations_per_bug, confident=confident_durations_per_bug, unsure=unsure_durations_per_bug, accuracy_dict=accuracy_dict, islist=True)
 
    col_headers = ['Bug', 'Number of Participants', 'Min of Mean Fixation Durations per Participant', 'Max of Mean Fixation Durations per Participant', 'Mean of Mean Fixation Durations per Participant', 'Median of Mean Fixation Durations per Participant']
    save_all_stats_variations(output_dir, input_stem, col_headers, base="fduration_means_per_bug", all=duration_means_per_bug, success=success_duration_means_per_bug, fail=fail_duration_means_per_bug, confident=confident_duration_means_per_bug, unsure=unsure_duration_means_per_bug, accuracy_dict=accuracy_dict, islist=False)

def save_intermediate_step(output_dir, metric, segment, input_stem, col_headers, data, accuracy_dict=None, islist=False): 
    base_output_filename = f"{output_dir}/{segment}/{input_stem}_{metric}"
    os.makedirs(f"{output_dir}/{segment}", exist_ok=True)
    output_filename = f"{base_output_filename}_{segment}.csv"
    print(f"Saving {output_filename}...")
    with open(output_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(col_headers)  # Write header row
        if islist: 
            logging.error(f"data is a list: {data}")
        for bug in data:
            if len(data[bug]) > 0:
                for participant in data[bug]: 
                    if islist == True: 
                        pass
                        logging.error(f"Should not get here")
                    else: 
                        writer.writerow([bug, participant, data[bug][participant], accuracy_dict[bug][participant]["Where_Accuracy"], accuracy_dict[bug][participant]["Where_Confidence"]])
        # Extract all values
        all_values = [v for bug in data.values() for v in bug.values()]

        mean = statistics.mean(all_values)
        median = statistics.median(all_values)
        minimum = min(all_values)
        maximum = max(all_values)
        std_dev = statistics.stdev(all_values)
    
    # Add to overall stats 
    overall_filename = f"{output_dir}/{segment}/{input_stem}_{segment}.csv"
    headers = ['Metric', 'Segment', 'Mean', 'Median', 'Min', 'Max', 'Stddev'] 

    # Check if the file exists and has any content
    file_needs_header = not os.path.exists(overall_filename) or os.path.getsize(overall_filename) == 0

    with open(overall_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file_needs_header:
            writer.writerow(headers)
        writer.writerow([col_headers[2], segment, mean, median, minimum, maximum, std_dev])

def save_all_stats_variations(output_dir, input_stem, col_headers, base, all, success, fail, confident, unsure, accuracy_dict, islist=False): 
    output_stem = f"{output_dir}/{base}/{input_stem}_stats"
    os.mkdir(f"{output_dir}/{base}")
    base_output_filename = f"{output_stem}_{base}"
    save_stats(f"{base_output_filename}_all.csv", col_headers, fixation_agg=all, islist=islist)
    save_stats(f"{base_output_filename}_success.csv", col_headers, success_ps=success, islist=islist)
    save_stats(f"{base_output_filename}_fail.csv", col_headers, fail_ps=fail, islist=islist)
    save_stats(f"{base_output_filename}_confident.csv", col_headers, confident_ps=confident, islist=islist)
    save_stats(f"{base_output_filename}_unsure.csv", col_headers, unsure_ps=unsure, islist=islist)
    save_stats(f"{base_output_filename}.csv", col_headers, fixation_agg=all, success_ps=success, fail_ps=fail, confident_ps=confident, unsure_ps=unsure, islist=islist)

def flatten_data_to_df(data, accuracy_data, metric): 
    rows = []
    for bug, participants in data.items():
        for participant, value in participants.items():

            rows.append({'bug': bug, 'participant': participant, f'{metric}': value, 'Where_Accuracy': accuracy_data[bug][participant]["Where_Accuracy"], 'Where_Confidence': accuracy_data[bug][participant]["Where_Confidence"]})

    df = pd.DataFrame(rows)
    return df 

def cohen_d(x, y):
    """Cohen's d for effect size"""
    nx, ny = len(x), len(y)
    pooled_std = np.sqrt(((nx - 1) * np.std(x, ddof=1) ** 2 + (ny - 1) * np.std(y, ddof=1) ** 2) / (nx + ny - 2))
    return (np.mean(x) - np.mean(y)) / pooled_std

def rank_biserial(u_stat, n1, n2):
    """Rank biserial effect size from Mann-Whitney U"""
    return 1 - (2 * u_stat) / (n1 * n2)

def plot_metric_by_accuracy(df, metric, low_threshold=2, high_threshold=4, split='Where_Accuracy', graph_filename=None): 
    # --- Plotting ---
    # Melt for seaborn
    # Filter only rows that are low or high
    df_filtered = df[(df[split] <= low_threshold) | (df[split] >= high_threshold)].copy()

    # Label them
    df_filtered[f'{split}_Group'] = df_filtered[split].apply(
        lambda x: f'Low (≤{low_threshold})' if x <= low_threshold else f'High (≥{high_threshold})'
    )

    # Make boxplot
    plt.figure(figsize=(2.75, 2.5))  # Adjust size as needed

    sns.boxplot(data=df_filtered, x=f'{split}_Group', y=metric, order=[f'Low (≤{low_threshold})', f'High (≥{high_threshold})'])
    #plt.title(f"{metric} Distribution by {split} Group")
    #plt.xlabel(f"{split} Group")
    plt.xlabel('')
    # these are hardcoded labels, also, for fixation duration, we take the mean of the task, and then we take the mean of those means when we group by accuracy 
    label_mapping = {'fcount': 'Fixation Count', 'fduration_means_per_bug': 'Fixation Duration', 'flines_uniq': 'Unique Lines', 'fmethods_uniq': 'Unique Methods', 'fregressionrate': 'Regression Rate'}
    plt.ylabel(label_mapping[metric], fontweight='bold')

    plt.tight_layout()
    plt.savefig(graph_filename)
    plt.close()

def divide_by_accuracy(df, metric, split='Where_Accuracy', graph_filename=None, low_threshold=2, high_threshold=4): 
    # Create task identifier
    df['task'] = df['bug'].astype(str) + "_" + df['participant'].astype(str)

    # Try to convert split column to numeric and identify dropped rows
    converted_split = pd.to_numeric(df[split], errors='coerce')

    # Find the rows where conversion failed
    invalid_rows = df[converted_split.isna() & df[split].notna()]

    # Print the dropped rows (optional: adjust to show only specific columns)
    if not invalid_rows.empty:
        logging.warning(f"Dropped rows while calculating stat sig for {metric} and {split} due to invalid float conversion in column '{split}':")
        logging.warning(invalid_rows[[split, 'task']])  # or just print(invalid_rows) if you want everything

    # Replace the original column with the converted version and drop invalid
    df[split] = converted_split
    df = df.dropna(subset=[split])

    # Filter for low and high accuracy
    low_df = df[df[split] <= low_threshold].copy()
    high_df = df[df[split] >= high_threshold].copy()

    # Drop missing metric values
    low_vals = low_df[metric].dropna()
    high_vals = high_df[metric].dropna()

    test_less = mannwhitneyu(low_vals, high_vals, alternative='less')
    stat_name_less = "Mann-Whitney U Less Side p-value"
    stat_value_less = test_less.pvalue

    test_greater = mannwhitneyu(low_vals, high_vals, alternative='greater')
    stat_name_greater = "Mann-Whitney U Greater Side p-value"
    stat_value_greater = test_greater.pvalue

    results = {
        'metric': metric,
        'mean_low': np.mean(low_vals),
        'mean_high': np.mean(high_vals),
        'median_low': np.median(low_vals),
        'median_high': np.median(high_vals),
        'std_low': statistics.stdev(low_vals), # use statistics.stdev to be consistent, uses sample n-1 instead of n 
        'std_high': statistics.stdev(high_vals), # which is appropriate since we may be using a sample of the population if we drop ones that did not enter a confidence
        f'{stat_name_less}': stat_value_less,
        f'{stat_name_greater}': stat_value_greater
    }
    logging.info(f"metric: {metric}, split: {split}, Low threshold: {low_threshold}, high_threshold: {high_threshold}, Number of high vals: {len(high_vals)}, number of low values: {len(low_vals)}, mean: {results['mean_low']}, {results['mean_high']}")
    plot_metric_by_accuracy(df, metric, low_threshold, high_threshold, split=split, graph_filename=graph_filename) 
    return results

def get_stat_sig(data, accuracy_data, metric, output_dir, input_stem, split='Where_Accuracy', low_threshold=2, high_threshold=4):
    dir_name = f"{output_dir}/all/L{low_threshold}_H{high_threshold}_{split}"
    os.makedirs(dir_name, exist_ok=True)
    overall_filename = f"{dir_name}/{input_stem}_stat_sig_L{low_threshold}_H{high_threshold}.csv"
    graph_filename = f"{dir_name}/{input_stem}_{metric}_L{low_threshold}_H{high_threshold}.svg"
    df = flatten_data_to_df(data, accuracy_data, metric)
    results = divide_by_accuracy(df, metric, split=split, graph_filename=graph_filename, low_threshold=low_threshold, high_threshold=high_threshold)
    
    # Check if the file needs a header
    file_needs_header = not os.path.exists(overall_filename) or os.path.getsize(overall_filename) == 0

    # Write to the CSV
    with open(overall_filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results.keys())
        if file_needs_header:
            writer.writeheader()  # Write header only if file is new or empty
        writer.writerow(results)  # Write the actual data

def save_all_intermediates(output_dir, input_stem, col_headers, base, all, success, fail, confident, unsure, accuracy_dict, islist=False): 
    save_intermediate_step(output_dir, base, "all", input_stem, col_headers, all, accuracy_dict=accuracy_dict, islist=islist)
    save_intermediate_step(output_dir, base, "success", input_stem, col_headers, success, accuracy_dict=accuracy_dict, islist=islist)
    save_intermediate_step(output_dir, base, "fail", input_stem, col_headers, fail, accuracy_dict=accuracy_dict, islist=islist)
    save_intermediate_step(output_dir, base, "confident", input_stem, col_headers, confident, accuracy_dict=accuracy_dict, islist=islist)
    save_intermediate_step(output_dir, base, "unsure", input_stem, col_headers, unsure, accuracy_dict=accuracy_dict, islist=islist)
    get_stat_sig(all, accuracy_dict, base, output_dir, input_stem, split='Where_Accuracy', low_threshold=2, high_threshold=4)
    get_stat_sig(all, accuracy_dict, base, output_dir, input_stem, split='Where_Accuracy', low_threshold=1, high_threshold=5)

    get_stat_sig(all, accuracy_dict, base, output_dir, input_stem, split='Where_Confidence', low_threshold=2, high_threshold=4)
    get_stat_sig(all, accuracy_dict, base, output_dir, input_stem, split='Where_Confidence', low_threshold=1, high_threshold=5)
    
def get_accuracy_bug_participant_dict(accuracy_data, bug_names): 
    accuracy_bug_participant_dict = {bug: {} for bug in bug_names}
    for row in accuracy_data: 
        bug = row["Bug"]
        participant_id = row["Participant ID"]
        wa = row["Where_Accuracy"]
        wc = row["Where_Confidence"]
        accuracy_bug_participant_dict[bug][participant_id] = {
            "Where_Accuracy": wa,
            "Where_Confidence": wc
        }
    return accuracy_bug_participant_dict

def get_stats(input_filename, accuracy_file, output_dir, input_stem, skip_fireflyp11=False): 
    # NOTE: separate .c from .md. Doing this with extract_fixations 
    # NOTE: what percentage of fixations on .md vs .c? I am doing this a little manually instead 
    data = pickle.load(open(input_filename, "rb"))
    bug_names = ["ladybug", "stonefly", "hornet", "praying_mantis", "firefly", "silverfish", "spider", "weevil"]

    fcount = {bug: {} for bug in bug_names}
    fcount_success = {bug: {} for bug in bug_names}
    fcount_fail = {bug: {} for bug in bug_names}
    fcount_confident = {bug: {} for bug in bug_names}
    fcount_unsure = {bug: {} for bug in bug_names}


    fduration = {bug: {} for bug in bug_names}

    flines = {bug: {} for bug in bug_names}
    flines_uniq = {bug: {} for bug in bug_names}
    flines_uniq_success = {bug: {} for bug in bug_names}
    flines_uniq_fail = {bug: {} for bug in bug_names}
    flines_uniq_confident = {bug: {} for bug in bug_names}
    flines_uniq_unsure = {bug: {} for bug in bug_names}
    flines_tally = {bug: {} for bug in bug_names}

    fwords = {bug: {} for bug in bug_names}

    fregressions = {bug: {} for bug in bug_names}
    fregressions_success = {bug: {} for bug in bug_names}
    fregressions_fail = {bug: {} for bug in bug_names}
    fregressions_confident = {bug: {} for bug in bug_names}
    fregressions_unsure = {bug: {} for bug in bug_names}
    
    fwords_tally = {bug: {} for bug in bug_names}

    fmethods = {bug: {} for bug in bug_names}

    fmethods_uniq = {bug: {} for bug in bug_names}
    fmethods_uniq_success = {bug: {} for bug in bug_names}
    fmethods_uniq_fail = {bug: {} for bug in bug_names}
    fmethods_uniq_confident = {bug: {} for bug in bug_names}
    fmethods_uniq_unsure = {bug: {} for bug in bug_names}

    fmethods_tally = {bug: {} for bug in bug_names}

    # Get accuracy data
    with open(accuracy_file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        accuracy_data = list(reader)
    accuracy_dict = get_accuracy_bug_participant_dict(accuracy_data, bug_names)

    # NOTE: using these values for confidence too for now 
    success = 4 # 4 and 5 are success 
    # 3 is neither 
    fail = 2 # 1 and 2 are fail 

    
    for session in data:
        logging.info("\n")
        logging.info(f"session: {session}")
        try: 
            bug = data[session][0]["bug_name"]
            participant_id = data[session][0]["participant_id"]
            logging.info(f"bug name: {bug}")
            if skip_fireflyp11 and bug == "firefly" and participant_id == "p11":
                logging.info(f"Skipping firefly p11")
                continue

            logging.info("Getting count of fixations...")
            # add count of fixations 
            fcount = get_fixation_counts(bug, fcount, participant_id, session, data)

            # add fixation durations 
            logging.info("Getting fixation durations...")
            fduration = get_fixation_durations(bug, fduration, participant_id, session, data)

            # add count of unique lines visited and tally of each line visited 
            logging.info("Getting fixations lines...")
            flines = get_line_counts(bug, flines, participant_id, session, data)
           
            # get words visited and regression rates 
            logging.info("Getting fixation words...")
            fwords = get_words(bug, fwords, participant_id, session, data)

            # add count of methods visited and tally of each method visited 
            logging.info("Getting fixations methods...")
            fmethods = get_methods(bug, fmethods, participant_id, session, data)
            
        except Exception as e: 
            logging.error(f"Could not get data for session: {session} because: {e}")
        
    # Calculate number of unique lines and the count of each line 
    for bug in flines: 
        for participant_id in flines[bug]: 
            # Get number of unique lines 
            flines_uniq[bug][participant_id] = len(set(flines[bug][participant_id]))
            # Get count of each line 
            counts = Counter(flines[bug][participant_id])
            flines_tally[bug][participant_id] = list(counts.items())

    # Calculate regression rates and count of each word 
    for bug in fwords: 
        for participant_id in fwords[bug]: 
            words = fwords[bug][participant_id]
            # Calculate regression rate for words 
            swords = list(set(words))
            regression_rate = ((len(words)-len(swords))*100)/len(words)
            fregressions[bug][participant_id] = regression_rate
            # Get count of each word
            counts = Counter(fwords[bug][participant_id])
            fwords_tally[bug][participant_id] = list(counts.items())

    # Calculate number of methods and the count of each method
    for bug in fmethods: 
        for participant_id in fmethods[bug]: 
            # Get number of unique methods
            fmethods_uniq[bug][participant_id] = len(set(fmethods[bug][participant_id]))
            # Get count of each method
            counts = Counter(fmethods[bug][participant_id])
            fmethods_tally[bug][participant_id] = list(counts.items())

    
    # Make output directory
    output_stem = f"{output_dir}/{input_stem}"
    raw_output_filename =  f"{output_stem}_data" 

    # Save data per participant per bug 
    col_headers = ['Bug', 'Participant ID', 'Fixation Count']
    fcount_success, fcount_fail, fcount_confident, fcount_unsure = save_per_bug(f"{raw_output_filename}_fcount.csv", fcount, col_headers, accuracy_data, success_ps=fcount_success, fail_ps=fcount_fail, success=success, fail=fail, confident_ps=fcount_confident, unsure_ps=fcount_unsure)
    
    col_headers = ['Bug', 'Participant ID', 'Mean Fixation Duration', 'Min Fixation Duration', "Max Fixation Duration"]
    save_per_bug(f"{raw_output_filename}_fduration.csv", fduration, col_headers, stat_type='duration')
    
    col_headers = ['Bug', 'Participant ID', 'Fixation Line', 'Fixation Line Count']
    save_per_bug(f"{raw_output_filename}_flines_tally.csv", flines_tally, col_headers, stat_type='lines')
    
    
    col_headers = ['Bug', 'Participant ID', 'Unique Fixation Line Count']
    flines_uniq_success, flines_uniq_fail, flines_uniq_confident, flines_uniq_unsure = save_per_bug(f"{raw_output_filename}_flines_uniq.csv", flines_uniq, col_headers, accuracy_data, success_ps=flines_uniq_success, fail_ps=flines_uniq_fail, success=success, fail=fail, confident_ps=flines_uniq_confident, unsure_ps=flines_uniq_unsure)
    
    col_headers = ['Bug', 'Participant ID', 'Fixation Word', 'Fixation Word Count']
    save_per_bug(f"{raw_output_filename}_fwords_tally.csv", fwords_tally, col_headers, stat_type='lines')
    

    col_headers = ['Bug', 'Participant ID', 'Regression Rate']
    fregressions_success, fregressions_fail, fregressions_confident, fregressions_unsure = save_per_bug(f"{raw_output_filename}_fregressionrate.csv", fregressions, col_headers, accuracy_data, success_ps=fregressions_success, fail_ps=fregressions_fail, success=success, fail=fail, confident_ps=fregressions_confident, unsure_ps=fregressions_unsure)

    col_headers = ['Bug', 'Participant ID', 'Fixation Method', 'Fixation Method Count']
    save_per_bug(f"{raw_output_filename}_fmethods_tally.csv", fmethods_tally, col_headers, stat_type='lines')
    
    col_headers = ['Bug', 'Participant ID', 'Unique Fixation Method Count']
    fmethods_uniq_success, fmethods_uniq_fail, fmethods_uniq_confident, fmethods_uniq_unsure = save_per_bug(f"{raw_output_filename}_fmethods_uniq.csv", fmethods_uniq, col_headers, accuracy_data, success_ps=fmethods_uniq_success, fail_ps=fmethods_uniq_fail, success=success, fail=fail, confident_ps=fmethods_uniq_confident, unsure_ps=fmethods_uniq_unsure)
    
    # Save intermediate steps
    col_headers = ['Bug', 'Participant ID', 'Num Fixations', 'Where_Accuracy', 'Where_Confidence']
    save_all_intermediates(output_dir, input_stem, col_headers, base="fcount", all=fcount, success=fcount_success, fail=fcount_fail, confident=fcount_confident, unsure=fcount_unsure, accuracy_dict=accuracy_dict)
    
    col_headers = ['Bug', 'Participant ID', 'Num Uniq Lines Fixated On', 'Where_Accuracy', 'Where_Confidence']
    save_all_intermediates(output_dir, input_stem, col_headers, base="flines_uniq", all=flines_uniq, success=flines_uniq_success, fail=flines_uniq_fail, confident=flines_uniq_confident, unsure=flines_uniq_unsure, accuracy_dict=accuracy_dict)

    col_headers = ['Bug', 'Participant ID', 'Regression Rate', 'Where_Accuracy', 'Where_Confidence']
    save_all_intermediates(output_dir, input_stem, col_headers, base="fregressionrate", all=fregressions, success=fregressions_success, fail=fregressions_fail, confident=fregressions_confident, unsure=fregressions_unsure, accuracy_dict=accuracy_dict)

    col_headers = ['Bug', 'Participant ID', 'Num Uniq Methods Fixated On', 'Where_Accuracy', 'Where_Confidence']
    save_all_intermediates(output_dir, input_stem, col_headers, base="fmethods_uniq", all=fmethods_uniq, success=fmethods_uniq_success, fail=fmethods_uniq_fail, confident=fmethods_uniq_confident, unsure=fmethods_uniq_unsure, accuracy_dict=accuracy_dict)
    


    # Save averages and stats for each bug (average all participants together)
    col_headers = ['Bug', 'Number of Participants', 'Min Fixations', 'Max Fixations', 'Mean Fixations', 'Median Fixations']
    save_all_stats_variations(output_dir, input_stem, col_headers, base="fcount", all=fcount, success=fcount_success, fail=fcount_fail, confident=fcount_confident, unsure=fcount_unsure, accuracy_dict=accuracy_dict)

    save_duration_stats(output_dir, input_stem, col_headers, bug_names, fduration, base="fduration", accuracy_data=accuracy_data, accuracy_dict=accuracy_dict)

    col_headers = ['Bug', 'Number of Participants', 'Min Fixation Lines', 'Max Fixation Lines', 'Mean Fixation Lines', 'Median Fixation Lines']
    save_all_stats_variations(output_dir, input_stem, col_headers, base="flines_uniq", all=flines_uniq, success=flines_uniq_success, fail=flines_uniq_fail, confident=flines_uniq_confident, unsure=flines_uniq_unsure, accuracy_dict=accuracy_dict)

    col_headers = ['Bug', 'Number of Participants', 'Min Regression Rate', 'Max Regression Rate', 'Mean Regression Rate', 'Median Regression Rate']
    save_all_stats_variations(output_dir, input_stem, col_headers, base="fregressionrate", all=fregressions, success=fregressions_success, fail=fregressions_fail, confident=fregressions_confident, unsure=fregressions_unsure, accuracy_dict=accuracy_dict)

    col_headers = ['Bug', 'Number of Participants', 'Min Fixation Methods', 'Max Fixation Methods', 'Mean Fixation Methods', 'Median Fixation Methods']
    save_all_stats_variations(output_dir, input_stem, col_headers, base="fmethods_uniq", all=fmethods_uniq, success=fmethods_uniq_success, fail=fmethods_uniq_fail, confident=fmethods_uniq_confident, unsure=fmethods_uniq_unsure, accuracy_dict=accuracy_dict)
    

   
def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Get stats from pkl.")
    
    # Add arguments for input and output files
    parser.add_argument('input_file', type=str, help="Input file")
    parser.add_argument('accuracy_file', type=str, help="Success file")
    parser.add_argument("--skip_p11firefly", default=False, action="store_true", help="Don't include p11 firefly data")
    args = parser.parse_args()
    input_stem = os.path.splitext(os.path.basename(args.input_file))[0]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"{timestamp}_get_fixation_stats_{input_stem}_outputs"
    os.mkdir(output_dir)
    output_stem = f"{output_dir}/{input_stem}"
    default_log = f"{output_stem}_get_fixation_stats.log" 
    print(f"Log: {default_log}")

    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(default_log),
                        logging.StreamHandler()
                    ])

    get_stats(args.input_file, args.accuracy_file, output_dir, input_stem, args.skip_p11firefly)

if __name__ == "__main__":
    main()
