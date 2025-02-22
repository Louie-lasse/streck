"""
This script is to start the bastugatan and streck scripts.
This script should be located outside of this directory, but run with the context of this directory.
"""


import os
import time
import subprocess
from datetime import datetime
import atexit

# Paths
#repo_dir = os.path.expanduser()
backup_dir = os.path.expanduser("streck_backups/")
db_path = "streck/streck.db"

bg = "bastugatan.py"
streck = "streck.py"

branch = "master"

# Process storage
processes = {}
last_maintenance = None

def start_script(name, version=""):
    """Starts a script and stores its process."""
    path = name
    proc = subprocess.Popen([f"python{version}", path], start_new_session=True)
    processes[name] = proc
    print(f"Started {name} (PID: {proc.pid})")

def stop_script(name):
    """Stops a running script if it is running."""
    if name in processes and processes[name].poll() is None:
        print(f"Stopping {name} (PID: {processes[name].pid})")
        processes[name].terminate()
        processes[name].wait()

def check_and_restart():
    """Checks if a process has stopped and restarts it if necessary."""
    for name, proc in processes.items():
        print(f"Checking {name}...")
        if proc and proc.poll() is not None:  # Process has stopped
            print(f"{name} has stopped. Restarting...")
            start_script(name)

def check_for_updates():
    """Stops A and B, updates repo, and restarts them."""
    print("Checking for updates...")

    check_update_cmd = (
        "git fetch origin && "
        "git rev-parse HEAD > .git/current_commit && "
        f"git rev-parse origin/{branch} > .git/latest_commit && "
        "diff .git/current_commit .git/latest_commit"
    )

    update_code = os.system(check_update_cmd)

    if update_code == 0:
        print("No updates found.")
        check_and_restart()
        return

    stop_script(bg)
    stop_script(streck)
    
    update_command = (
        "git pull || (git merge --abort; git reset --hard)"
    )
    exit_code = os.system(update_command)

    if exit_code != 0:
        print("Git update failed or merge conflict detected. Running old version.")
        return
    
    print("Repository updated successfully!")

    start_script(bg)
    start_script(streck, "3")

def cleanup_old_backups(days_old):
    """Deletes backups older than `days_old` days."""
    current = time.time()
    cutoff = current - days_old * 86400
    print(f"cutoff: {cutoff}")
    print(f"current: {current}")

    # List all files in the backup directory
    for filename in os.listdir(backup_dir):
        file_path = os.path.join(backup_dir, filename)

        # Check if the file is older than the cutoff
        if os.path.isfile(file_path):
            file_age = os.path.getmtime(file_path)  # Last modification time
            if file_age < cutoff:
                print(f"Deleting old backup: {filename}")
                os.remove(file_path)

def backup_database():
    """Backs up the database with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = os.path.join(backup_dir, f"streck_backup_{timestamp}.db")
    os.system(f"cp {db_path} {backup_file}")
    print(f"Database backed up to {backup_file}")

    cleanup_old_backups(14)

def exit_handler():
    """Stops all running scripts."""
    print("Stopping all running scripts...")
    stop_script(bg)
    stop_script(streck)

atexit.register(exit_handler)

# Start scripts on launch
def main():
    start_script(bg)
    start_script(streck, "3")

    while True:
        now = datetime.now()

        # Run daily maintenance at noon
        #if now.hour == 12 and last_maintenance != now.date():
        print("Performing daily maintenance...")
        check_for_updates()
        backup_database()
        last_maintenance = now.date()

        time.sleep(60)

if __name__ == "__main__":
    main()
