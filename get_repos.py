import os
import subprocess
import argparse

# Function to check for directory, clone repository, and checkout commit 
def check_and_clone(directory, bug_name, repo_name, repo_url, commit_hash):
    # Step 1: Check if the bug folder exists
    folder_name = bug_name
    bug_path = os.path.join(directory, folder_name)

    if not os.path.exists(bug_path):
        os.mkdir(bug_path)
        print(f"Folder '{bug_path}' created.")
    else:
        print(f"Folder '{bug_path}' already exists.")

   
    repo_path = os.path.join(bug_path, repo_name)

    # Step 2: Check if repository exists 
    if not os.path.exists(repo_path):
        print(f"Git repository '{repo_name}' not found in '{bug_path}'. Cloning from {repo_url}...")
        # Step 3: Clone the repository into the bug folder
        subprocess.run(["git", "clone", repo_url, repo_path])
        print(f"Repository '{repo_name}' cloned successfully into '{bug_path}'.")

        # Step 4: Check out a specific commit
        print(f"Checking out commit '{commit_hash}' in '{repo_path}'...")
        subprocess.run(["git", "checkout", commit_hash], cwd=repo_path)

    else:
        print(f"Repository '{repo_name}' already exists in '{bug_path}'.")

# Main function to handle arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check for existing folders.')
    parser.add_argument('directory', type=str, help='The directory to check for existing repos')

    args = parser.parse_args()

    # Call the function with the given directory
    check_and_clone(args.directory, "ladybug", "sway", "git@github.com:swaywm/sway.git", "d6f279902a094230633cde05f9677da67289dd28")
    check_and_clone(args.directory, "spider", "sway", "git@github.com:swaywm/sway.git", "8d7ebc258a830dc893bef327c2e672a901ced4ed")
    check_and_clone(args.directory, "praying_mantis", "redis", "git@github.com:redis/redis.git", "522760fac79536eb68dc5fc70e9166f689eb76dc")
    check_and_clone(args.directory, "cricket", "openssl", "git@github.com:openssl/openssl.git", "b6144bb8c1be63935ae09e1992c04fbe6e0f88a8")
    check_and_clone(args.directory, "hornet", "sway", "git@github.com:swaywm/sway.git", "77587ee632db2f047e5e0b7979b0319ed2257405")
    check_and_clone(args.directory, "stonefly", "redis", "git@github.com:redis/redis.git", "fe2fdef7b0b65c86eb3cc2685cf0c4efe5007b1c")
    check_and_clone(args.directory, "antlion", "redis", "git@github.com:redis/redis.git", "ce1f9cf81d4758197147294c292bf6a50b3f96d6")
    check_and_clone(args.directory, "silverfish", "redis", "git@github.com:redis/redis.git", "4930d19e70c391750479951022e207e19111eb55")
    check_and_clone(args.directory, "firefly", "openssl", "git@github.com:openssl/openssl.git", "6fa9a84386cc61d00a15c56010900a46429c6242")
    check_and_clone(args.directory, "weevil", "openssl", "git@github.com:openssl/openssl.git", "0c9646ec373e7f3f9b07f218a348ecb82219eaa7")

