# pushover-client

This is a work-in-progress.   The idea is that you receive a message that was sent via the [Pushover Service](https://pushover.net/).


Here's the gist to get going:
1. Download the Pushover client to your phone (good for trouble-shooting)
2. Send a pushover message from the Pushover website, and receive it on your phone
3. Send a pushover message from the command-line, and receive it on your phone
4. Send a message from the CLI, and receive it via a CLI websocket



The Listener (currently "pushoverListen.py") needs a configuration file called "pushoverListen.config" in the following format:

```
[pushoverListen]
secret=<super-long-secret-key>
device_id=<device-id>
```

You need to create a new client of type "Open Client Desktop".  You can purchase this license for a one-time fee of $5, go to https://pushover.net/clients/desktop

