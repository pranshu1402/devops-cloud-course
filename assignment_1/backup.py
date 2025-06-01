# Q4. In DevOps, performing regular backups of important files is crucial:
# ● Implement a Python script called backup.py that takes a source directory and a destination directory as command-line arguments.
# ● The script should copy all files from the source directory to the destination directory.
# ● Before copying, check if the destination directory already contains a file with the same name. If so, append a timestamp to the file name to ensure uniqueness.
# ● Handle errors gracefully, such as when the source directory or destination directory does not exist.
# Sample Command:
# python backup.py /path/to/source /path/to/destination
# By running the script with the appropriate source and destination directories, it should create backups of the files in the source directory, ensuring unique file names in the destination directory.

import os
import sys
import time

def append_timestamp(filename):
    base, ext = os.path.splitext(filename)
    timestamp = time.strftime("%Y%m%d%H%M%S")
    return f"{base}_{timestamp}{ext}"

def backup_files_in_directory(source_dir, dest_dir):
    try:
        if not os.path.exists(source_dir) or not os.path.isdir(source_dir):
            print(f"Error: Source directory {source_dir} does not exist.")
            return
        if not os.path.exists(dest_dir) or not os.path.isdir(dest_dir):
            print(f"Error: Destination directory {dest_dir} does not exist.")
            return
        
        files = os.listdir(source_dir)
        
        for file in files:
            source_file_path = os.path.join(source_dir, file)
            dest_file_path = os.path.join(dest_dir, file)

            if not os.path.isfile(source_file_path):
                continue

            if os.path.exists(dest_file_path):
                new_file_name = append_timestamp(file)
                dest_file_path = os.path.join(dest_dir, new_file_name)

            try:
                with open(source_file_path, 'rb') as src, open(dest_file_path, 'wb') as dest:
                    dest.write(src.read())
            except Exception as e:
                print(f"Error copying file {source_file_path} to {dest_file_path}: {e}")
    
    except Exception as e:
        print(f"Error copying {source_dir} to {dest_dir}: {e}")

if __name__ == "__main__":
    source_dir = sys.argv[1]
    dest_dir = sys.argv[2]
    backup_files_in_directory(source_dir, dest_dir)

