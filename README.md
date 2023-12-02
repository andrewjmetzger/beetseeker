# slskd-betanin-connector

## Overview

The ```slskd-betanin-connector``` project is a Python-based utility designed to automate the process of monitoring a specified downloads directory for the presence of new subdirectories and importing the completed downloads. This provides a streamlined solution for managing music libraries using the ```slskd``` and ```betanin``` services.

## Functionality

The script leverages the APIs of two services:

1. ```slskd```: A peer-to-peer file sharing system. The script queries the ```slskd``` API to retrieve the status of downloads.

2. ```betanin```: A tool for managing music libraries. The script uses the ```betanin``` API to import the completed downloads.

## Setup

To utilize the script, follow these steps:

1. **Python Package Installation**: The script requires the ```requests``` and ```os``` Python packages. Install these using pip:

```bash
pip install requests os
```

2. **Secrets Configuration**: The script requires the URLs and API keys for ```slskd``` and ```betanin```, as well as the path to the downloads directory. These can be provided in a ```secrets.py``` file or as environment variables. If using a ```secrets.py``` file, ensure it is added to the ```.gitignore``` file to prevent it from being committed to the GitHub repository.

3. **Script Execution**: Run the script using Python:

```bash
python main.py
```

## Operation

The operation of the ```slskd-betanin-connector``` script can be broken down into the following steps:

1. **Directory Monitoring**: Upon execution, the script begins monitoring the specified downloads directory. It continuously checks for the presence of new subdirectories.

2. **New Subdirectory Detection**: When a new subdirectory is detected, the script logs a timestamped message to the console indicating the detection of the new subdirectory.

3. **Download Status Check**: The script then queries the ```slskd``` API to retrieve the status of downloads. It checks if all downloads within the new subdirectory have been completed.

4. **Download Import**: If all downloads are completed, the script initiates the import process using the ```betanin``` API. A timestamped message indicating the initiation of the import process is logged to the console.

5. **Import Status Check**: After initiating the import, the script checks the status of the import process. If the import is successful, a timestamped message indicating the successful import is logged to the console.

6. **Manual Intervention Check**: If the import process encounters an issue that requires manual intervention, the script logs a timestamped message indicating the need for manual intervention. In this case, the script will skip the current subdirectory and continue monitoring the downloads directory for new subdirectories.

7. **Manual Intervention**: When the script logs a message indicating the need for manual intervention, you (the human) will need to take action. This may involve checking the status of the ```slskd``` and ```betanin``` services, resolving any issues with the downloads or the import process, or manually importing the downloads. Once you have resolved the issue, you can restart the script to continue the monitoring and import process.

8. **Continued Monitoring**: After processing a subdirectory (either by successfully importing the downloads or skipping the subdirectory due to the need for manual intervention), the script continues monitoring the downloads directory for new subdirectories. The process then repeats from step 1.

The ```slskd-betanin-connector``` script is designed to automate the process of monitoring and importing downloads, but it also provides detailed logging to help you track its progress and intervene when necessary.