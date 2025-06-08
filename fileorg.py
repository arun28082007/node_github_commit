import os
import shutil

# this is main function
def organize_files(source_dir, destination_dir):
    # Create destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Iterate over files in the source directory
    for filename in os.listdir(source_dir):
        # Skip directories
        if os.path.isdir(os.path.join(source_dir, filename)):
            continue
        
        # Get the file extension
        _, extension = os.path.splitext(filename)

        # Create directory for the file extension if it doesn't exist
        extension_dir = os.path.join(destination_dir, extension[1:])
        if not os.path.exists(extension_dir):
            os.makedirs(extension_dir)

        # Move the file to the appropriate directory
        destination_file_path = os.path.join(extension_dir, filename)
        # If file already exists in the destination directory, add a number suffix
        if os.path.exists(destination_file_path):
            base, extension = os.path.splitext(filename)
            count = 1
            while os.path.exists(os.path.join(extension_dir, f"{base}_{count}{extension}")):
                count += 1
            destination_file_path = os.path.join(extension_dir, f"{base}_{count}{extension}")
        shutil.move(os.path.join(source_dir, filename), destination_file_path)
        
        # Print the file moved
        print(f"Moved: {filename} to {destination_file_path}")

# Example usage
source_directory = input("Enter source directory\n")
destination_directory = source_directory
organize_files(source_directory, destination_directory)
