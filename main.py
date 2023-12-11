#!/usr/bin/env python3

import os
import time
from collections import deque
from . import config
import slskd 
import betanin

print(f"Hello! BeetSeeker is up and monitoring {config.DOWNLOADS_DIRECTORY}. I'll get started in a few seconds..\n\n")

# Get the initial set of subdirectories
previous_subdirectories = slskd.get_subdirectories(config.DOWNLOADS_DIRECTORY)
subdirectory_queue = deque()

# Check if there are any completed downloads at the start of the program
if slskd.all_downloads_completed(slskd.get_download_status()):
    for subdirectory in previous_subdirectories:
        full_path = os.path.join(config.DOWNLOADS_DIRECTORY, subdirectory)
        try:
            if os.listdir(full_path):  # Check if directory is not empty
                print(f"Hey, I found a completed download: {subdirectory}. I'll add it to my to-do list.")
                subdirectory_queue.append(full_path)
        except FileNotFoundError:
            print(f"Could not access {subdirectory}. Skipping...")

while True:
    # Get the current set of subdirectories
    current_subdirectories = slskd.get_subdirectories(config.DOWNLOADS_DIRECTORY)
    # Find the new subdirectories
    new_subdirectories = current_subdirectories - previous_subdirectories
    # Add the new subdirectories to the queue
    for subdirectory in new_subdirectories:
        full_path = os.path.join(config.DOWNLOADS_DIRECTORY, subdirectory)
        try:
            if os.listdir(full_path):  # Check if directory is not empty
                print(f"Hey, I found a new subdirectory: {subdirectory}. I'll add it to my to-do list.")
                subdirectory_queue.append(full_path)
        except FileNotFoundError:
            print(f"Could not access {subdirectory}. Skipping...")

    # If there are subdirectories in the queue and all downloads are completed
    if subdirectory_queue and slskd.all_downloads_completed(slskd.get_download_status()):
        # Process the next subdirectory in the queue
        subdirectory = subdirectory_queue.popleft()
        print(f"Alright, let's get to work on {subdirectory}...")
        
        betanin.import_downloads(subdirectory)
        if betanin.check_manual_intervention_needed():
            print(f"Manual intervention needed for {subdirectory}. I'll have to skip this one for now.")
        else:
            print(f"Successfully processed {subdirectory}. On to the next one!")

    # Update the set of previous subdirectories
    previous_subdirectories = current_subdirectories
    # Wait for 5 seconds before checking again
    time.sleep(5)