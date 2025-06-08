import os
import shutil

def move_m4a_files(source_dir, destination_dir):
    # Check if the source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return
    
    # Check if the destination directory exists, if not create it
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        print(f"Created destination directory '{destination_dir}'.")

    # Get a list of all files in the source directory
    files = os.listdir(source_dir)

    # Iterate through each file
    for file in files:
        # Check if the file has a .m4a extension
        if file.endswith(".m4a"):
            # Build the full path to the file
            source_path = os.path.join(source_dir, file)
            # Build the full path to the destination directory
            destination_path = os.path.join(destination_dir, file)
            # Move the file to the destination directory
            shutil.move(source_path, destination_path)
            print(f"Moved '{file}' to '{destination_dir}'.")

# Example usage
source_directory = "/storage/emulated/0/ymusic"
destination_directory = "/storage/emulated/0/Music/Arun/"
move_m4a_files(source_directory, destination_directory)
