import os
import shutil
import time
import threading
import hashlib
import zipfile
from datetime import datetime

# Function to get the desktop path
def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

# Function to get the Downloads folder path
def get_special_folder_paths():
    home_path = os.path.expanduser("~")
    downloads_path = os.path.join(home_path, "Downloads")
    return downloads_path

# Function to categorize files based on their extension
def categorize_file(file_name):
    file_categories = {
        'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
        'Images': ['.jpg', '.jpeg', '.png', '.gif'],
        'Videos': ['.mp4', '.mov', '.avi'],
        'Music': ['.mp3', '.wav'],
        'Archives': ['.zip', '.rar', '.tar'],
        'Programs': ['.exe', '.sh', '.bat']
    }

    # Extract file extension
    _, file_extension = os.path.splitext(file_name)

    # Find the category for the file extension
    for category, extensions in file_categories.items():
        if file_extension.lower() in extensions:
            return category
    return "Others"

# Function to create category folders
def create_category_folders(folder_path):
    categories = ["Documents", "Images", "Videos", "Music", "Archives", "Programs", "Others"]

    for category in categories:
        category_path = os.path.join(folder_path, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
            print(f"{category} folder created in {folder_path}")
        else:
            print(f"{category} folder already exists in {folder_path}")

# Function to move files to their respective category folders
def move_files(folder_path):
    items = os.listdir(folder_path)

    for item in items:
        item_path = os.path.join(folder_path, item)

        # Skip directories
        if os.path.isdir(item_path):
            continue

        # Get the category for the file
        category = categorize_file(item)

        # Determine destination path and move the file
        destination_folder = os.path.join(folder_path, category)
        destination_path = os.path.join(destination_folder, item)

        shutil.move(item_path, destination_path)
        print(f"{item} moved to {destination_path}")

# Function to calculate file hash to identify duplicates
def calculate_file_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Function to remove duplicate files within a folder
def remove_duplicates(folder_path):
    seen_files = {}
    items = os.listdir(folder_path)

    for item in items:
        item_path = os.path.join(folder_path, item)

        # Skip directories
        if os.path.isdir(item_path):
            continue

        # Calculate hash of the file to detect duplicates
        file_hash = calculate_file_hash(item_path)

        if file_hash in seen_files:
            # If the file is a duplicate, remove it
            os.remove(item_path)
            print(f"Removed duplicate file: {item_path}")
        else:
            # If the file is unique, add its hash to the seen_files dictionary
            seen_files[file_hash] = item_path

# Function to compress older files within a folder
def compress_old_files_in_folder(folder_path, days_old=30):
    archive_folder = os.path.join(folder_path, "Archives")

    # Create an Archives folder within each category if it doesn't exist
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    items = os.listdir(folder_path)

    for item in items:
        item_path = os.path.join(folder_path, item)

        # Skip directories and the Archives folder itself
        if os.path.isdir(item_path) or item == "Archives":
            continue

        # Get the age of the file
        file_age = get_file_age_in_days(item_path)

        # Compress the file if it is older than the specified number of days
        if file_age > days_old:
            zip_file_path = os.path.join(archive_folder, f"{item}.zip")

            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(item_path, item)
                print(f"Compressed '{item}' into '{zip_file_path}'")

            # Remove the original file after compression
            os.remove(item_path)
            print(f"Removed original file '{item}' after compression")

# Function to get the file modification time in days
def get_file_age_in_days(file_path):
    file_mod_time = os.path.getmtime(file_path)
    file_age = (datetime.now() - datetime.fromtimestamp(file_mod_time)).days
    return file_age

# Function to clean each folder by removing duplicates and compressing older files
def clean_folders(folder_paths):
    for folder_path in folder_paths:
        if os.path.exists(folder_path):
            # Step 1: Remove duplicate files in the folder
            remove_duplicates(folder_path)

            # Step 2: Compress old files in the folder
            compress_old_files_in_folder(folder_path)

# Function to run cleanup periodically
def run_cleanup_periodically(folder_paths, interval=(5)):
    while True:
        print("\nStarting desktop cleanup...")
        for folder_path in folder_paths:
            create_category_folders(folder_path)
            move_files(folder_path)
        clean_folders(folder_paths)
        print("Desktop cleanup complete! Waiting for next cycle")
        time.sleep(interval)

# Start the cleanup in the background
def start_cleanup_in_background():
    desktop_path = get_desktop_path()
    downloads_path = get_special_folder_paths()
    folder_paths = [desktop_path, downloads_path]
    cleanup_thread = threading.Thread(target=run_cleanup_periodically, args=(folder_paths,))
    cleanup_thread.daemon = True
    cleanup_thread.start()

if  __name__ == "__main__":
    start_cleanup_in_background()

    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCleanup script stopped...")
