import argparse
import os
import re

def process_file(input_filename):
    """Modify file contents: replace '.md' with '.c' and adjust gaze_target_type."""
    # Read the input file
    with open(input_filename, 'r', encoding='utf-8') as infile:
        content = infile.read()

    # Replace occurrences
    content = content.replace(".md", ".c")
    content = re.sub(r'gaze_target_type="md"', 'gaze_target_type="c"', content)

    # Write the modified content back
    with open(input_filename, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

    print(f"Processed: {input_filename}")

def process_directory(root_dir):
    """Recursively process files starting with 'itrace_eclipse' in root_dir."""
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.startswith("itrace_eclipse"):
                filepath = os.path.join(dirpath, filename)
                process_file(filepath)

def main():
    parser = argparse.ArgumentParser(description="Recursively process files in a directory.")
    parser.add_argument("input_path", help="File or directory to process.")
    args = parser.parse_args()

    if os.path.isdir(args.input_path):
        process_directory(args.input_path)
    elif os.path.isfile(args.input_path) and os.path.basename(args.input_path).startswith("itrace_eclipse"):
        process_file(args.input_path)
    else:
        print("Error: Provide a valid directory or a matching file.")

if __name__ == "__main__":
    main()
