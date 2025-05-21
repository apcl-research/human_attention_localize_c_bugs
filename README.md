# Replication Repository and Online Appendix for "Human Attention During Localization of Memory Bugs in C Programs" 


# 1 README Contents: overview of sections of this file 
<!-- TOC --> 
- [Replication Repository and Online Appendix for "Human Attention During Localization of Memory Bugs in C Programs"](#replication-repository-and-online-appendix-for-human-attention-during-localization-of-memory-bugs-in-c-programs)
- [1 README Contents: overview of sections of this file](#1-readme-contents-overview-of-sections-of-this-file)
- [5 More Details on `analyze` branch and Scripts](#5-more-details-on-analyze-branch-and-scripts)
  - [5.1 `analyze` Branch Contents](#51-analyze-branch-contents)
  - [5.2 Script Details](#52-script-details)
  - [5.3 FAQ](#53-faq)

<!-- /TOC --> 
# 5 More Details on `analyze` branch and Scripts
## 5.1 `analyze` Branch Contents 
<details>
  <summary><strong>Expand Section</strong></summary>

- `figs` folder 
- `important_spreadsheets` folder 
- `old_scripts` folder 
- `only_eclipse_data` folder 
- `scripts` folder 
- `README.md`

### 5.1.1 `figs` 
- `angle_percentage_diagram.png`: diagram showing the ranking of directional fixation change (direction have to move eyes to get from one fixation to the next)
- `table11boxplots.pdf` and `table11boxplots.svg` Figure that goes with Table 11 in paper 
- `regression_euclidean.pdf` and `regression_euclidean` Figure 7 in paper 
- 
### 5.1.2 `important_spreadsheets`
- `20250413_162432_gazes_gaze_counts_per_region_percent.xlsx`: output from region script with AI percentages calculated manually 
- `20250413_165253_fixations_no_md_next_fixation_similarity_percent_2_4 (1).xls`
- `Appendix_Bug_and_Grading_Information.xlsx`: contains information about each bug (repository, issue number, commit numbers); contains task set for each participant; contains scores and grading
- `accuracy_scores.csv`: mapping from task to accuracy, confidence, difficulty scores 
- `accuracy_scores_nop11firefly.csv`: same as `accuracy_scores.csv`, but with `p11_firefly` task removed (see Section 4.3)
- `correct_lines.csv`: listing of which lines of code are considered correct for each bug 
- `correct_lines.xlsx`: excel version of csv 
- `duration_from_notes.csv`: how long each participant took to do each task according to Study Administrator's notes
- `duration_from_notes.xlsx`: excel version of csv 
- `duration_from_notes_nop11firefly.csv`: same as `duration_from_notes.xlsx`, but with `p11_firefly` task removed (see Section 4.3)
- `fixations_percent.csv`: manually created csv by taking fixations data from "code" and "all" versions and putting them on one sheet to compare 
- `official_bug_names.csv`: mapping from bug nickname like "ladybug" to official bug name from repository 
- `region_coordinates_per_participant.xlsx`: for each task, the Study Administrator watched the playback videos and used `get_xy.py` to determine how the participant divided their screen. Each task is 1+ rows, and for each task, there are multiple regions and the coordinates of those regions (top left and bottom right for each region)


### 5.1.3 `scripts` 
1. `convert_md_to_c_in_eclipse_xml.py`
2. `count_unique_per_accuracy.py`
3. `create_duration_success_plots.py`
4. `create_graphs.py`
5. `create_specified_plot.py`
6. `extractfixations.py`
7. `get_answer_fixations.py`
8. `get_fixation_stats_success_breakdown.py`
9. `get_region_times.py`
10. `get_xy.py`
11. `graph_stats.py`
12. `normal_check.py`
13. `pearson.py`
14. `rename_md_to_c.py`
15. `topx_contain_ypercent_fixations.py`
16. `topx_contain_ypercent_fixations_log.py`
17. `unpickle.py`
18. `unpickle_all.py`
</details>

## 5.2 Script Details 
<details>
  <summary><strong>Expand Section</strong></summary>

### 5.2.1 `convert_md_to_c_in_eclipse_xml.py`
<details>
  <summary><strong>Expand Section</strong></summary>

#### Purpose 
When generating the srcml of the bug and instruction directories, I rename all the .md instruction files to have a .c extension 
so they could be processed by srcml which doesn't support .md. 
With this script, we are changing every instance in `itrace_eclipse*.xml` of a file that ends in .md to have the extension .c and c filetype. 
This way, the `StudyInstructions.c` that is in the in the .xml created by srcml of the instructions directory 
corresponds to the `StudyInstructions.c` in `itrace_eclipse*.xml`. 
#### Usage 
```
usage: convert_md_to_c_in_eclipse_xml.py [-h] input_path

Recursively process files in a directory.

positional arguments:
  input_path  File or directory to process.

options:
  -h, --help  show this help message and exit
```
#### Example 
```
python .\convert_md_to_c_in_eclipse_xml.py .\only_eclipse_data
```
#### Outputs 
The .xml files get modified in place, so now if you open the `itrace_eclipse*.xml` files, you will see the file names replaced. 
#### Outputs Used For 
These `itrace_eclipse*.xml` files are used by the iTrace toolkit when creating the .db3 databases. 
</details>

### 5.2.2 `count_unique_per_accuracy.py`
<details>
  <summary><strong>Expand Section</strong></summary>

#### Purpose 
create charts and csvs showing for each accuracy score, how many unique bugs and unique participants got that score 
#### Usage
```
usage: count_unique_per_accuracy.py [-h] [--output_dir OUTPUT_DIR] csv_path

Analyze Where_Accuracy by Bug and Participant.

positional arguments:
  csv_path              Path to the input CSV file

options:
  -h, --help            show this help message and exit
  --output_dir OUTPUT_DIR
                        Directory to save plots and data
```
#### Example 
```
python .\count_unique_per_accuracy.py .\accuracy_scores.csv --output_dir accuracy_counts
```
#### Outputs 
- `bug_accuracy_counts.csv`: where accuracy scores across the top, bugs down the side. numbers are telling you how many participants completed each bug with the specified score. For example, 1 person completed the firefly bug with a score of 0. 
- `bug_accuracy_line_plot.png`: line plot of `bug_accuracy_counts.csv` 
- `bug_histograms_subplot.png`: histograms of `bug_accuracy_counts.csv` 
- `participant_accuracy_counts.csv`: where accuracy scores across the top, participants down the side. numbers are telling you how many tasks each participant completed with each accuracy score. For example, participant 1 completed 3 bugs with a score of 1 and 1 bug with a score of 2, and so on. 
- `participant_accuracy_line_plot.png`: line plot of `participant_accuracy_counts.csv` 
- `participant_histograms_subplot.png`: histogram of `participant_accuracy_counts.csv` 
- `participant_stacked_bar.png`: shows how many tasks got each accuracy score. For example, there were 13 tasks that got a score of 2. The colors show you which participant did each task. Note: we round half values down. So, we rounded 3.5 down to 3 and 4.5 down to 4. However, we rounded a score of 0 up to 1. This reflects how we calculated all the other metrics. For the other metrics, the tasks with a "low" score where the threshold is 1 include all scores less than or equal to 1 including a score of 0. For the other metrics when the threshold is greater than or equal to 4, we include 4.5 but not 3.5. 
- `where_accuracy_summary.csv`: for each accuracy score, tells you how many unique bugs and participants got that score. For example, there were 4 unique participants who achieved a score of 1 on a task: p1, p3, p4, and p6. 
#### Outputs Used For 
This is Figure 8 in the paper. 
</details>

### 5.2.3 `create_duration_success_plots.py` 
<details>
  <summary><strong>Expand Section</strong></summary>

#### Purpose 
Create plots showing how long successful vs unsuccessful participants took to complete each bug. 
#### Usage
```
usage: create_duration_success_plots.py [-h] csv_file official_bug_names_csv

Scatter and box plots of bug duration with coloring based on confidence scores.

positional arguments:
  csv_file              Path to the CSV file
  official_bug_names_csv
                        Path to the CSV file containing official bug names mapping.

options:
  -h, --help            show this help message and exit
```
#### Example 
```
 python .\create_duration_success_plots.py .\duration_from_notes.csv .\official_bug_names.csv
```
#### Outputs 
- `Where_Accuracy_{timestamp}.png`: scatter plot showing how long it took each participant to do each bug.  The dots are color-coded by whether or not the participant had a "low" accuracy score (red) or a "high" accuracy score (green). Tasks where the score was neither "low" nor "high" were excluded. 
- `Where_Confidence_{timestamp}.png`: scatter plot showing how long it took each participant to do each bug.  The dots are color-coded by whether or not the participant had a "low" confidence score (red) or a "high" confidence score (green). Tasks where the score was neither "low" nor "high" were excluded. 
- `BoxPlot_By_Bug_Where_Accuracy_{timestamp}.png`: Group tasks by accuracy score into "low" and "high" groups for each bug. Some tasks were neither high nor low (score of 3), so they are excluded. Then, plot a boxplot for each group for each bug. 
- `BoxPlot_By_Bug_Where_Confidence_{timestamp}.png`: Group tasks by confidence score into "low" and "high" groups for each bug. Some tasks were neither high nor low (score of 3), so they are excluded. Then, plot a boxplot for each group for each bug.
#### Outputs Used For
Not using these right now 
NOTE: called by `create_graphs.py` 
</details>

### 5.2.4 `create_graphs.py`
<details>
  <summary><strong>Expand Section</strong></summary>

#### Purpose 
script to run other scripts. Specifically, it runs `graph_stats.py`, `create_specified_plot.py`, `topx_methods_contain_ypercent_fixations.py`, and `create_duration_success_plots.py` 
#### Usage
```
usage: create_graphs.py [-h] directory

Run graph_stats.py with a specified directory.

positional arguments:
  directory   Directory containing fixation data

options:
  -h, --help  show this help message and exit
```
#### Example 
```
python ./create_graphs.py 20250421_145430_get_fixation_stats_20250413_162432_fixations_outputs
```
#### Outputs 
- outputs from `graph_stats.py` for `fdurations_per_bug` 
- outputs from `graph_stats.py` for `fduration_means_per_bug` 
- outputs from `graph_stats.py` for `fcount`
- outputs from `graph_stats.py` for `flines_uniq`  
- outputs from `graph_stats.py` for `fregressionrate` 
- outputs from `graph_stats.py` for `fmethods_uniq`  
- outputs from `topx_contain_ypercent_fixations` for `fmethods_tally.csv` 
- outputs from `topx_contain_ypercent_fixations` for `flines_tally.csv` 
- outputs from `create_specified_plot.py` for `fmethods_uniq.csv` 
- outputs from `create_duration_success_plots.py` 

#### Outputs Used For
Figures 3-4 and Tables 8-9
</details>

###  5.2.5 `create_specified_plot.py`
<details>
  <summary><strong>Expand Section</strong></summary>

#### Purpose 
Create plots of how many unique methods each participant looked at. This can also be used to make other scatter/box plots. For example, we use it to create the scatter plot showing the percent of fixations that were on code. 
#### Usage
```
usage: create_specified_plot.py [-h] [--title TITLE] [--xlabel XLABEL] [--ylabel YLABEL] [--dir DIR]
                                csv_file official_bug_names_csv x_col y_col label_col

Plot data from a CSV file.

positional arguments:
  csv_file              Path to the CSV file
  official_bug_names_csv
                        Path to the CSV file containing official bug names mapping.
  x_col                 Column name for x-axis
  y_col                 Column name for y-axis
  label_col             Column name for data point labels

options:
  -h, --help            show this help message and exit
  --title TITLE         Title for the plot
  --xlabel XLABEL       Label for the x-axis
  --ylabel YLABEL       Label for the y-axis
  --dir DIR             Directory name
```
#### Example 
```
python ./create_specified_plot.py 20250413_165755_get_fixation_stats_20250413_162432_fixations_outputs/20250413_162432_fixations_data_fmethods_uniq.csv official_bug_names.csv "Bug" "Unique Fixation Method Count" "Participant ID" --title "Unique Number of Methods Visited Per Bug" --ylabel "Unique_Number of Methods Visited" 
```

```
 python .\create_specified_plot.py .\code_percent_demo\20250413_162432_fixations_data_fcount_md_vs_no_md.csv .\official_bug_names.csv "Bug" "Percent Code Fixations" "Participant ID" --title "Percent Fixations on Code" --xlabel "Bug" --ylabel "Percent Fixations on Code" --dir percent_code
```
#### Outputs 
- outputs a .png and a .svg version of a scatter plot and a box plot to a new folder called `uniq_methods` (or the directory name specified) that is created in the directory where the input csv_file is. The name of the .png and .svg are either based on the title from the command line arguments, or it is `Unique_Number_of_Methods_Visted_Per_Bug_*` 
- what the graph shows is really dependent on the data and the command line arguments, but when this script is called from `create_graphs.py`, the box plot shows the average number of unique methods/functions looked at for each bug. The average is over all the participants who completed the specified bug. When this script is called from `create_graphs.py`, the scatter plot shows how many unique methods/functions each participant looked at for each bug. The dots are color coded so that each participant is a different color, but the same color across all of the tasks they completed. 
#### Outputs Used For
NOTE: called by `create_graphs.py`. Used to create Figure 5 in paper.  
</details>

### 5.2.6 `extractfixations.py` 
<details>
  <summary><strong>Expand Section</strong></summary>
  
#### Purpose 
Take databases and turn them into .pkl. Basically, take all databases and extract the information we want from them and put all this information in the same data structure. 
Then, we pickle the data structure and save it as a .pkl file. 
#### Usage
```
usage: extractfixations.py [-h] [--no-gazes [NO_GAZES]] [--no-md [NO_MD]] [--no-verify [NO_VERIFY]] directory

Extract fixations and gazes from database files.

positional arguments:
  directory             Directory to search for .db3 files

options:
  -h, --help            show this help message and exit
  --no-gazes [NO_GAZES]
                        Don't extract gazes (default: False)
  --no-md [NO_MD]       Remove fixations on markdown files .md (default: False)
  --no-verify [NO_VERIFY]
                        Don't verify db time order
```
#### Example 
```
python ./extractfixations.py databases\ 
```
#### Outputs 
- `{timestamp}_fixations.pkl`: Pickled data structure containing all fixation information for all participants and all tasks. 
- OPTIONAL: `{timestamp}_gazes.pkl`: Pickled data structure containing all gazes information for all participants and all tasks. 
- OPTIONAL: `{timestamp}_fixations_no_md.pkl`: Pickled data structure containing fixations that are on files that don't end in the markdown file extension `md`. We want to exclude these files so that we are mostly getting fixations that are on `.c` files. We generalize this to mean that these fixations are only on code, not on the bug reports or the instructions. 
- `{timestamp}_extract_fixations.log`: Logging file for this script, contains information about what the script did and if it encountered any errors or warnings. 
#### Outputs Used For
The .pkl files from this script are processed by many of the other scripts including `get_fixation_stats_success_breakdown.py`, `get_answer_fixations.py`, `get_region_times.py`, etc. 
</details>

### 5.2.7 `get_answer_fixations.py`
<details>
  <summary><strong>Expand Section</strong></summary>
  
#### Purpose 
This script processes the fixation data and the gaze data together to learn about fixations over time. 
For example this script creates timelines of fixations, highlighting which fixations were on the bug locations (answers to task). 
This script also computes metrics like the percentage of time that participant looked at the same line twice in a row, etc. 
#### Usage
```
usage: get_answer_fixations.py [-h] [--includes_md] [--buffer BUFFER] [--skip_timelines] [--skip_dwell] [--low_threshold LOW_THRESHOLD] [--high_threshold HIGH_THRESHOLD]
                               input_file duration_file correct_lines_file

Get how many times each participant looked at correct bug location from pkl.

positional arguments:
  input_file            Input file
  duration_file         Duration file
  correct_lines_file    Correct lines file

options:
  -h, --help            show this help message and exit
  --buffer BUFFER       Buffer range around the correct line (default: 0)
  --skip_timelines      Skip creating timelines
  --skip_dwell          Skip getting dwell information
  --low_threshold LOW_THRESHOLD
                        Unsuccessful Accuracy Threshold (default: 2)
  --high_threshold HIGH_THRESHOLD
                        Successful Accuracy Threshold (default: 4)
```
The threshold values are inclusive. So the threshold of 2 is all scores less than and equal to 2. 
The buffer allows you to be more flexible with what you consider a "correct fixation" or a fixation on a line that contains the answer to the task. 
When the buffer is set to 0, only the exact line is considered correct. However, if you increase the buffer to 1, then one line above and one line below 
the correct line will also be considered correct. 
#### Example 
```
python .\get_answer_fixations.py 20250413_165253_fixations_no_md.pkl .\duration_from_notes.csv .\correct_lines.csv --low_threshold 1 --high_threshold 5
```
#### Outputs 
- Creates a directory called `{timestamp}_get_answer_fixations_{name_of_pkl_file}`
- Inside this directory, there are directories called `buffer{B}` where B is the number that the buffer was set to 
- Inside the buffer directories, there are directories for each bug and a file called `summary_buffer{B}.csv`. This file lists each task and how many fixations on correct lines there were. 
- Inside each bug directory, there is one timeline for each participant who completed the bug. The timelines show fixations over time. The y axis is the duration of the fixation. Fixations on correct lines are highlighted in a non-grey color. 
- Besides the buffer directories, there are a series of .csvs and .svgs. 
- `{name_of_pkl_file}_divided_by_accuracy.csv`: shows average line distance, percentage of fixations where the next fixation is on the same line, etc. For these numbers, we group by task, calculate the metric, and then average over the metrics for the tasks for the tasks with low accuracy and the tasks with high accuracy. 
- `{name_of_pkl_file}_divided_by_accuracy.svg`: subplots of data from `{name_of_pkl_file}_divided_by_accuracy.csv`
- `{name_of_pkl_file}_divided_per_fixation_by_accuracy.csv`: shows line distance, euclidean distance, right_pupil_diameter, etc. These metrics are calculated without grouping by task first. They are the averages over all the fixations where the fixation is in a task with a low or high accuracy.  
- `{name_of_pkl_file}_divided_per_fixation_by_accuracy.svg`: subplots of data from `{name_of_pkl_file}_divided_per_fixation_by_accuracy.csv` 
- `{name_of_pkl_file}_get_answer_fixations.log`: log file from running `get_answer_fixations.py` 
- `{name_of_pkl_file}_next_fixation_similarity.csv`: "raw" data this script uses to generate the averages/plots 
- `{name_of_pkl_file}_next_fixation_similarity_percent.csv`: averages and counts for each participant. These are the averages that are averaged together for `{name_of_pkl_file}_divided_by_accuracy.csv`

#### Outputs Used For
Used to get euclidean distance for figure 7 and table 11. 
</details>

### 5.2.8 `get_fixation_stats_success_breakdown.py` 
<details>
  <summary><strong>Expand Section</strong></summary>
  
#### Purpose 
I would say this is the "meat" of the data analysis. Get "Table 2" data. Fixation count, fixation duration, Lines looked at, functions looked at, etc and put info into .csvs 
#### Usage
```
usage: get_fixation_stats_success_breakdown.py [-h] input_file accuracy_file

Get stats from pkl.

positional arguments:
  input_file     Input file
  accuracy_file  Success file

options:
  -h, --help     show this help message and exit
```
#### Example 
```
python .\get_fixation_stats_success_breakdown.py 20250413_165253_fixations_no_md.pkl .\accuracy_scores.csv
```
#### Outputs 
- `all` directory: contains metrics for all tasks (not divided by accuracy or confidence)
  - `L1_H5_Where_Accuracy` directory: contains metrics and plots for tasks divided by `Where_Accuracy` where the low threshold is <= 1 and the high threshold is >= 5. Measures differences between low and high groups. 
  - `L1_H5_Where_Confidence` directory: contains metrics and plots for tasks divided by `Where_Confiderce` where the low threshold is <= 1 and the high threshold is >= 5. Measures differences between low and high groups. 
  - `L2_H4_Where_Accuracy` directory: contains metrics and plots for tasks divided by `Where_Accuracy` where the low threshold is <= 2 and the high threshold is >= 4. Measures differences between low and high groups. 
  - `L2_H4_Where_Confidence` directory: contains metrics and plots for tasks divided by `Where_Confidence` where the low threshold is <= 2 and the high threshold is >= 4. Measures differences between low and high groups. 
  - `{name_of_pkl_file}_all.csv`: summary of 5 metrics: number of fixations, number of unique lines fixated on, regression rate, number of unique methods fixated on, mean fixation duration. There are mean, medians, mins, maxs, and stddevs for each metric calculated across all tasks. Ex: number of fixations for p10_ladybug + number of fixations for p2_stonefly + ... / total number of tasks = mean number of fixations 
  - `{name_of_pkl_file}_fcount_all.csv`: number of fixations per task 
  - `{name_of_pkl_file}_fduration_means_per_bug_all.csv`: mean fixation duration per task 
  - `{name_of_pkl_file}_flines_uniq_all.csv`: number of unique lines looked at per task 
  - `{name_of_pkl_file}_fmethods_uniq_all.csv`: number of unique methods/functions looked at per task 
  - `{name_of_pkl_file}_fregressionrate_all.csv`: regression rate per task 
- `confident`/ `unsure` directories: contain .csvs showing the same 5 metrics from the `all` directory, but instead we only have the tasks where the participant either rated their confidence as >= 4 (confident) or <=2 (unsure)
- `success`/ `fail` directories: : contain .csvs showing the same 5 metrics from the `all` directory, but instead we only have the tasks where the where accuracy is either >= 4 (success) or <=2 (fail)
- `fcount` directory 
  - `{name_of_pkl_file}_stats_fcount.csv`: summary of following 5 .csvs, shows number of tasks, min number of fixations, max number of fixations, mean number of fixations, and median number of fixations for each bug for each group (all, successful, failed, confident, unsure) 
  - `{name_of_pkl_file}_stats_fcount_all.csv`: shows number of tasks, min number of fixations, max number of fixations, mean number of fixations, and median number of fixations for all tasks grouped by bug 
  - `{name_of_pkl_file}_stats_fcount_confident.csv`: shows number of tasks, min number of fixations, max number of fixations, mean number of fixations, and median number of fixations for tasks where the participant rated their confidence >= 4 grouped by bug 
  - `{name_of_pkl_file}_stats_fcount_fail.csv`: shows number of tasks, min number of fixations, max number of fixations, mean number of fixations, and median number of fixations for tasks where the accuracy score is <= 2 grouped by bug 
  - `{name_of_pkl_file}_stats_fcount_success.csv`: shows number of tasks, min number of fixations, max number of fixations, mean number of fixations, and median number of fixations for tasks where the accuracy score is >= 4 grouped by bug 
  - `{name_of_pkl_file}_stats_fcount_unsure.csv`: shows number of tasks, min number of fixations, max number of fixations, mean number of fixations, and median number of fixations for tasks where the participant rated their confidence <= 2 grouped by bug
- `fduration_means_per_bug` directory: same as `fcount` directory, but instead of number of fixations, it is the mean duration of the fixations for each task grouped by bug 
- `fdurations_per_bug` directory: same as `fcount` directory, but instead of number of fixations, it is the mean duration of the fixations grouped byg bug 
- `flines_uniq` directory: same as `fcount` directory, but instead of number of fixations, it is the number of unique lines the participant looked at 
-`fmethods_uniq` directory: same as `fcount` directory, but instead of number of fixations, it is number of unique methods/functions the participant looked at 
-`fregressionrate` directory: same as `fcount` directory, but instead of number of fixations, it is the regression rate 
- `{name_of_pkl_file}_data_fcount.csv`: shows the number of fixations per task (no means, medians, etc)
- `{name_of_pkl_file}_data_fduration.csv`: shows the average fixation duration per task 
- `{name_of_pkl_file}_data_flines_tally.csv`: shows the unique lines looked at in each task and the count of how many times the participant looked at each line 
- `{name_of_pkl_file}_data_flines_uniq.csv`: shows the number of unique lines looked at during each task 
- `{name_of_pkl_file}_data_fmethods_tally.csv`: shows the unique methods/functions looked at during each task and the count of how many times the participant looked at each function/method 
- `{name_of_pkl_file}_data_fregressionrate.csv`: shows the regression rate for each task    
- `{name_of_pkl_file}_data_fwords_tally.csv`: shows the unique tokens/words looked at during each task and how many times the participant for the task looked at each token/word 
- `{name_of_pkl_file}_get_fixation_stats.log`: logging file for this script 
 
#### Outputs Used For
The outputs of this script are used as the input for `graph_stats.py` and other scripts. 
Used to get Table 6 and Table 10 data. 
</details>

### 5.2.9 `get_region_times.py`
<details>
  <summary><strong>Expand Section</strong></summary>
   
#### Purpose 
Get how much time was spent in each "region" of eclipse IDE (file explorer, code, report, iTrace, AI)
#### Usage
```
usage: get_region_times.py [-h] input_file region_xys_file

Get region from gaze pkl.

positional arguments:
  input_file       Gaze pkl file
  region_xys_file  xlsx containing regions and x,y coordinates for each session

options:
  -h, --help       show this help message and exit
```
#### Example 
```
python .\get_region_times.py 20250413_165253_gazes.pkl important_spreadsheets\region_coordinates_per_participant.xlsx
```
#### Outputs 
- `timestamp_gazes_duration.csv`: duration of each task with start and ending timestamps 
- `timestamp_gazes_gaze_counts_per_region.csv`: number of gazes per region per task
- `timestamp_gazes_get_region_times.log`: logging file for script 
#### Outputs Used For
Percent Gazes AI Window in Table 10 
</details>

### 5.2.10 `get_xy.py`
<details>
  <summary><strong>Expand Section</strong></summary>
  
#### Purpose 
Print and save the x,y coordinate of wherever you click with your mouse. Only starts recording mouse clicks after hit any key on keyboard. Used this to get x and y coordinates for screen regions. 
#### Usage
```
usage: get_xy.py [-h] output

Record mouse clicks and save to a CSV file.

positional arguments:
  output      Name of the output CSV file

options:
  -h, --help  show this help message and exit
```
#### Example 
```
python .\get_xy.py p11_clicks.csv 
```
#### Outputs 
Saves mouse clicks to output file specified. Also prints click locations to terminal. 
#### Outputs Used For
Used this to get x and y coordinates for screen regions. 
</details>

### 5.2.11 `graph_stats.py`
<details>
  <summary><strong>Expand Section</strong></summary>
  
#### Purpose 
Create bar charts showing how different groups (success/fail, confident/unsure) compare to each other along a metric. 
#### Usage
```
usage: graph_stats.py [-h] [--no_participant_label] folder y_column official_bug_names_csv

Plot grouped bar charts from specific CSV files with participant labels.

positional arguments:
  folder                Folder containing the CSV files
  y_column              Column name to be used for the y-axis
  official_bug_names_csv
                        Path to the CSV file containing official bug names mapping.

options:
  -h, --help            show this help message and exit
  --no_participant_label
                        Don't put number of participants on top of bars
```
#### Example 
Need to run `get_fixation_stats*` script first so that you have the directory needed in the arguments. 
```
python .\graph_stats.py \path\to\dir\fdurations_per_bug "Mean Fixation Duration" official_bug_names.csv --no_participant_label
```
#### Outputs 
Outputs 3 plots: 
1. ["all", "success", "fail", "confident", "unsure"],
2. ["success", "fail"],
3. ["confident", "unsure"]
#### Outputs Used For
This script is called by `create_graphs.py`
These graphs are not being used in the paper. 
</details>

### 5.2.12 `normal_check.py` 
<details>
  <summary><strong>Expand Section</strong></summary>
  
#### Purpose 
Check if a dataset is normally distributed. 
#### Usage
```
usage: normal_check.py [-h] [--plot] csv_path column_name

Check if a column in a CSV is normally distributed.

positional arguments:
  csv_path     Path to the CSV file
  column_name  Name of the column to check for normality

options:
  -h, --help   show this help message and exit
  --plot       Show histogram and Q-Q plot
```
#### Example 
Need to run `get_fixation_stats*` script first so that you have the .csv file path to specify. 
```
 python .\normal_check.py .\20250514_101411_get_fixation_stats_20250413_165253_fixations_no_md_outputs\20250413_165253_fixations_no_md_data_fcount.csv "Fixation Count"
```
#### Outputs 
Outputs whether or not the data in the column specified has a normal distribution. Also tells you the skewness and kurtosis of the data. 
#### Outputs Used For
General statistics 
</details>

### 5.2.13 `pearson.py` 
<details>
  <summary><strong>Expand Section</strong></summary>
  
#### Purpose 
Calculates the pearson correlation coefficient between columns in .csv file. 

#### Usage
```
usage: pearson.py [-h] [--alpha ALPHA] csv_path

Compute Pearson correlation matrix from a CSV file.

positional arguments:
  csv_path       Path to the CSV file.

options:
  -h, --help     show this help message and exit
  --alpha ALPHA  Significance level for hypothesis testing (default: 0.05).
```
#### Example 
```
python .\pearson.py important_spreadsheets\accuracy_scores.csv 
```
Note that this script currently only works for the format of the `accuracy_scores.csv` file in this repository. 
In the future, I will make this more generalizable. 
#### Outputs 
3 matrices: 
1. pearson correlation coefficient matrix 
2. p-value matrix 
3. significant correlations matrix 

#### Outputs Used For
Table 4 in paper 
</details>

### 5.2.14 `rename_md_to_c.py`
<details>
  <summary><strong>Expand Section</strong></summary>
  
#### Purpose 
Rename all .md files in a directory to .c. 
This was necessary because srcML does not create srcML for markdown files. 
So, I converted them to .c files to create the srcML for them. 
#### Usage
```
usage: rename_md_to_c.py [-h] directory

Rename all .md files in a directory to .c files.

positional arguments:
  directory   Directory to process

options:
  -h, --help  show this help message and exit
```
#### Example 
```
python .\rename_md_to_c.py \path\to\study\instructions\folder 
```
#### Outputs 
Changes the extension of the files in place. So, I normally do this on a copy or on a separate branch. 
#### Outputs Used For
After renaming, then I use srcML to create the .xml of the study instructions and source code. 
Then, that srcML is the input to the iTrace Toolkit. 
</details>

### 5.2.15 `topx_contain_ypercent_fixations.py`
<details>
  <summary><strong>Expand Section</strong></summary>
  
There is also a `log` version of this script where the y axis of the figures is a log scale. 
#### Purpose 
Create graphs showing how many functions or lines contain the top x percent fixations. 
#### Usage
```
usage: topx_contain_ypercent_fixations.py [-h] [--percentage PERCENTAGE] [--unit UNIT] [--unit_max UNIT_MAX]
                                          csv_file official_bug_names_csv

Process fixation data from a CSV file.

positional arguments:
  csv_file              Path to the CSV file containing fixation data.
  official_bug_names_csv
                        Path to the CSV file containing official bug names mapping.

options:
  -h, --help            show this help message and exit
  --percentage PERCENTAGE
                        Percentage of fixations to consider (default: 75).
  --unit UNIT           What type of data to graph. Options: Functions, Lines
  --unit_max UNIT_MAX   Maximum number of units to display in the plot (default: 25).
```
#### Example 
```
python .\topx_contain_ypercent_fixations.py \path\to\20250413_165253_fixations_no_md_data_flines_tally.csv .\official_bug_names.csv  --unit "Lines" --unit_max 250
```
#### Outputs 
-`aggregate_data.csv`: Data per task   
-`aggregate_data_stats.csv`: Task data aggregated per bug   
-svgs, pngs, pdfs - There is one per bug, but 3 versions (svg, png, pdf)
#### Outputs Used For
Tables 7 and 8, Figures 3 and 4. 
</details>

### 5.2.16 `topx_contain_ypercent_fixations_log.py`
<details>
  <summary><strong>Expand Section</strong></summary>
  
#### Purpose 
This is the same as `topx_contain_ypercent_fixations.py`, but the graphs use a log scale on the y axis. 
</details>

### 5.2.17 `unpickle.py`
<details>
  <summary><strong>Expand Section</strong></summary>
  
#### Purpose 
Unpickle .pkl to .csv 
#### Usage
```
usage: unpickle.py [-h] input_file output_file

Unpickle a file and output its contents to a CSV file.

positional arguments:
  input_file   Input pickle file
  output_file  Output CSV file

options:
  -h, --help   show this help message and exit
```
#### Example 
```
python .\unpickle.py fixations.pkl fixations.csv 
```
#### Outputs 
.csv containing all data in .pkl 
</details>

### 5.2.18 `unpickle_all.py`
<details>
  <summary><strong>Expand Section</strong></summary>
  
#### Purpose 
Unpickle all .pkls in a directory to .csvs 
#### Usage
```
usage: unpickle_all.py [-h] input_directory pattern output_directory

Unpickle all files in a directory that match a pattern and output their contents to CSV files.

positional arguments:
  input_directory   Directory containing input pickle files
  pattern           Pattern filter for input files
  output_directory  Directory to save output CSV files

options:
  -h, --help        show this help message and exit
```
#### Example 
```
python .\unpickle_all.py databases databases_unpickled 
```
#### Outputs 
.csv files containing data from .pkl files 
</details>
</details>

## 5.3 FAQ 
<details>
  <summary><strong>Expand Section</strong></summary>

### What is the difference between `fduration_means_per_bug` and `fdurations_per_bug`? 
 - fduration_means_per_bug: take the average fixation duration for each task, then take the average of the tasks for each bug. For example, if 4 participants did bug ladybug, we would have 4 averages for ladybug, and then we take the average of those 4 averages to get the average for ladybug. 
  - fdurations_per_bug: concatenate all the fixation durations for each participant that does each bug, and then take the average of those durations for each bug. For example, if there are 4 participants who did ladybug, there might be 100 durations for each participant, so 400 durations total. We take the average over all 400 durations to get the mean duration for ladybug. 
</details>