#!/usr/bin/env python3

import os
import requests
from . import config

def get_subdirectories(directory):
    """
    Returns a set of subdirectories in the given directory.
    """
    return set(folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder)))

def get_download_status():
    """
    Returns the download status from the slskd API.
    """
    url = f"{config.SLSKD_URL}/api/v0/transfers/downloads"
    params = {'includeRemoved': 'false'}
    headers = {'X-API-Key': config.SLSKD_API_KEY}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return data

def all_downloads_completed(data):
    """
    Checks if all downloads are completed.
    """
    total_files = 0
    completed_files = 0
    for user in data:
        for directory in user['directories']:
            for file in directory['files']:
                total_files += 1
                if file['state'] == 'Completed, Succeeded':
                    completed_files += 1
    return completed_files == total_files, completed_files, total_files