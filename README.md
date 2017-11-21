# pushover-client

This is a work-in-progress.   The idea is that you receive a message that was sent via the [Pushover Service](https://pushover.net/).


Here's the gist to get going:
---------------------------------
1. Download the Pushover client to your phone (good for trouble-shooting)
2. Send a pushover message from the Pushover website, and receive it on your phone
3. Send a pushover message from the command-line, and receive it on your phone
4. Send a message from the CLI, and receive it via a CLI websocket

Requirements: 
--------------
A. Install the iPhone app on your phone (might cost $5 ?)
B. Purchase the Open Client Desktop license (costs $5)

Step 0
========
1. Create your account at the Pushover website

Step 1 (install iPhone App)
=========
1. Install the iPhone App
2. Login to your account 
3. <There might be another step, but I did it back in 2012, so I can't remember the exact details.  Feel free to open an issue if you've got more detail here>

Step 2 (email notification to your iPhone)
=========
1. Go to your Pushover dashboard, and find your email address (which delivers to all your devices)
2. Send a short email to that address
3. Enjoy the sweet sound of the notification (and message) on your Iphone
4. Didnt' work ? Keep working at it, no sense going on until you figure this out

Step 3 (CLI message from Windows to your iPhone)
=============



The Listener (currently "pushoverListen.py") needs a configuration file called "pushoverListen.config" in the following format:

```
[pushoverListen]
secret=<super-long-secret-key>
device_id=<device-id>
```

You need to create a new client of type "Open Client Desktop".  You can purchase this license for a one-time fee of $5, go to https://pushover.net/clients/desktop

