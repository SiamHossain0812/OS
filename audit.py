import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 1. File Monitoring with watchdog
class FileAccessHandler(FileSystemEventHandler):
    def __init__(self, log_file="file_access.log"):
        self.log_file = log_file

    def on_modified(self, event):
        if not event.is_directory:
            self.log_event(event.src_path, "modified")

    def on_created(self, event):
        if not event.is_directory:
            self.log_event(event.src_path, "created")

    def on_deleted(self, event):
        if not event.is_directory:
            self.log_event(event.src_path, "deleted")

    def on_moved(self, event):
        if not event.is_directory:
            self.log_event(event.src_path, f"moved to {event.dest_path}")

    def log_event(self, file_path, action):
        with open(self.log_file, "a") as log:
            log.write(f"{time.ctime()} - {file_path} was {action}\n")
        print(f"Logged: {time.ctime()} - {file_path} was {action}")

def monitor_files(directory_to_watch):
    event_handler = FileAccessHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory_to_watch, recursive=True)
    observer.start()
    print(f"Monitoring directory: {directory_to_watch}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# 2. System-Level Auditing with auditd
def configure_auditd(directory_to_monitor):
    rule = f"sudo auditctl -w {directory_to_monitor} -p rwxa"
    try:
        subprocess.run(rule, shell=True, check=True)
        print(f"Auditd rule added to monitor {directory_to_monitor}")
    except subprocess.CalledProcessError as e:
        print(f"Error adding auditd rule: {e}")

def view_auditd_logs(target_path="/path/to/watch"):
    try:
        subprocess.run(f"sudo ausearch -f {target_path}", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error viewing audit logs: {e}")
