#!/usr/bin/env python3

import requests
import urllib.parse
import config
from datetime import datetime
from main import print_timestamped_message

def import_downloads(parent_directory):
    """
    Imports the downloads using the betanin API.
    """
    url = f"{config.BETANIN_URL}/api/torrents/"
    headers = {"X-API-Key": config.BETANIN_API_KEY, "Content-Type": "application/x-www-form-urlencoded"}
    data = {"name": urllib.parse.quote(parent_directory), "path": config.DOWNLOADS_DIRECTORY}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print_timestamped_message(f"Yay! I've successfully imported the downloads from {parent_directory}.")
    else:
        print_timestamped_message(f"Oops! I couldn't import the downloads from {parent_directory}.")

def get_download_outcome(download_id):
    """
    Gets the outcome of the download from the betanin API.
    """
    url = f"{config.BETANIN_URL}/api/torrents/{download_id}/console/stdout"
    headers = {"X-API-Key": config.BETANIN_API_KEY, "accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    for item in data:
        print_timestamped_message(f"Here's the stdout from {dldn}: {item['data']}")

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

    if download_status == "COMPLETED":
        print_timestamped_message("Yay! Import complete.")
        return False
    else:
        print_timestamped_message(f"Uh-oh! I think betanin needs your input for {download_name}, please check {config.BETANIN_URL}.")
        get_download_outcome(download_id)
        return True
