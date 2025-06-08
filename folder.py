import os
import shutil
from pathlib import Path

def get_folder_size(folder_path):
    """Get the size of a folder in bytes"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    pass
    except (OSError, PermissionError):
        pass
    return total_size

def format_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def is_folder_empty(folder_path):
    """Check if a folder is completely empty (no files or subdirectories)"""
    try:
        return len(os.listdir(folder_path)) == 0
    except (OSError, PermissionError):
        return False

def find_empty_folders(root_path):
    """Find all empty folders in the directory tree"""
    empty_folders = []
    
    try:
        # Walk through all directories, bottom-up to handle nested empty folders
        for root, dirs, files in os.walk(root_path, topdown=False):
            for directory in dirs:
                folder_path = os.path.join(root, directory)
                if is_folder_empty(folder_path):
                    try:
                        # Get folder info
                        stat_info = os.stat(folder_path)
                        size = get_folder_size(folder_path)
                        
                        folder_info = {
                            'path': folder_path,
                            'size': size,
                            'formatted_size': format_size(size),
                            'modified_time': stat_info.st_mtime
                        }
                        empty_folders.append(folder_info)
                    except (OSError, PermissionError) as e:
                        print(f"Warning: Cannot access {folder_path}: {e}")
                        
    except (OSError, PermissionError) as e:
        print(f"Error accessing root directory {root_path}: {e}")
        return []
    
    return empty_folders

def delete_empty_folders(root_path, confirm_each=False):
    """Main function to find, display, and delete empty folders"""
    
    print(f"Scanning for empty folders in: {root_path}")
    print("=" * 60)
    
    empty_folders = find_empty_folders(root_path)
    
    if not empty_folders:
        print("No empty folders found!")
        return
    
    print(f"Found {len(empty_folders)} empty folder(s):\n")
    
    # Display all empty folders with details
    total_size = 0
    for i, folder_info in enumerate(empty_folders, 1):
        print(f"{i:3d}. {folder_info['path']}")
        print(f"     Size: {folder_info['formatted_size']}")
        print(f"     Modified: {Path(folder_info['path']).stat().st_mtime}")
        total_size += folder_info['size']
        print()
    
    print(f"Total size of empty folders: {format_size(total_size)}")
    print("=" * 60)
    
    # Ask for confirmation
    if confirm_each:
        deleted_count = 0
        for folder_info in empty_folders:
            response = input(f"Delete '{folder_info['path']}'? (y/n/q): ").lower().strip()
            if response == 'q':
                break
            elif response == 'y':
                try:
                    os.rmdir(folder_info['path'])
                    print(f"✓ Deleted: {folder_info['path']}")
                    deleted_count += 1
                except OSError as e:
                    print(f"✗ Failed to delete {folder_info['path']}: {e}")
        print(f"\nDeleted {deleted_count} out of {len(empty_folders)} empty folders.")
    else:
        response = input(f"Delete all {len(empty_folders)} empty folders? (y/n): ").lower().strip()
        if response == 'y':
            deleted_count = 0
            failed_count = 0
            
            for folder_info in empty_folders:
                try:
                    os.rmdir(folder_info['path'])
                    print(f"✓ Deleted: {folder_info['path']}")
                    deleted_count += 1
                except OSError as e:
                    print(f"✗ Failed to delete {folder_info['path']}: {e}")
                    failed_count += 1
            
            print(f"\nSummary:")
            print(f"Successfully deleted: {deleted_count} folders")
            if failed_count > 0:
                print(f"Failed to delete: {failed_count} folders")
            print(f"Total space freed: {format_size(total_size)}")
        else:
            print("Operation cancelled.")

if __name__ == "__main__":
    import sys
    
    # Get the directory path from command line argument or use current directory
    if len(sys.argv) > 1:
        target_directory = sys.argv[1]
    else:
        target_directory = input("Enter the directory path to scan (or press Enter for current directory): ").strip()
        if not target_directory:
            target_directory = "."
    
    # Validate the directory
    if not os.path.exists(target_directory):
        print(f"Error: Directory '{target_directory}' does not exist!")
        sys.exit(1)
    
    if not os.path.isdir(target_directory):
        print(f"Error: '{target_directory}' is not a directory!")
        sys.exit(1)
    
    # Ask for confirmation mode
    print("\nDeletion mode:")
    print("1. Delete all at once (default)")
    print("2. Confirm each deletion individually")
    
    mode = input("Choose mode (1 or 2): ").strip()
    confirm_each = (mode == "2")
    
    try:
        delete_empty_folders(target_directory, confirm_each)
    except KeyboardInterrupt:
        print("\n\nOperation interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
