import pickle
from statistics import mean, median
import argparse
import csv
import os 
import logging 
from datetime import datetime, timedelta
from collections import Counter
import pandas as pd 

def convert_datetime_to_human(time): 
    return  time.strftime("%Y-%m-%d %H:%M:%S")
    
def convert_system_to_datetime(system_time): 
    #logging.info(f"Converting system time: {system_time}")
    system_time = float(system_time) / 1000.0
    time = datetime.fromtimestamp(float(system_time))
    return time

def get_times(data, output_stem): 
    # Open csv 
    duration_filename = f"{output_stem}_duration.csv"
    col_headers = ["bug", "session_id", "start", "end", "duration"]
    with open(duration_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(col_headers)  # Write header row 
        for session in data: 
            bug = data[session][0]["bug_name"]
            participant_id = data[session][0]["participant_id"]
            logging.info(f"bug name: {bug}, particiapnt id: {participant_id}")
            # Pull times from pkl 
            first_entry_system_time = data[session][0]['system_time']
            last_entry_system_time = data[session][len(data[session])-1]['system_time']
            first_entry_time = convert_system_to_datetime(first_entry_system_time)
            last_entry_time = convert_system_to_datetime(last_entry_system_time)
            difference = last_entry_time - first_entry_time
            # Write times to csv 
            info = {"bug": bug, "session": session, "start time": convert_datetime_to_human(first_entry_time), "end time": convert_datetime_to_human(last_entry_time), "duration":difference}
            writer.writerow(info.values())

def parse_coordinates(coord_str):
    """Convert a coordinate string like '(470,70)' into a tuple (470, 70)."""
    return tuple(map(int, coord_str.strip("()").split(",")))

def find_region(data, x, y):
    """Determine which region the (x, y) coordinate belongs to."""
    #logging.info(f"x: {x}, y: {y}, data: {data}")
    for entry, details in data.items():
        regions = [key for key in data.keys() if key.startswith("region") and key.endswith("name")]
        #logging.info(f"Found regions: {regions}")
        for region_key in regions:
            region_name = data[region_key]
            #logging.info(f"region_name: {region_name}")
            if region_name == '': 
                #logging.info(f"returning because reached end of filled in regions")
                return None # got to end of filled in regions 
            prefix = region_key.rsplit("_", 1)[0]  # Extract "region1", "region2", etc.
            #logging.info(f"prefix: {prefix}")
            # Get top-left and bottom-right coordinates
            topleft = parse_coordinates(data[f"{prefix}_topleft"])
            bottomright = parse_coordinates(data[f"{prefix}_bottomright"])
            #logging.info(f"Coordinates of region {region_key} are {topleft}, {bottomright}")

            # Check if (x, y) is inside the region
            if topleft[0] <= x <= bottomright[0] and topleft[1] <= y <= bottomright[1]:
                return prefix  # Return the matching region

    return None  # No region found

def convert_string_to_timedelta(time_str):
    """ Convert a string like 2:00 to a timedelta object that can be added to a datetime object."""
    minutes, seconds = map(int, time_str.split(":"))
    time_delta = timedelta(minutes=minutes, seconds=seconds)
    return time_delta

def get_time_delta(time_str): 
    time_delta= convert_string_to_timedelta(time_str)
    return time_delta

def check_start_gaze(check_start, i, gaze, start_gaze_time): 
    if check_start: 
        gaze_time = convert_system_to_datetime(gaze["system_time"])
        if gaze_time < start_gaze_time: 
            #logging.info(f"Skipping gaze {i} at time {convert_datetime_to_human(gaze_time)} because it is before start time: {convert_datetime_to_human(start_gaze_time)}")
            # don't add to total_gazes because those should be counted in a different iteration 
            return True  
    return False 

def check_end_gaze(check_end, i, gaze, end_gaze_time): 
    if check_end:
        gaze_time = convert_system_to_datetime(gaze["system_time"])
        if gaze_time > end_gaze_time: 
            #logging.info(f"Skipping gaze {i} at time {convert_datetime_to_human(gaze_time)} because it is after end time: {convert_datetime_to_human(end_gaze_time)}")
            # don't add to total_gazes because those should be counted in a different iteration 
            return True 
    return False 


def check_start_end(region_xys, id): 
    check_start = False 
    check_end = False 
    start_delta = None
    end_delta = None
    start = region_xys[id]["start"]
    end = region_xys[id]["end"]
    if start != "start": 
        logging.info(f"ID {id} from the region_xys sheet has start time {start}!")
        start_delta = get_time_delta(start)
        check_start = True 
    if end != "end": 
        logging.info(f"ID {id} from the region_xys sheet has end time {end}!")
        end_delta = get_time_delta(end)
        check_end = True 
    return check_start, check_end, start_delta, end_delta

def get_gaze_counts(data, region_xys): 
    for id in region_xys:  
        logging.info(f"Getting info for id: {id}")
        session = region_xys[id]["session"]
        logging.info(f"Session {session} matches id: {id}")
        if session not in data:  # Make sure gaze data to match session exists 
            logging.error(f"Could not find {session} in gazes data!") # should we break instead? 
            continue 
        check_start, check_end, start_delta, end_delta = check_start_end(region_xys, id)
        this_session_regions = region_xys[id]
        this_session_regions["out_of_bounds"] = 0 
        this_session_regions["no_x_y"] = 0 
        this_session_regions["total_gazes"] = 0 
        start_gaze_time = None
        end_gaze_time = None
        for i,gaze in enumerate(data[session]): 
            try: 
                if check_start and i == 0: 
                    first_gaze_time = convert_system_to_datetime(gaze["system_time"])
                    start_gaze_time = first_gaze_time + start_delta
                    logging.info(f"First gaze time: {convert_datetime_to_human(first_gaze_time)}, start gaze time: {convert_datetime_to_human(start_gaze_time)}")
                if check_end and i == 0:
                    first_gaze_time = convert_system_to_datetime(gaze["system_time"])
                    end_gaze_time = first_gaze_time + end_delta
                    logging.info(f"First gaze time: {convert_datetime_to_human(first_gaze_time)}, end gaze time: {convert_datetime_to_human(end_gaze_time)}")
                if check_start_gaze(check_start, i, gaze, start_gaze_time):
                    continue 
                if check_end_gaze(check_end, i, gaze, end_gaze_time):
                    logging.info(f"Ending because gaze {i} is after end time")
                    break 
                x = int(gaze["x"])
                y = int(gaze["y"])
                #logging.info(f"x: {x}, y: {y}, this session regions: {this_session_regions}")
                region = find_region(this_session_regions, x, y)
                if region == None: 
                    #logging.warning(f"x,y: ({x},{y}) not in region")
                    this_session_regions["out_of_bounds"] += 1 
                    this_session_regions["total_gazes"] +=1 
                    continue 
                #logging.info(f"x: {x} y: {y} in region: {region}")
                this_session_regions[f"{region}_gaze_count"] += 1 
                this_session_regions["total_gazes"] += 1
            
            except Exception as e: 
                #logging.warning(f"x,y for gaze {gaze} could not be found because {e}")
                this_session_regions["no_x_y"] += 1 
                this_session_regions["total_gazes"] += 1 
            
        region_xys[id] = this_session_regions 
    return region_xys


def main():
    # TODO: add percentages 
    # Create argument parser
    parser = argparse.ArgumentParser(description="Get region from gaze pkl.")
    
    # Add arguments for input and output files
    parser.add_argument('input_file', type=str, help="Gaze pkl file")
    parser.add_argument('region_xys_file', type=str, help="csv containing regions and x,y coordinates for each session")
    args = parser.parse_args()
    input_stem = os.path.splitext(os.path.basename(args.input_file))[0]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"{timestamp}_get_region_times_{input_stem}_outputs"
    os.mkdir(output_dir)
    output_stem = f"{output_dir}/{input_stem}" 
    default_log = f"{output_stem}_get_region_times.log" 
    print(f"Log: {default_log}")

    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(default_log),
                        logging.StreamHandler()
                    ])
    # Load data from .pkl file 
    data = pickle.load(open(args.input_file, "rb"))
    get_times(data, output_stem)

    df = pd.read_excel(args.region_xys_file)
    df = df.fillna("")  # Replace NaN with empty string
    region_xys = df.set_index(df.columns[0]).to_dict(orient="index")
    region_xys = get_gaze_counts(data, region_xys)
    region_xys_df = pd.DataFrame.from_dict(region_xys, orient="index")
    region_xys_df.to_csv(f"{output_stem}_gaze_counts_per_region.csv", index=False)

if __name__ == "__main__":
    main()