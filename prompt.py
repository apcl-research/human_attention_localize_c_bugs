import tkinter as tk
from datetime import datetime, timedelta
import csv
import argparse
import time
from tkinter import messagebox

# Set up argument parser for command-line options
parser = argparse.ArgumentParser(description="Prompt user responses at intervals and save to a CSV file.")
parser.add_argument("--interval", type=float, default=5.0, help="Time interval in minutes between prompts (can be a fraction)")
parser.add_argument("--csv", type=str, default="responses.csv", help="CSV file name to save responses")
args = parser.parse_args()

# Retrieve command-line arguments
time_interval = args.interval * 60  # Convert interval from minutes to seconds
start_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
print(f"Start Time: {start_time}")
csv_file = f"{str(start_time)}_{args.csv}"

# List of open-ended questions to display
questions = [
]

# Define the multiple-choice questions and options
mc_questions = [
    ("In the few seconds before this screen appeared, what were you thinking about?", ["I was focused on the task.", "I was thinking about my performance on the task or how long it is taking.", "I was thinking about things unrelated to the task (e.g., daydreaming)", "I was distracted by sights or sounds in my environment.", "My mind was blank."])
]

responses = []  # List to store responses with timestamps
grouping_number = 1  # Initialize grouping number for responses

# Initialize the CSV file with headers
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Grouping Number", "Prompt Timestamp", "Submit Timestamp", "Question", "Response"])

def show_prompt():
    global grouping_number  # Declare as global to modify it
    # Capture the timestamp when the prompt appears
    prompt_timestamp = datetime.now()

    # Create a new window for each prompt
    window = tk.Tk()
    window.title("Type your responses")
    
    # Set window size (width x height)
    window.geometry("1000x800")
    window.minsize(800,600)

    # Make the window always on top
    window.attributes("-topmost", True)
    
    # Disable window close button (X)
    window.protocol("WM_DELETE_WINDOW", lambda: None)
    
    # Create a dictionary to hold Text widgets for each open-ended question
    text_widgets = {}

    # Display each open-ended question with an associated Text widget
    for i, question in enumerate(questions):
        tk.Label(window, text=question, font=("Arial", 12), anchor="w", wraplength=50).pack(pady=5, padx=10, anchor="w")
        text_box = tk.Text(window, font=("Arial", 12), wrap="word", width=50, height=4)
        text_box.pack(pady=5, padx=10)
        text_widgets[question] = text_box  # Store the Text widget in the dictionary

    # Multiple-choice question setup
    mc_vars = []  # To hold StringVars for each multiple-choice question
    for mc_question, mc_options in mc_questions:
        tk.Label(window, text=mc_question, font=("Arial", 12), anchor="w").pack(pady=10, padx=10, anchor="w")
        mc_var = tk.StringVar(value="")  # StringVar to hold the selected option
        mc_vars.append(mc_var)  # Store the StringVar for later use
        for option in mc_options:
            tk.Radiobutton(window, text=option, variable=mc_var, value=option, font=("Arial", 12)).pack(anchor="w", padx=20)

    # Save responses and timestamps when the "Submit" button is clicked
    def submit_responses():
        global grouping_number  # Declare as global to modify it
        all_filled = True
        responses_data = []

        # Check if all text responses are filled
        for question, text_box in text_widgets.items():
            response = text_box.get("1.0", "end").strip()  # Get text and strip whitespace
            if not response:
                all_filled = False
                break
            responses_data.append((question, response))
        
        # Check if multiple-choice questions are answered
        for mc_var in mc_vars:
            mc_response = mc_var.get()
            if not mc_response:
                all_filled = False
        
        if not all_filled:
            messagebox.showwarning("Incomplete", "All questions must be answered before submitting.")
            return  # Do not proceed if any answer is missing

        # Save responses to CSV if all questions are answered
        submit_timestamp = datetime.now()  # Timestamp when the user submits their responses
        with open(csv_file, "a", newline="") as file:
            writer = csv.writer(file)
            for question, response in responses_data:
                writer.writerow([grouping_number, prompt_timestamp, submit_timestamp, question, response])
            # Save the responses for the multiple-choice questions
            for mc_question, mc_var in zip(mc_questions, mc_vars):
                writer.writerow([grouping_number, prompt_timestamp, submit_timestamp, mc_question[0], mc_var.get()])

        print(f"Responses saved at {submit_timestamp}")
        grouping_number += 1  # Increment the grouping number for the next set of responses
        window.destroy()  # Close the window after submitting

    # Submit button with padding for spacing
    tk.Button(window, text="Submit", font=("Arial", 12), command=submit_responses).pack(pady=20)
    
    window.mainloop()

# Schedule prompt based on the specified interval
next_prompt_time = datetime.now() + timedelta(seconds=time_interval)
while True:
    if datetime.now() >= next_prompt_time:
        show_prompt()
        next_prompt_time = datetime.now() + timedelta(seconds=time_interval)
    time.sleep(1)  # Sleep briefly to prevent high CPU usage in the loop
