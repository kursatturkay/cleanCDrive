import os
import send2trash
import time
import subprocess
import shutil

def get_file_size_in_mb(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)

def disable_hibernation():
    try:
        print("Disabling hibernation...")
        subprocess.run("powercfg -h off", check=True, shell=True)
        print("Hibernation disabled successfully.")
    except Exception as e:
        print(f"Error disabling hibernation: {e}")

def delete_temp_files():
    try:
        
        user_temp_path = os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Local', 'Temp')

        
        if os.path.exists(user_temp_path):
            for root, dirs, files in os.walk(user_temp_path, topdown=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    try:
                        os.rmdir(dir_path)  
                        print(f"Deleted directory: {dir_path}")
                    except Exception as e:
                        print(f"Error deleting directory {dir_path}: {e}")
        else:
            print(f"Temp folder not found at {user_temp_path}")
    except Exception as e:
        print(f"Error cleaning Temp folder: {e}")

def cleanup_drive(drive, extensions):
    total_size = 0
    start_time = time.time()

    for root, _, files in os.walk(drive):
        
        if "$Recycle.Bin" in root:
            continue
        
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                try:
                    if not os.path.exists(file_path):  
                        print(f"Skipping missing file: {file_path}")
                        continue

                    size_in_mb = get_file_size_in_mb(file_path)

                    
                    send2trash.send2trash(file_path)

                    total_size += size_in_mb
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    
    hibernation_file = os.path.join(drive, "hiberfil.sys")
    if os.path.exists(hibernation_file):
        try:
            print("Hibernation file found. Attempting to delete...")
            os.remove(hibernation_file)
            print("Hibernation file deleted.")
            total_size += get_file_size_in_mb(hibernation_file)
        except Exception as e:
            print(f"Error deleting hibernation file: {e}")

    elapsed_time = time.time() - start_time
    return total_size, elapsed_time

def generate_report(total_size, elapsed_time):
    print("\n--- Cleanup Report ---")
    print(f"\nTotal space freed: {total_size / 1024:.2f} GB")
    print(f"Time taken for cleanup: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    
    disable_hibernation()

    
    delete_temp_files()

    drive = "C:\\"
    extensions_to_cleanup = [".tmp", ".log", ".bak", ".old", ".dmp", ".trec"]

    print("Scanning and cleaning up...\n")
    total_size, elapsed_time = cleanup_drive(drive, extensions_to_cleanup)
    generate_report(total_size, elapsed_time)
