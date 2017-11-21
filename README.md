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
1. Login to your favorite Linux box
2. Go to the Pushover website (https://pushover.net)
2. At the top right, in big giant letter is "Your User Key". SAVE THIS (needed below, called "user")
2. Scroll down to "Your Applications"
2. Click on "Create an Application/API Token" (or click here: https://pushover.net/apps/build)
  * Name: test01
  * Type: Other
  * Description: test cli pushover client
  * URL: <blank>
  * Icon: <none>
  * <Click Create>
2. Go back to your dashboard, click on  your new application
2. In big giant letters, will tell you your new "API Token/Key".  SAVE THIS (needed below, called "token")
2. 
2. Clone this repository
3. Create a file called "pushover.config" (use "user" and "token" from above)
```
[pushover]
token = apadskSuperFakeTokendkgasd
user = aakdgThisisaFakeUseradksVaS
```
4. Run this command
```
./pushoverSend.py -v --message "Now is the time for all good men to come to the aid of their country"
```
5. Enjoy the sound of notification on your phone


The Listener (currently "pushoverListen.py") needs a configuration file called "pushoverListen.config" in the following format:

```
[pushoverListen]
secret=<super-long-secret-key>
device_id=<device-id>
```

You need to create a new client of type "Open Client Desktop".  You can purchase this license for a one-time fee of $5, go to https://pushover.net/clients/desktop

