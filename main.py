#!/usr/bin/env python3

import time
from collections import deque
import config
import download_status
import download_import
from datetime import datetime

## main.py
def print_timestamped_message(message):
    """
    Prints a message with a timestamp.
    """
    print(f"{datetime.now()}: {message}")

# Get the initial set of subdirectories
previous_subdirectories = download_status.get_subdirectories(config.DOWNLOADS_DIRECTORY)
subdirectory_queue = deque()

while True:
    # Get the current set of subdirectories
    current_subdirectories = download_status.get_subdirectories(config.DOWNLOADS_DIRECTORY)
    # Find the new subdirectories
    new_subdirectories = current_subdirectories - previous_subdirectories
    # Add the new subdirectories to the queue
    for subdirectory in new_subdirectories:
        print_timestamped_message(f"Hey, I found a new subdirectory: {subdirectory}. I'll add it to my to-do list.")
        subdirectory_queue.append(subdirectory)

    # If there are subdirectories in the queue and all downloads are completed
    if subdirectory_queue and download_status.all_downloads_completed(download_status.get_download_status()):
        # Process the next subdirectory in the queue
        subdirectory = subdirectory_queue.popleft()
        print_timestamped_message(f"Alright, let's get to work on {subdirectory}...")
        download_import.import_downloads(subdirectory)
        if download_import.check_manual_intervention_needed():
            print_timestamped_message(f"Manual intervention needed for {subdirectory}. I'll have to skip this one for now.")
        else:
            print_timestamped_message(f"Successfully processed {subdirectory}. On to the next one!")

    # Update the set of previous subdirectories
    previous_subdirectories = current_subdirectories
    # Wait for 5 seconds before checking again
    time.sleep(5)