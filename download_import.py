import requests
import urllib.parse
import secrets
from datetime import datetime
from main import print_timestamped_message

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
