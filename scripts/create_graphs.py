import subprocess
import argparse
import os 

def run_command(command): 
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:")
        print(e.stderr)

def find_methods_tally_file(directory: str, ending):
    for file in os.listdir(directory):
        print(f"Checking file: {file}")
        if file.endswith(ending):
            return os.path.join(directory, file)
    return ""

def run_graph_stats(directory: str):
    fdurations_command = [
        "python", "./graph_stats.py",
        f"{directory}\\fdurations_per_bug",
        "Mean Fixation Duration",
        "official_bug_names.csv",
        "--no_participant_label"
    ]
    fduration_means_command = [
        "python", "./graph_stats.py",
        f"{directory}\\fduration_means_per_bug",
        "Mean of Mean Fixation Durations per Participant",
         "official_bug_names.csv"
    ]
    fcount_command = [
        "python", "./graph_stats.py",
        f"{directory}\\fcount",
        "Mean Fixations",
        "official_bug_names.csv"
    ]
    flines_uniq = [
        "python", "./graph_stats.py",
        f"{directory}\\flines_uniq",
        "Mean Fixation Lines",
        "official_bug_names.csv"
    ]
    fregressionrate = [
        "python", "./graph_stats.py",
        f"{directory}\\fregressionrate",
        "Mean Regression Rate",
        "official_bug_names.csv"
    ]
    fmethods_uniq = [
        "python", "./graph_stats.py",
        f"{directory}\\fmethods_uniq",
        "Mean Fixation Methods",
        "official_bug_names.csv"
    ]

    methods_tally_file = find_methods_tally_file(directory, "fmethods_tally.csv")
    if not methods_tally_file:
        print("Error: No file ending with 'fmethods_tally.csv' found in the directory.")
    else: 
        topx_contain_ypercent_fixations_command = [
            "python", "./topx_contain_ypercent_fixations_log.py", 
            f"{methods_tally_file}",
            "official_bug_names.csv"
        ]
        print(f"{topx_contain_ypercent_fixations_command}")
        run_command(topx_contain_ypercent_fixations_command)

    lines_tally_file = find_methods_tally_file(directory, "flines_tally.csv")
    if not lines_tally_file:
        print("Error: No file ending with 'flines_tally.csv' found in the directory.")
    else: 
        topx_contain_ypercent_fixations_command = [
            "python", "./topx_contain_ypercent_fixations_log.py", 
            f"{lines_tally_file}",
            "official_bug_names.csv",
            "--unit", "Lines", 
            "--unit_max", "250"
        ]
        print(f"{topx_contain_ypercent_fixations_command}")
        run_command(topx_contain_ypercent_fixations_command)

    methods_uniq_file = find_methods_tally_file(directory, "fmethods_uniq.csv")
    if not methods_uniq_file:
        print("Error: No file ending with 'fmethods_uniq.csv' found in the directory.")
    else: 
        create_methods_command = [
            "python", "./create_specified_plot.py",
            methods_uniq_file,
            "official_bug_names.csv",
            "Bug",
            "Unique Fixation Method Count",
            "Participant ID",
            "--title", "Unique Number of Methods Visited Per Bug",
            "--ylabel", "Unique Number of Methods Visited"
        ]
        print(f"{create_methods_command}")
        run_command(create_methods_command)

    durations_by_score = [
        "python", "./create_duration_success_plots.py",
       "duration_from_notes.csv",
        "official_bug_names.csv"
    ]


    
    run_command(fdurations_command)
    run_command(fduration_means_command)
    run_command(fcount_command)
    run_command(flines_uniq)
    run_command(fregressionrate)
    run_command(fmethods_uniq)
    run_command(durations_by_score)
   

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run graph_stats.py with a specified directory.")
    parser.add_argument("directory", help="Directory containing fixation data")
    args = parser.parse_args()
    run_graph_stats(args.directory)
