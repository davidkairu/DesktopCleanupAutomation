# Desktop Cleanup Automation Script

## Overview
This project is a Python automation script designed to keep your desktop clean and organized. It runs periodically in the background, categorizes files into different folders, removes duplicate files, and compresses older files. The goal is to minimize desktop clutter and maintain an organized environment effortlessly.

## Features

1. **File Categorization**: Automatically categorizes files into folders based on their type (e.g., Documents, Images, Videos).
2. **Periodic Cleanup**: Runs periodically in the background to ensure continuous desktop organization.
3. **Remove Duplicate Files**: Removes duplicate files from categorized folders based on content comparison.
4. **Compress Older Files**: Compresses files older than a specified threshold to save space.
5. **Runs in Background**: Uses threading to run continuously without disrupting your workflow.

## How It Works
1. The script first **creates category folders** on the desktop, such as Documents, Images, Videos, Music, etc.
2. Files are then **moved from the desktop** into these respective folders based on their file extensions.
3. The script **removes duplicate files** within each categorized folder, ensuring only one copy of each unique file is kept.
4. **Older files** are compressed into ZIP archives to save space.
5. The entire process runs in a **background thread** and repeats periodically to keep the desktop clutter-free.

## Folder Categories
The following folders are created on the desktop to categorize files:
- **Documents**: Files with extensions like `.pdf`, `.docx`, `.txt`, `.xlsx`, `.pptx`.
- **Images**: Files like `.jpg`, `.jpeg`, `.png`, `.gif`.
- **Videos**: Files like `.mp4`, `.mov`, `.avi`.
- **Music**: Files like `.mp3`, `.wav`.
- **Archives**: Compressed files like `.zip`, `.rar`, `.tar`.
- **Programs**: Executable files like `.exe`, `.sh`, `.bat`.
- **Others**: Files that do not match any of the specified categories.

## Setup Instructions

### Prerequisites
- **Python 3**: Ensure Python 3 is installed on your system. You can check by running `python3 --version` in your terminal.
- **PyCharm or Any Code Editor**: You can use any code editor of your choice, though PyCharm is recommended for Python projects.

### Step-by-Step Setup
1. **Clone or Download the Project**:
   - Clone the repository or download the `desktop_cleanup.py` script.

2. **Create a Virtual Environment** (optional but recommended):
   ```sh
   python3 -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install Required Libraries**:
   - The script uses standard libraries (`os`, `shutil`, `time`, `threading`, `hashlib`, `zipfile`, and `datetime`). No additional libraries need to be installed.

4. **Run the Script**:
   - Open the script in PyCharm or your preferred editor.
   - Run the script to start the automatic desktop cleanup process.

5. **(Optional) Set Up on System Startup**:
   - To make the script run automatically at startup, you can use **LaunchAgents** on macOS, **Task Scheduler** on Windows, or **cron jobs** on Linux. Refer to the "Automatic Startup" section below for details.

## Automatic Startup
### macOS (Using LaunchAgents)
1. Create a `.plist` file in `~/Library/LaunchAgents/` with the following content:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.desktop.cleanup</string>
       <key>ProgramArguments</key>
       <array>
           <string>/usr/local/bin/python3</string>
           <string>/path/to/desktop_cleanup.py</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
       <key>StandardOutPath</key>
       <string>/tmp/desktop_cleanup.out</string>
       <key>StandardErrorPath</key>
       <string>/tmp/desktop_cleanup.err</string>
   </dict>
   </plist>
   ```
   Replace `/path/to/desktop_cleanup.py` with the full path to your Python script.

2. Load the `.plist` using Terminal:
   ```sh
   launchctl load ~/Library/LaunchAgents/com.desktop.cleanup.plist
   ```

### Windows (Using Task Scheduler)
1. Create a batch file (`desktop_cleanup.bat`) with the following content:
   ```bat
   @echo off
   python "path_to_your_script\desktop_cleanup.py"
   ```
   Replace `path_to_your_script` with the full path to your Python script.

2. Use **Task Scheduler** to create a new task that runs this batch file at login.

## Logging
- **Standard Output** (`stdout`): The script logs general output, like files being moved or compressed, to `/tmp/desktop_cleanup.out` (on macOS).
- **Standard Error** (`stderr`): Any errors encountered during execution are logged to `/tmp/desktop_cleanup.err` (on macOS).
- To view these logs, use the following command in Terminal:
  ```sh
  cat /tmp/desktop_cleanup.out
  cat /tmp/desktop_cleanup.err
  ```

## Customization
### Configurable Options
1. **Interval Between Cleanups**:
   - You can adjust the interval for how often the cleanup runs by modifying the `interval` parameter in the `run_cleanup_periodically()` function.

2. **File Age for Compression**:
   - By default, files older than **30 days** are compressed. You can adjust this value by changing the `days_old` parameter in the `compress_old_files_in_folder()` function.

3. **Category Customization**:
   - You can add new categories or modify existing ones by editing the `file_categories` dictionary in the `categorize_file()` function.

## Future Enhancements
- **Graphical User Interface (GUI)**: Adding a simple GUI to manage cleanup settings.
- **User Confirmation for Cleanup Actions**: Ask for confirmation before deleting or compressing files.
- **Cloud Backup Integration**: Integrate with Google Drive or Dropbox to back up important files before cleanup.

## Contributing
Contributions are welcome! Feel free to submit a pull request or report issues to help improve this project.

## License
This project is licensed under the MIT License. Feel free to use and modify it as needed.


