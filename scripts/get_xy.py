import time
import csv
import argparse
from pynput import mouse, keyboard

# Parse command-line argument for output CSV file
parser = argparse.ArgumentParser(description="Record mouse clicks and save to a CSV file.")
parser.add_argument("output", type=str, help="Name of the output CSV file")
args = parser.parse_args()

# Open CSV file and record mouse clicks
with open(args.output, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "X", "Y", "Event"])
    
    def on_click(x, y, button, pressed):
        event_type = "Pressed" if pressed else "Released"
        writer.writerow([time.time(), x, y, f"{button} {event_type}"])
        print(f"Mouse {button} {event_type} at ({x}, {y})")
    
    def on_key_press(key):
        print("Key pressed! Starting click recording...")
        return False  # Stop listening for keypress after first press
    
    # Wait for a key press before recording clicks
    with keyboard.Listener(on_press=on_key_press) as key_listener:
        print("Press any key to start recording mouse clicks...")
        key_listener.join()
    
    # Set up mouse listener
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    print("Recording mouse clicks. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nRecording stopped.")
        listener.stop()
