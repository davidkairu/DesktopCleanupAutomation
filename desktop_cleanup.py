import os
#This will help us interact with the file system (e.g., checking for files, creating folders, moving files).

import shutil
#used for moving files between directories

import time
#used to add pauses to ensure the script runs periodically

import threading
#helps us run the script in the background continuously

#Testing
def get_desktop_path():
    return os.path.join(os.path.expanduser("~"),"Desktop")

""" we’ll create a function that categorizes files into folders based on their types. This function will:
            Take a file name as input.
            Determine the file type using the file extension.
            Return the appropriate folder name for each type.
This helps to keep our desktop organized based on categories like "Documents", "Images", etc."""

def categorize_file(file_name):
    # Dictionary to map file extensions to folder names
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
    # Default to "Others" if no match is found
    return "Others"

"""Now that we can categorize files, the next step is to create folders on your desktop for each category. 
This way, when we start moving files, we have the appropriate folders ready."""

def create_category_folders(desktop_path):
    categories = ["Documents", "Images", "Videos", "Music", "Archives", "Programs", "Others"]

    for category in categories:
        category_path = os.path.join(desktop_path, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path) #creates a folder if it doesn't already exist.
            print(f"{category} folder created")
        else:
            print(f"{category} folder already exists")

"""we’ll create a function to move files from your desktop into the appropriate category folders. This function will:
    Iterate through all the files on your desktop.
    Use the categorize_file() function to determine the category.
    Move the file to the appropriate folder."""

def move_files(desktop_path):
    #list all items on the desktop
    items = os.listdir(desktop_path)

    for item in items:
        item_path = os.path.join(desktop_path, item)

        #skip directories (except desktop folders we created)
        if os.path.isdir(item_path):
            continue

        #Get the category for the file
        category = categorize_file(item)

        #determine destination path and move the file
        destination_folder = os.path.join(get_desktop_path(), category)
        destination_path = os.path.join(destination_folder, item)

        shutil.move(item_path, destination_path)
        print(f"{item} moved to {destination_path}")

"""modify the script so it can run periodically, 
checking the desktop every few minutes to clean up any new clutter automatically."""
def run_cleanup_periodically(desktop_path, interval = 300):
    #This function runs an infinite loop that calls the cleanup functions and then
    # waits for a specified interval (default is 300 seconds or 5 minutes).

    while True:
        print("\nStarting desktop cleanup...")
        create_category_folders(desktop_path)
        move_files(desktop_path)
        print("Desktop cleanup complete! Waiting for next cycle")
        time.sleep(interval)

"""This function starts a new thread (cleanup_thread) to 
 run the cleanup in the background. The daemon=True parameter ensures 
 that the background thread will stop when the main script is terminated."""
def start_cleanup_in_background():
    desktop_path = get_desktop_path()
    cleanup_thread = threading.Thread(target=run_cleanup_periodically, args=(desktop_path,))
    cleanup_thread.daemon = True
    cleanup_thread.start()

if __name__ == "__main__":
    start_cleanup_in_background()

    #keep the script running
    try:
        while True:
            time.sleep(1) #keep the thread alive
    except KeyboardInterrupt:
        print("\nCleanup script stopped...")