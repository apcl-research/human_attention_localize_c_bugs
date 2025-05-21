import argparse
import os

def rename_files_in_directory(directory):
    # Loop through all files in the provided directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Check if it's a file (and not a subdirectory)
        if os.path.isfile(file_path):
            # If the file has a .md extension, rename it to .c
            if filename.endswith('.md'):
                new_filename = filename[:-3] + '.c'  # Replace '.md' with '.c'
                new_file_path = os.path.join(directory, new_filename)

                # Rename the file
                os.rename(file_path, new_file_path)
                print(f"Renamed: {filename} -> {new_filename}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Rename all .md files in a directory to .c files.")
    parser.add_argument('directory', type=str, help="Directory to process")

    # Parse the arguments
    args = parser.parse_args()

    # Rename files in the given directory
    rename_files_in_directory(args.directory)

if __name__ == "__main__":
    main()
