import pickle
import sqlite3
import os
import argparse
import hashlib
from datetime import datetime, timedelta
import re 
import logging 

# Function to get the file's timestamp and hash
def get_file_metadata(fname):
    file_timestamp = datetime.fromtimestamp(os.path.getmtime(fname)).strftime("%Y-%m-%d %H:%M:%S")
    hasher = hashlib.sha256()
    with open(fname, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    file_hash = hasher.hexdigest()
    return file_timestamp, file_hash

def convert_datetime_to_human(time): 
    return  time.strftime("%Y-%m-%d %H:%M:%S")
    
def convert_system_to_datetime(system_time): 
    #logging.info(f"Converting system time: {system_time}")
    system_time = float(system_time) / 1000.0
    time = datetime.fromtimestamp(float(system_time))
    return time

def convert_string_to_timedelta(time_str):
    """ Convert a string like 2:00 to a timedelta object that can be added to a datetime object."""
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

def get_system_time_from_event_time(fname, event_time): 
    sqliteConnection = sqlite3.connect(fname)  # Connect to the SQLite database
    cursor = sqliteConnection.cursor()
    cursor.execute(f'SELECT * from gaze WHERE "event_time" = {event_time}')  # Retrieve all records from the 'gaze' table
    desc = cursor.description  # Get column descriptions
    col_names = [col[0] for col in desc]  # Extract column names
    data = [dict(zip(col_names, row)) for row in cursor]  # Convert rows to dictionaries
    for i,entry in enumerate(data): # the length should only be 1
        system_time = entry['system_time']
        return system_time
    
def get_event_time_from_fixation_id(fname, fixation_id): 
    sqliteConnection = sqlite3.connect(fname)  # Connect to the SQLite database
    cursor = sqliteConnection.cursor()
    cursor.execute(f'SELECT * from fixation_gaze WHERE "fixation_id" = "{fixation_id}"')  # Retrieve all records from the 'gaze' table
    desc = cursor.description  # Get column descriptions
    col_names = [col[0] for col in desc]  # Extract column names
    data = [dict(zip(col_names, row)) for row in cursor]  # Convert rows to dictionaries
    for i,entry in enumerate(data): # There is more than 1 row per fixation id, so this only verifies per fixation id  
        event_time = entry['event_time']
        return event_time
    
def verify_gazes_table_order(fname): 
    '''
    Verify assumption that all fixations before fixation_id occur before system_time of fixation_id 
    '''
    sqliteConnection = sqlite3.connect(fname)  # Connect to the SQLite database
    cursor = sqliteConnection.cursor()
    cursor.execute(f'SELECT * from gaze')  # Retrieve all records from the 'gaze' table
    desc = cursor.description  # Get column descriptions
    col_names = [col[0] for col in desc]  # Extract column names
    data = [dict(zip(col_names, row)) for row in cursor]  # Convert rows to dictionaries
    for i,entry in enumerate(data): # the length should only be 1
        if i == 0: 
            prev_time = convert_system_to_datetime(entry['system_time'])
        else: 
            current_time = convert_system_to_datetime(entry['system_time']) 
            #print(f"{i}, current_time: {current_time}, prev_time: {prev_time}")
            if current_time < prev_time: 
                logging.error(f"Current time at index {i} {current_time} is < prev_time: {prev_time}, fname: {fname}")
            prev_time = current_time
    logging.info(f"Verified gazes table time ordering")

def verify_fixations_table_order(fname): 
    '''
    Verify assumption that all fixations before fixation_id occur before system_time of fixation_id 
    '''
    sqliteConnection = sqlite3.connect(fname)  # Connect to the SQLite database
    cursor = sqliteConnection.cursor()
    cursor.execute(f'SELECT * from fixation')  # Retrieve all records from the 'fixation' table
    desc = cursor.description  # Get column descriptions
    col_names = [col[0] for col in desc]  # Extract column names
    data = [dict(zip(col_names, row)) for row in cursor]  # Convert rows to dictionaries
    for i,entry in enumerate(data): # the length should only be 1
        if i == 0: 
            event_time = get_event_time_from_fixation_id(fname, entry['fixation_id'])
            system_time = get_system_time_from_event_time(fname, event_time)
            prev_time = convert_system_to_datetime(system_time)
        else: 
            event_time = get_event_time_from_fixation_id(fname, entry['fixation_id'])
            system_time = get_system_time_from_event_time(fname, event_time)
            current_time = convert_system_to_datetime(system_time) 
            #print(f"{i}, fixation_id: {entry["fixation_id"]}, event_time: {event_time}, system_time: {system_time}, current_time: {current_time}, prev_time: {prev_time}")
            if current_time < prev_time: 
                print(f"ERROR: Current time at index {i} {current_time} is < prev_time: {prev_time}, fname: {fname}")
                #exit(1)
            prev_time = current_time
    logging.info(f"Verified fixations table time ordering")

def get_firefly_p8_cutoff(fname): 
    firefly_end_time = convert_string_to_timedelta("2025-01-08 12:31:00") 
    sqliteConnection = sqlite3.connect(fname)  # Connect to the SQLite database
    cursor = sqliteConnection.cursor()
    cursor.execute('SELECT * from fixation_gaze')  # Retrieve all records from the 'gaze' table
    desc = cursor.description  # Get column descriptions
    col_names = [col[0] for col in desc]  # Extract column names
    data = [dict(zip(col_names, row)) for row in cursor]  # Convert rows to dictionaries
    for i,entry in enumerate(data):
       system_time = get_system_time_from_event_time(fname, entry["event_time"])
       if convert_system_to_datetime(system_time) > firefly_end_time: 
           print(f"Found first fixation with time past end with time: {convert_system_to_datetime(system_time)}")
           print(f"entry: {entry}")
           return entry["event_time"], entry["fixation_id"]

# Function to extract fixation data from a SQLite database file
def extract_data(fname, type='fixations'):
    # TODO: we don't need the header row for every db 
    sqliteConnection = sqlite3.connect(fname)  # Connect to the SQLite database
    cursor = sqliteConnection.cursor()
    if type == 'fixations': 
        cursor.execute('SELECT * from fixation')  # Retrieve all records from the 'fixation' table
    elif type == 'gazes': 
        cursor.execute('SELECT * from gaze')  # Retrieve all records from the 'gaze' table
    desc = cursor.description  # Get column descriptions
    col_names = [col[0] for col in desc]  # Extract column names
    data = [dict(zip(col_names, row)) for row in cursor]  # Convert rows to dictionaries
    
    # Make adjustments for firefly 
    participant_id, bug_name = os.path.basename(fname).split("_", 1)
    bug_name = bug_name.rsplit(".", 1)[0]  # Remove the file extension
    if participant_id == "p8" and re.sub(r'_\d+$', '', bug_name) == "firefly": 
        firefly_end_time = convert_string_to_timedelta("2025-01-08 12:31:00") 
        start_firefly_gaze_index = -1 
        stop_firefly_gaze_index = -1 
        event_time, fixation_id = get_firefly_p8_cutoff(fname)

    # Get file metadata
    file_timestamp, file_hash = get_file_metadata(fname)
    print(f"length of data: {len(data)}")
    # Add metadata to each data entry
    for i,entry in enumerate(data):
        entry["source_file"] = fname
        entry["file_timestamp"] = file_timestamp
        entry["file_hash"] = file_hash
        
        if type == 'fixations': 
            entry["system_time"] = get_system_time_from_event_time(fname, get_event_time_from_fixation_id(fname, entry["fixation_id"]))
            entry["human_time"] = convert_datetime_to_human(convert_system_to_datetime(get_system_time_from_event_time(fname, get_event_time_from_fixation_id(fname, entry["fixation_id"]))))
        elif type == 'gazes': 
            entry["human_time"] = convert_datetime_to_human(convert_system_to_datetime(entry["system_time"])) 
        
        try: 
            participant_id, bug_name = os.path.basename(fname).split("_", 1)
            bug_name = bug_name.rsplit(".", 1)[0]  # Remove the file extension
            entry["participant_id"] = participant_id
            entry["bug_name"] = re.sub(r'_\d+$', '', bug_name)
            if entry["participant_id"] == "p8" and entry["bug_name"] == "firefly" and start_firefly_gaze_index == -1: 
                start_firefly_gaze_index = i 
            if entry["participant_id"] == "p8" and entry["bug_name"] == "firefly":
                if type == 'gazes' and entry["event_time"] == event_time:  
                    print(f"{i}: gaze time: {convert_datetime_to_human(convert_system_to_datetime(entry["system_time"]))}, firefly end time: {firefly_end_time}")
                    stop_firefly_gaze = entry 
                    stop_firefly_gaze_index = i 
                    break 
                elif type == 'fixations' and entry["fixation_id"] == fixation_id: 
                    print(f"stopping fixations at fixation: {i} {fixation_id}")
                    stop_firefly_gaze = entry 
                    stop_firefly_gaze_index = i 

        except Exception as e: 
            logging.error(f"Failed to parse input database name into participant id and bug name because: {e}")
    
    if participant_id == "p8" and re.sub(r'_\d+$', '', bug_name) == "firefly": 
        print(f"Need to keep only rows {start_firefly_gaze_index} through {stop_firefly_gaze_index}") 
        data = data[0:stop_firefly_gaze_index]
        print(f"length of data now: {len(data)}")
        print(f"gaze: {stop_firefly_gaze}")
    sqliteConnection.close()  # Close the database connection
    return data

def main():
    # Set up argument parser to get the directory from the user
    parser = argparse.ArgumentParser(description="Extract fixations and gazes from database files.")
    parser.add_argument("directory", type=str, help="Directory to search for .db3 files")
    parser.add_argument("--no-gazes", type=bool, nargs="?", const=True, default=False, help="Don't extract gazes (default: False)")
    parser.add_argument("--no-md", type=bool, nargs="?", const=True, default=False, help="Remove fixations on markdown files .md (default: False)")
    parser.add_argument("--no-verify", type=bool, nargs="?", const=True, default=False, help="Don't verify db time order")
    args = parser.parse_args()

    # Generate a timestamped filename with timestamp at the beginning
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_log = f"{timestamp}_extract_fixations.log"
    print(f"Log: {default_log}")

    # Set up logger 
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(default_log),
                        logging.StreamHandler()
                    ])
    
    # Walk through the directory to find all .db3 files
    alldb = [os.path.join(root, name)
             for root, dirs, files in os.walk(args.directory)
             for name in files
             if name.endswith(".db3")]

    final_fixations = dict()
    final_gazes = dict()
    # Process each .db3 file and extract data
    for i,fname in enumerate(alldb):
        logging.info(f"Getting data for database: {fname}...{i}/{len(alldb)}")
        sample = os.path.basename(fname).replace(".db3", "")  # Extract file name without extension
        try:
            if not args.no_verify: 
                verify_fixations_table_order(fname)
            final_fixations[sample] = extract_data(fname)  # Retrieve fixation data
            if not args.no_gazes: 
                if not args.no_verify: 
                    verify_gazes_table_order(fname)
                final_gazes[sample] = extract_data(fname, 'gazes')  # Retrieve gaze data
        except Exception as e:
            logging.error(f"Error processing {fname}: {e}")  # Print error message if processing fails
    
    
    #input_files = "_".join([os.path.basename(f).replace(".db3", "") for f in alldb])
    # Save extracted data to a pickle file
    fixations_output_filename = f"{timestamp}_fixations.pkl"
    pickle.dump(final_fixations, open(fixations_output_filename, "wb"))
    logging.info(f"Fixations data saved to {fixations_output_filename}")

    if args.no_md: 
        md_files = ["StudyProcedure.c", "StudyInstructions.c", "ladybug.c", "stonefly.c", "hornet.c", "silverfish.c", "praying_mantis.c", "spider.c", "weevil.c", "firefly.c", "pre-study.c", "post-study.c"]
        filtered_data = {
            key: [d for d in value if d.get("fixation_target") not in md_files]
            for key, value in final_fixations.items()
        }
        fixations_output_filename_no_md = f"{timestamp}_fixations_no_md.pkl"
        pickle.dump(filtered_data, open(fixations_output_filename_no_md, "wb"))
        logging.info(f"Fixations data without .md saved to {fixations_output_filename_no_md}")

    if not args.no_gazes: 
        gazes_output_filename = f"{timestamp}_gazes.pkl"
        pickle.dump(final_gazes, open(gazes_output_filename, "wb"))
        logging.info(f"Gaze data saved to {gazes_output_filename}")

if __name__ == "__main__":
    main()
