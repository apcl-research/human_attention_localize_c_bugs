# Replication Repository and Online Appendix for "Human Attention During Localization of Memory Bugs in C Programs" 


# 1 README Contents: overview of sections of this file 
<!-- TOC --> 
- [Replication Repository and Online Appendix for "Human Attention During Localization of Memory Bugs in C Programs"](#replication-repository-and-online-appendix-for-human-attention-during-localization-of-memory-bugs-in-c-programs)
- [1 README Contents: overview of sections of this file](#1-readme-contents-overview-of-sections-of-this-file)
- [2 Repository Organization: description of contents of each branch](#2-repository-organization-description-of-contents-of-each-branch)
- [3 Replication Procedure for Study: description of how to replicate the data analysis](#3-replication-procedure-for-study-description-of-how-to-replicate-the-data-analysis)
  - [3.1 Software Setup](#31-software-setup)
  - [3.2 Setup for Session](#32-setup-for-session)
  - [3.3 Session with Participant](#33-session-with-participant)
  - [3.4 After Participant Leaves](#34-after-participant-leaves)
- [4 Replication Procedure for Data Analysis](#4-replication-procedure-for-data-analysis)
  - [4.1 Data Processing Steps](#41-data-processing-steps)
  - [4.2 Analysis Steps](#42-analysis-steps)
  - [4.3 Table/Figures Recap](#43-tablefigures-recap)
- [5 More Details on `analyze` branch and Scripts](#5-more-details-on-analyze-branch-and-scripts)
  - [5.1 `analyze` Branch Contents](#51-analyze-branch-contents)
  - [5.2 Script Details](#52-script-details)
  - [5.3 FAQ](#53-faq)
- [6 More Details on `instructions` branch](#6-more-details-on-instructions-branch)
  - [6.1 `StudyInstructions`](#61-studyinstructions)
  - [6.2 Scripts](#62-scripts)

<!-- /TOC --> 

# 2 Repository Organization: description of contents of each branch 
<details>
  <summary><strong>Expand Section</strong></summary>

This repository is organized into branches: 
- `main`: contains the raw itrace_core and itrace_eclipse .xml files 
- `instructions`: a template branch that contains the template consent form, pre-study questionnaire, post-study questionnaire, and bug reports. The branch was copied from to create the participant branches. 
- `analyze`: contains the data analysis scripts and intermediate versions of data 
</details>

# 3 Replication Procedure for Study: description of how to replicate the data analysis
## 3.1 Software Setup  
<details>
  <summary><strong>Expand Section</strong></summary>

  1. We use the Tobii Pro Fusion Eye Tracker 120 Hz: https://www.tobii.com/products/eye-trackers/screen-based/tobii-pro-fusion and Tobii Eye Tracker Manager 2.6.1: https://connect.tobii.com/s/etm-downloads?language=en_US 
  2. Download Eclipse IDE for C/C++ Developers (2024-09) Version 4.33.0: https://www.eclipse.org/downloads/packages/release/2024-09/r/eclipse-ide-cc-developers 
  3. Download iTrace tools: 
  https://www.i-trace.org/main/pages/downloads.html 
  - Core - v0.2.0 
  - Plugin - v0.2.0 
  - Toolkit - v0.2.2
  4. Add the iTrace plugin to Eclipse following the instructions on the iTrace wiki: https://github.com/iTrace-Dev/iTrace-Core/wiki/Getting-Started-with-iTrace-Core 
  5. Install the Remain AI Chat Plugin for Eclipse: https://marketplace.eclipse.org/content/remain-ai-chat-chatgpt#details 
  6. Clone this repository 
  7. Switch to the `instructions` branch 
  8. Run the `get_repos.py` script to download the buggy versions of source code for each bug 
</details>

## 3.2 Setup for Session 
<details>
  <summary><strong>Expand Section</strong></summary>

1. Attach Tobii Eye Tracker to computer 
2. Create Display Setup for Tobii Eye Tracker in Tobii Eye Tracker Manager 
3. Make a copy of the `instructions` branch 
4. Modify the `StudyInstructions/StudyProcedure.md` file if you want to change which bugs the participant will solve during the session. The default is `ladybug`, `stonefly`, `hornet`, `silverfish`, `praying_mantis`, and `spider` 
5. Open Eclipse, and use File > Open Projects from File System to open the Study Instructions folder and the folder containing each bug's source code. 
6. Rename the folders in Eclipse containing each bug's source code to the bug's code name (e.g. `ladybug`)
7. Make sure you see the iTrace Eclipse Plugin in Eclipse. Window > Show View > Other > search for iTrace > select iTrace plugin, and it should open in Eclipse 
8. Open iTrace core; minimize command prompt that opens 
9. In Eclipse, in the iTrace plugin window, click "Connect to Core" 
10. Create folders to save iTrace data. It is important to create a new folder for each task because the mouse click data from iTrace saves to the same file name every time. 
</details>

## 3.3 Session with Participant 
<details>
  <summary><strong>Expand Section</strong></summary>

1. Thank participant for participating in our study. 
2. Introductions 
3. Sit participant down at computer 
4. Have participant read through the consent form and sign name 
5. Conduct pre-study questionnaire 
6. Walk participant through calibrating in Tobii Eye Tracker Manager 
7. Walk participant through calibrating, starting, stopping in iTrace-core 
8. Participant ready to read `StudyInstructions.md` now 
9. Answer any questions that the participant has. 
10. Start script to do pop ups called `prompt.py` with 
```
python .\prompt.py --interval 5.0 --csv {participant_name}.csv
```
11. Participant opens `StudyProcedure.md` and starts  
12. Repeat steps 13-17 until time is up

13. In the Session Setup tab of iTrace-core, fill in Task Name, Researcher Name, and Participant ID in the iTrace-core window. Choose a Data Directory.In the iTrace Tracking tab, select Tobii Pro Fusion as the tracker, check the boxes for "Record with DejaVu" and "Enable Screen Recording",  calibrate, and then start iTrace-core.  
14. Start 30 minute timer for bug 
15. Participant opens bug report and works on bug 
16. After 30 minutes, ask participant to move on to next bug if not done.
17. When participant is done with this bug, stop iTrace-core. In the Data Directory, you should see 4 files: `itrace_core-*`, `itrace_eclipse-*`, `out.csv`, and `screen_rec-*` 

18. When participant finishes bug that is closest to the 2 hour mark, tell them that they are done. 
19. Stop `prompt.py` script which has been running the whole time 
20. Conduct post-study questionnaire
21. Pay participant 
</details>

## 3.4 After Participant Leaves 
<details>
  <summary><strong>Expand Section</strong></summary>

1. Label and backup files created by iTrace (Data Directories)
2. Save Remain AI Chat window history using save button in Eclipse 
3. Upload .xml files, AI Chat window history, and popup .csv to GitHub 
4. Upload screen recordings to Google Drive (too big for GitHub)
</details>

# 4 Replication Procedure for Data Analysis 
Switch to the `analyze` branch 
## 4.1 Data Processing Steps 
<details>
  <summary><strong>Expand Section</strong></summary>

### 4.1.1 Eye Tracking Data 
#### Note: Skip steps 1-2 if using study's original data which is included in this repository, `analyze` branch, `only_eclipse_data` folder. Note, you many need to unzip some large files.  
1. Reorganize data to make sure there are no nested folders (iTrace-Toolkit does not handle nested folder structures well). You will see that the folder organization of `only_eclipse_data` in the `analyze` branch has been modified from `main`'s version to accommodate this. 
2. Convert all relevant references to .md files to references to .c files in the iTrace/eclipse .xml files. Use `convert_md_to_c_in_eclipse_xml.py` 
#### Note: This is the state that the files in `only_eclipse_data` in the `analyze` branch are in 
#### Note: You may skip steps 3-4 if you would like to use our generated srcML files located at this Google Drive Link: https://drive.google.com/drive/folders/1Y4HQGYNrKKFCap6LzHGmnmCDMB3xlQEa?usp=drive_link 
3. Convert all .md files in the directory containing the code for the bug and in the study instructions directory to .c files. we do this because srcml cannot create .xmls for .md files. To do this, use the `rename_md_to_c.py` script 
4. Generate the srcml for the directory containing the code for the bug and the instructions directory. (must install srcml on machine first) 
Command: 
```
srcml --verbose --archive --position path\to\bug\directory path\to\instructions\directory -o {bug_name}_{participant_id}.xml
```

#### Note: You may skip step 5 if you would like to use our generated databases located at this Google Drive Links: https://drive.google.com/drive/folders/1_D4LoZXNVAaxDzO2TuDV_Dc0lOmk_dOm?usp=drive_link
5. For each bug subfolder for each participant, use iTrace-Toolkit to generate database (.db3 files; you should have at least one per task). Note: We excluded folders that contained data for just a few seconds of tracking. These files are from cases where the eye tracker was started/stopped very quickly during configuration. 
    - create new database 
    - import folder containing .xml eclipse data 
    - you can only import one folder at a time, and the folders cannot be nested. 
    - map tokens: choose .xml created in step 4 
    - you may need to individually create .xmls for files that are not found in the first round of mapping tokens 
    - generate fixations. set fixation settings to Fixation Filter = IVT, Velocity Threshold = 50, Duration (milliseconds) 80. (these are the default values for IVT)

#### Note: You may skip step 6 if you would like to use our generated .pkl files located at this Google Drive Link: https://drive.google.com/drive/folders/1eTnnvSOuRE0g94TNWKcHzAgez_4G1xa9?usp=drive_link 
6. Run `extractfixations.py` to generate the .pkl files. Note: there is extra logic in this script to remove data from participant 8's firefly task because the eye tracker was not stopped at the end of the task. 
7. You can run `unpickle.py` to get a .csv version of a .pkl file

### 4.1.2 Region Coordinates Data 
1. Refer to `important_spreadsheets\region_coordinates_per_participant.xlsx` on this branch to see the format the data needs to be in for interfacing with the analysis scripts. This spreadsheet was created manually by the study administrator. Each task gets a row, and then there are columns for each region and the x,y coordinates of the top-left and bottom-right corners of each region. 
2. For each task, repeat the following: 
- Watch the screen recording and take note of any time the screen configuration changes. 
- For each time the screen configuration changes, do the following: 
  - Start the `get_xy.py` script 
  - Open the screen recording for the task and make it full screen on the computer used to complete the task 
  - Click any key on the keyboard to trigger the script to log x,y coordinates 
  - Click on the top-left and bottom-right corners of each region 
#### Our screen recordings are located in the folders for each task here: https://drive.google.com/drive/folders/1XD6sTp58JqH-pPvnUD8yfo3JKRSm-rya?usp=drive_link 

### 4.1.3 AI Chat Data (Table 10 Queries)
1. If you are conducting your own study, you will have the `.json` files saved from the Remain AI Chat Window in Eclipse for each participant 
2. For our study, please refer to this file in Google Drive: https://docs.google.com/spreadsheets/d/1HsdA5WA44Ezjk6fC90fZqoEeKMscgR-MtqGbvv1KHUs/edit?usp=drive_link. Note that for some participants, we successfully saved the `.json` file while for others, the number of AI queries is confirmed by region coordinate data, watching the screen recordings, and the study administrator's notes. 

### 4.1.4 Popup Data (Table 6)
There is a .csv file for each participant documenting when the attention survey popped up and what the participant's response was. This .csv file for each participant is included in each participant's branch on this repository. The aggregated data is here: https://docs.google.com/spreadsheets/d/1giubGglxVcxWsRzYHPYchLtC9wkwCA8O/edit?usp=drive_link&ouid=100587885798417241681&rtpof=true&sd=true. 

### 4.1.5 Bug Repository Data (Table 1)
Please see the `important_spreadsheets\Appendix_Bug_and_Grading_Information.xlsx` in this branch. 
</details>

## 4.2 Analysis Steps 
<details>
  <summary><strong>Expand Section</strong></summary>
  
1. Run `get_fixation_stats_success_breakdown.py` to get the basic metrics like fixation count, number of unique lines, etc. (Table 7)
2. Run `create_graphs.py`. You need to run `get_fixation_stats_success_breakdown.py` first thought because the directories that are the outputs of `get_fixation_stats_success_breakdown.py` are the inputs to `create_graphs.py`. (Table 8, Table 9, Figure 3, Figure 4)
3. Run `get_region_times.py` to get the data used to calculate the percentages for Table 10. The percentages are calculated manually from the output. See our spreadsheet here: important_spreadsheets/20250413_162432_gazes_gaze_counts_per_region_percent.xlsx 
4. Create the `fixations_percent.csv` file (pre-work for Figure 5)
- copy the `{timestamp}_fixations_data_fcount.csv` file from the `{timestamp}_get_fixation_stats_{timestamp}_fixations_outputs` directory to a new directory. I called this directory `code_percent` 
- copy the `{timestamp}_fixations_no_md_data_fcount.csv` from the `{timestamp}_get_fixation_stats_{timestamp}_fixations_no_md_outputs` directory to the same directory `code_percent` 
- make a copy of the `{timestamp}_fixations_data_fcount.csv` file in the `code_percent` directory and rename it `{timestamp}_fixations_data_fcount_md_vs_no_md.csv` 
- copy column C from `{timestamp}_fixations_no_md_data_fcount.csv` to column D of `{timestamp}_fixations_data_fcount_md_vs_no_md.csv` 
- in column E of `{timestamp}_fixations_data_fcount_md_vs_no_md.csv`, enter the formula for `column C - column D`
- in column F of `{timestamp}_fixations_data_fcount_md_vs_no_md.csv`, enter the formula for `1 - column E` 
5. Run `create_specified_plot.py` with the `fixations_percent.csv` to generate the plot for percent fixations on code per bug (Figure 5 in paper)
6. Run `count_unique_per_accuracy.py` to generate Figure 8 (stacked bar chart) and all the histograms in Figure 2. 
7. Run `get_answer_fixations.py` to get the data about when participants looked at the correct buggy line. These outputs are used for Figure 6, Figure 7, Table 11, the box plots for Table 11, Figure 9, Figure 10, Figure 11, and Figure 12. 
8. To create Figure 7 and Table 11, the data outputted from `get_fixation_stats_success_breakdown.py` and `get_answer_fixations.py` were combined into 1 spreadsheet: `20250413_165253_fixations_no_md_next_fixation_similarity_percent_2_4 (1).xlsx` and XLSTAT was used for the statistical tests. See the spreadsheet for more details. You can also find these numbers in the outputs from `get_fixation_stats_success_breakdown.py` and `get_answer_fixations.py`. 
9. The box plots that go with Table 11 are in the outputs from `get_fixation_stats_success_breakdown.py` and `get_answer_fixations.py`. 
10. Run `pearson.py` to get the numbers for Table 4. 
11. The numbers for Table 5 come from the `important_spreadsheets\Appendix_Bug_and_Grading_Information.xlsx` in this branch. 
</details>

## 4.3 Table/Figures Recap 
<details>
  <summary><strong>Expand Section</strong></summary>

- `p11_firefly`: The participant did not complete this task within 30 minutes, so they don't have scores for confidence/difficulty and received a score of 0 for accuracy. This task is not included when comparing successful and failure tasks. However, the eye tracking data from this task is included in the big-picture eye tracking metrics. 
- `p11_ladybug`: The eye tracker was not started successfully at the beginning of this task, so we do not have eye tracking data for this task. However, we do have accuracy/difficulty/confidence scores, so those are included, but because there is no eye tracking data, it is not possible to include it in the eye tracking metrics. 
### 4.3.1 Tables 
- Table 1: see `important_spreadsheets\Appendix_Bug_and_Grading_Information.xlsx`
- Table 2: see `important_spreadsheets\Appendix_Bug_and_Grading_Information.xlsx`
- Table 3: see `important_spreadsheets\Appendix_Bug_and_Grading_Information.xlsx`
- Table 4: `pearson.py` and accuracy data (includes p11_ladybug and p11_firefly)
- Table 5: 
  - program information and scores comes from `important_spreadsheets\Appendix_Bug_and_Grading_Information.xlsx`
  - time comes from `important_spreadsheets/duration_from_notes_seconds.csv` (includes p11_firefly, but not p11_ladybug)
- Table 6: You can see the options in `prompt.py` in the `instructions` branch, and the Percentages are calculated on this spreadsheet: important_spreadsheets/20250413_162432_gazes_gaze_counts_per_region_percent.xlsx which is an aggregation of the .csvs from each participant (located on each participant's branch)
- Table 7: `get_fixation_stats_success_breakdown.py` outputs (metrics run on code-only/no_md version of data, includes p11_firefly, but not p11_ladybug)
- Table 8-9: `create_graphs.py` runs `topx_contain_ypercent_fixations_log.py` which generates this data (metrics run on code-only/no_md version of data, includes p11_firefly, but not p11_ladybug)
- Table 10: AI Queries can be see here: https://docs.google.com/spreadsheets/d/1HsdA5WA44Ezjk6fC90fZqoEeKMscgR-MtqGbvv1KHUs/edit?usp=drive_link, and percentages calculated on this sheet important_spreadsheets/20250413_162432_gazes_gaze_counts_per_region_percent.xlsx which is outputted from `get_region_times.py` (includes p11_ladybug and p11_firefly)
- Table 11: Data can be seen on `important_spreadsheets/20250413_165253_fixations_no_md_next_fixation_similarity_percent_2_4 (1).xls`, and that data comes from `get_fixation_stats_success_breakdown.py` and `get_answer_fixations.py` where you can also see the Table 11 numbers in the outputs. (metrics run on code-only/no_md version of data, does not include p11_firefly or p11_ladybug)

### 4.3.2 Figures 
- Figure 1: This is a screenshot of the interface taken by the study administrator 
- Figure 2: Output from `count_unique_per_accuracy.py` (includes p11_ladybug and p11_firefly)
- Figure 3-4: `create_graphs.py` runs `topx_contain_ypercent_fixations_log.py` which generates these graphs (only code, no_md, includes p11_firefly, but not p11_ladybug)
- Figure 5: `create_specified_plot.py` with the `fixations_percent.csv` (includes p11_firefly, but not p11_ladybug)
- Figure 6: `get_answer_fixations.py` (includes p11_firefly, but not p11_ladybug)
- Figure 7: See `important_spreadsheets/20250413_165253_fixations_no_md_next_fixation_similarity_percent_2_4 (1).xls`. The file in the paper is a .pdf version of this chart. 
- Figure 8: `count_unique_per_accuracy.py` (includes p11_ladybug and p11_firefly)
- Figures 9-12: `get_answer_fixations.py` (includes p11_firefly, only code)
</details>

# 5 More Details on `analyze` branch and Scripts
<details>
  <summary><strong>Expand Section</strong></summary>

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
</details>

# 6 More Details on `instructions` branch
<details>
  <summary><strong>Expand Section</strong></summary>

## 6.1 `StudyInstructions` 
- `StudyInstructions.md`: instructions for study participant to read before starting to localize bugs 
- `StudyProcedure.md`: procedure participant follows and where they write their answers 
- `consent_form.md`: consent form 
- `{bug_name}.md`: bug reports for each bug 
- `post_study.md`: post-study questionnaire
- `pre-study.md`: pre-study questionnaire 

## 6.2 Scripts 
<details>
  <summary><strong>Expand Section</strong></summary>

### 6.2.1 `get_repos.py` 
<details>
  <summary><strong>Expand Section</strong></summary>

#### Purpose 
Download open source C repositories used for study to commit that contains the bug. 

#### Usage 
```
usage: get_repos.py [-h] directory

Check for existing folders.

positional arguments:
  directory   The directory to check for existing repos

options:
  -h, --help  show this help message and exit
```
</details>

### 6.2.2 `prompt.py` 
<details>
  <summary><strong>Expand Section</strong></summary>

#### Purpose 
Creates a pop-up window every X minutes that asks the user about their attentional state. 
Saves the answers to a .csv. 

#### Usage 
```
usage: prompt.py [-h] [--interval INTERVAL] [--csv CSV]

Prompt user responses at intervals and save to a CSV file.

options:
  -h, --help           show this help message and exit
  --interval INTERVAL  Time interval in minutes between prompts (can be a fraction)
  --csv CSV            CSV file name to save responses
```
</details>
</details>
</details>