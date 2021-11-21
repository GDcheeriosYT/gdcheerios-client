import subprocess
import sys

def install(package):
    print(f"installing requirement {package}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

import info

try:
    import urllib.request
except ModuleNotFoundError:
    install("urllib")
    import urllib.request
    
try:
    from watchdog.observers import Observer
    from watchdog.events import PatternMatchingEventHandler
except ModuleNotFoundError:
    install("watchdog")
    from watchdog.observers import Observer
    from watchdog.events import PatternMatchingEventHandler
    
import time

#Made with tutortial from https://thepythoncorner.com/posts/2019-01-13-how-to-create-a-watchdog-in-python-to-look-for-filesystem-changes/

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

def on_modified(event):
    print(f"new score data has been detected in your osu directory: {event.src_path}, refreshing")
    urllib.request.urlopen(f"http://gdcheerios.com/refresh/{info.osu_username}")

my_event_handler.on_modified = on_modified

path = f"{info.osu_path}/data/r"
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)

my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()