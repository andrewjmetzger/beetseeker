#!/usr/bin/env python3

import os
import requests
import config
from slskd import all_downloads_completed, get_download_status

def import_downloads(parent_directory):
    """
    Imports the downloads using the betanin API.
    """
    url = f"{config.BETANIN_URL}/api/torrents/"
    headers = {"X-API-Key": config.BETANIN_API_KEY, "Content-Type": "application/x-www-form-urlencoded"}

    # Extract the subdirectory name from the parent_directory
    subdirectory_name = os.path.basename(parent_directory)
    # Append the subdirectory name to the BETANIN_IMPORT_DIRECTORY
    betanin_path = f"{config.BETANIN_IMPORT_DIRECTORY}/{subdirectory_name}"
    print(f"Betanin path: {betanin_path}")

    download_data = get_download_status()
    all_completed, completed_files, total_files = all_downloads_completed(download_data)
    if not all_completed:
        print(f"{completed_files}/{total_files} files downloaded. Waiting for all downloads to complete.")
        return

    data = {"both": betanin_path}
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print(f"Yay! I've successfully imported the downloads.")
    else:
        print(f"Oops! I couldn't import the downloads.")

def get_download_outcome(download_id):
    """
    Gets the outcome of the download from the betanin API.
    """
    url = f"{config.BETANIN_URL}/api/torrents/{download_id}/console/stdout"
    headers = {"X-API-Key": config.BETANIN_API_KEY, "accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    for item in data:
        print(f"Here's the stdout: {item['data']}")

def check_manual_intervention_needed():
    """
    Checks if manual intervention in betanin is needed.
    """
    url = f"{config.BETANIN_URL}/api/torrents/"
    headers = {"X-API-Key": config.BETANIN_API_KEY, "accept": "application/json"}
    params = {"page": 1, "per_page": 1}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    download_id = data['torrents'][0]['id']
    download_status = data['torrents'][0]['status']
    download_name = data['torrents'][0]['name']

    if download_status != "COMPLETED":
        print(f"Uh-oh! I think betanin needs your input, please check {config.BETANIN_URL}.")
        get_download_outcome(download_id)
        return True
    return False
