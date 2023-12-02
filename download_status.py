import os
import requests
import secrets

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