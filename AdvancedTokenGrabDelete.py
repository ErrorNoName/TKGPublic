import os
import psutil
import time
import shutil
import winreg
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Colors for output
INFO = Fore.CYAN + "[INFO]" + Style.RESET_ALL
SUCCESS = Fore.GREEN + "[SUCCESS]" + Style.RESET_ALL
ERROR = Fore.RED + "[ERROR]" + Style.RESET_ALL
LOADING = Fore.YELLOW + "[LOADING]" + Style.RESET_ALL

# Target software to detect and remove
TARGET_PROCESS = 'TokenGrab.exe'
TARGET_DIRECTORIES = [
    r'C:\path\to\installation\directory',  # Change this to your installation path
    os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
]

# Function to display a loading animation
def loading_animation(text):
    for _ in range(5):
        print(LOADING + f" {text}...", end="\r")
        time.sleep(0.2)
    print(LOADING + f" {text} complete!")

# Function to check if the target software is running
def is_process_running(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None

# Function to terminate the target process
def terminate_process(pid):
    try:
        loading_animation(f"Terminating process {pid}")
        process = psutil.Process(pid)
        process.terminate()
        process.wait()  # Wait for the process to terminate
        print(SUCCESS + f" Process {pid} terminated.")
    except Exception as e:
        print(ERROR + f" Error terminating process {pid}: {e}")

# Function to delete the software installation directory
def delete_directory(directory):
    if os.path.exists(directory):
        try:
            loading_animation(f"Deleting directory {directory}")
            shutil.rmtree(directory)
            print(SUCCESS + " Directory successfully deleted.")
        except Exception as e:
            print(ERROR + f" Error deleting directory: {e}")
    else:
        print(SUCCESS + f" Directory {directory} not found.")

# Remove the software from the startup folder
def remove_from_startup():
    startup_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup\windows_manager.py')
    if os.path.exists(startup_path):
        try:
            loading_animation("Removing from Startup")
            os.remove(startup_path)
            print(SUCCESS + " Removed from Startup folder.")
        except Exception as e:
            print(ERROR + f" Error removing from Startup folder: {e}")
    else:
        print(SUCCESS + " Startup entry not found.")

# Remove the software from the Windows Registry
def remove_from_registry():
    try:
        loading_animation("Removing from Windows Registry")
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_ALL_ACCESS)
        try:
            winreg.DeleteValue(reg_key, 'windows_manager')
            print(SUCCESS + " Removed registry entry from 'Run'.")
        except FileNotFoundError:
            print(SUCCESS + " Registry entry not found.")
        winreg.CloseKey(reg_key)
    except Exception as e:
        print(ERROR + f" Error removing from registry: {e}")

# Check if a scheduled task exists for the software and remove it
def remove_scheduled_task(task_name='windows_manager'):
    try:
        loading_animation("Removing Scheduled Task")
        os.system(f'schtasks /delete /tn {task_name} /f')
        print(SUCCESS + " Scheduled task removed.")
    except Exception as e:
        print(ERROR + f" Error removing scheduled task: {e}")

# Display a progress bar for file deletion
def progress_bar(task, seconds):
    for _ in tqdm(range(seconds), desc=task):
        time.sleep(1)

# Main function for antivirus behavior
def main():
    print(INFO + " Starting antivirus scan...")

    # Step 1: Check if the target software is running
    pid = is_process_running(TARGET_PROCESS)
    if pid:
        print(INFO + f" {TARGET_PROCESS} is running with PID: {pid}")
        
        # Step 2: Terminate the running process
        terminate_process(pid)
        progress_bar("Terminating process", 3)
    else:
        print(SUCCESS + f" {TARGET_PROCESS} is not running.")
    
    # Step 3: Check if the installation directories exist and delete them
    for directory in TARGET_DIRECTORIES:
        delete_directory(directory)
        progress_bar(f"Deleting {directory}", 3)
    
    # Step 4: Remove the software from the startup folder
    remove_from_startup()
    progress_bar("Removing from startup", 2)

    # Step 5: Remove from the Windows Registry
    remove_from_registry()
    progress_bar("Removing from registry", 2)
    
    # Step 6: Remove any scheduled tasks related to the software
    remove_scheduled_task()
    progress_bar("Removing scheduled tasks", 2)
    
    print(SUCCESS + " Antivirus scan completed and system cleaned.")

if __name__ == "__main__":
    main()
