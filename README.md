# Replication Repository and Online Appendix for "Human Attention During Localization of Memory Bugs in C Programs" 

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