# BeetSeeker

Automagic beets for Soulseek.

## What does BeetSeeker do?

BeetSeeker leverages the APIs of two services:

1. `slskd`: A browser-based client for Soulseek (the peer-to-peer file sharing system).
2. `betanin`: A browser-based interface for beets, designed to interface with a torrent client for automagic music library management.

## Getting Started

This script depends on preexisting installs of slskd and betanin, with both APIs enabled and configured.

Customize and rename **[example_secrets.py](./example_secrets.py)**. BeetSeeker needs to know the URLs and API keys for `slskd` and `betanin`, plus the path to the downloads directory. BeetSeeker does not need direct access to any files.

### slskd considerations

You must configure and enable the slskd API. The setup for API keys is described [in the slskd docs](https://github.com/slskd/slskd/blob/master/docs/config.md#authentication). Please use HTTPS if possible.

### betanin considerations

Although betanin was designed to make beets work with a torrent client, where everything is fully downloaded, we can make it work with Soulseek too, using the the slskd APIs to wait until each request is complete. This tracks subdirectories of a hypothetical "completed downloads" path, the same path you'd configure in slskd itself. Tracking the sub-directory for each download operation should allow you to download stuff with multiple child subdirectories (like a discography or multi-disc album) with no issues.

It is not recommended to run `beet import`` jobs in parallel. Since betanin's `config.toml` is undocumented for now, here is a minimal example:

```toml
[frontend]
username = "betanin"
password = "betanin"

[clients]
api_key = "<generate a random 32-bit key>"

[server]
num_parallel_jobs = 1
```

## How does BeetSeeker work??

1. **Directory Monitoring**: BeetSeeker is designed to monitor slskd's "Completed Downloads" path. It continuously checks for the presence of new subdirectories. When a new subdirectory is detected, BeetSeeker queries `slskd` to retrieve the status of these recent downloads, and waits until all downloads within the new subdirectory have been completed.

2. **Download Import**: Once the latest downloads from the new directory are completed, BeetSeeker initiates the beets import process using `betanin`, and continually checks its status. This will have one of two possible results:

  - If the import succeeds, BeetSeeker's process repeats from step 1.
  - If the import process encounters an issue that requires manual intervention, BeetSeeker will skip the current subdirectory and let you know.


### Manual Intervention

When BeetSeeker logs a message indicating the need for manual intervention, you (the human) will need to take action. 

  - Check the status of `slskd` and `betanin`. If their API's don't respond, nothing works. (Note: Both services provide a `/swagger` interface for testing.)
  - Remove and retry any download errors, and/or
  - Manually import the downloads yourself via the betanin web interface.

BeetSeeker completely skips directories with errors, so once you have resolved the issue, you can either download something else or restart BeetSeeker to continue the monitoring and automatic import process.