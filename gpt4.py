import os
import requests
import time
import urllib.parse
from collections import deque
import secrets
from datetime import datetime

def print_timestamped_message(message):
    """
    Prints a message with a timestamp.
    """
    print(f"{datetime.now()}: {message}")

def get_subdirectories(directory):
    """
    Returns a set of subdirectories in the given directory.
    """
    return set(folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder)))

def get_download_status():
    """
    Returns the download status from the slskd API.
    """
    url = f"{secrets.SLSKD_URL}/api/v0/transfers/downloads"
    params = {'includeRemoved': 'false'}
    headers = {'X-API-Key': secrets.SLSKD_API_KEY}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return data

def all_downloads_completed(data):
    """
    Checks if all downloads are completed.
    """
    for user in data:
        for directory in user['directories']:
            for file in directory['files']:
                if file['state'] != 'Completed, Succeeded':
                    return False
    return True

def import_downloads(parent_directory):
    """
    Imports the downloads using the betanin API.
    """
    url = f"{secrets.BETANIN_URL}/api/torrents/"
    headers = {"X-API-Key": secrets.BETANIN_API_KEY, "Content-Type": "application/x-www-form-urlencoded"}
    data = {"name": urllib.parse.quote(parent_directory), "path": secrets.DOWNLOADS_DIRECTORY}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print_timestamped_message(f"Yay! I've successfully imported the downloads from {parent_directory}.")
    else:
        print_timestamped_message(f"Oops! I couldn't import the downloads from {parent_directory}.")

def get_download_outcome(download_id):
    """
    Gets the outcome of the download from the betanin API.
    """
    url = f"{secrets.BETANIN_URL}/api/torrents/{download_id}/console/stdout"
    headers = {"X-API-Key": secrets.BETANIN_API_KEY, "accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    for item in data:
        print_timestamped_message(f"Here's some data from the download: {item['data']}")

def check_manual_intervention_needed():
    """
    Checks if manual intervention is needed by checking the status of the download.
    """
    url = f"{secrets.BETANIN_URL}/api/torrents/"
    headers = {"X-API-Key": secrets.BETANIN_API_KEY, "accept": "application/json"}
    params = {"page": 1, "per_page": 1}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    download_id = data['torrents'][0]['id']
    download_status = data['torrents'][0]['status']

    if download_status == "COMPLETED":
        print_timestamped_message("No manual intervention needed. Everything's going smoothly!")
        return False
    else:
        print_timestamped_message("Uh-oh, it looks like this download needs some manual intervention.")
        get_download_outcome(download_id)
        return True

# Get the initial set of subdirectories
previous_subdirectories = get_subdirectories(secrets.DOWNLOADS_DIRECTORY)
subdirectory_queue = deque()

while True:
    # Get the current set of subdirectories
    current_subdirectories = get_subdirectories(secrets.DOWNLOADS_DIRECTORY)
    # Find the new subdirectories
    new_subdirectories = current_subdirectories - previous_subdirectories
    # Add the new subdirectories to the queue
    for subdirectory in new_subdirectories:
        print_timestamped_message(f"Hey, I found a new subdirectory: {subdirectory}. I'll add it to my to-do list.")
        subdirectory_queue.append(subdirectory)

    # If there are subdirectories in the queue and all downloads are completed
    if subdirectory_queue and all_downloads_completed(get_download_status()):
        # Process the next subdirectory in the queue
        subdirectory = subdirectory_queue.popleft()
        print_timestamped_message(f"Alright, let's get to work on {subdirectory}...")
        import_downloads(subdirectory)
        if check_manual_intervention_needed():
            print_timestamped_message(f"Manual intervention needed for {subdirectory}. I'll have to skip this one for now.")
        else:
            print_timestamped_message(f"Successfully processed {subdirectory}. On to the next one!")

    # Update the set of previous subdirectories
    previous_subdirectories = current_subdirectories
    # Wait for 5 seconds before checking again
    time.sleep(5)