# BeetSeeker

Automagic beets for your Soulseek beats.

## What does BeetSeeker do?

BeetSeeker leverages the APIs of two self-hosted services:

1. [`slskd`](https://github.com/slskd/slskd): A browser-based client for Soulseek (the peer-to-peer file sharing system).
2. [`betanin`](https://github.com/sentriz/betanin): A browser-based interface for beets, designed for torrent clients and automation.

## Getting Started

BeetSeeker requires Python 3.7 or higher for `requests`. Using a virtual environment is recommended to install the Python modules:

``` 
pip install -r requirements.txt
```

Customize and rename **[example_config.py](./example_config.py)**: BeetSeeker needs to know the URLs and API keys for `slskd` and `betanin`, plus the path to the "downloads directory. 

BeetSeeker does not need direct access to any other files. Instead, BeetSeeker uses APIs, so it depends on preexisting installs of slskd and betanin, with both APIs enabled and configured. 


### slskd API considerations

The setup for slskd API keys is described [in the slskd docs](https://github.com/slskd/slskd/blob/master/docs/config.md#authentication). Please use HTTPS if possible.

### betanin API considerations

Although betanin was designed to make beets work with a torrent client, we can make it work with Soulseek using the the slskd APIs to wait until each directory request is complete. The APIs track subdirectories of the slskd "completed downloads" path -- the same path you'd configure in slskd itself, which prevents BeetSeeker from trying to process each file individually.

It is not recommended to run beets jobs in parallel. Since betanin's `config.toml` is undocumented for now, here is a minimal example:

```toml
[frontend]
username = "betanin"
password = "betanin"

[clients]
api_key = ""

[server]
num_parallel_jobs = 1

[notifications.services]

[notifications.strings]
body = "@ $time. view/use the console at http://127.0.0.1:9393/$console_path"
title = "[betanin] torrent `$name` $status"
```

## How does BeetSeeker work??

1. **Directory Monitoring**: BeetSeeker is designed to monitor slskd's "Completed Downloads" path. It continuously checks for the presence of new subdirectories. When a new subdirectory is detected, BeetSeeker queries `slskd` to retrieve the status of these recent downloads, and waits until all downloads within the new subdirectory have been completed.

2. **Download Import**: Once the latest downloads from the new directory are completed, BeetSeeker initiates the beets import process using `betanin`, and continually checks its status. This will have one of two possible results:

  - If the import succeeds, BeetSeeker's process repeats from step 1.
  - If the import process encounters an issue that requires manual intervention, BeetSeeker will skip the current subdirectory and let you know.

### Manual Intervention

When BeetSeeker requires attention, you (the human) will need to take action. 

  - Check the status of `slskd` and `betanin`. If their API's don't respond, nothing works. (Note: Both services can be configured to provide a `/swagger` interface for testing.)
  - Remove and retry any download errors, and/or
  - Manually import the downloads yourself via the betanin web interface.

BeetSeeker completely skips directories with errors, so once you have resolved the issue, you can either download something else or restart BeetSeeker to continue the monitoring and automatic import process.
