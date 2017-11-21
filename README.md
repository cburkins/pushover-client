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

Installation & Configuration
==============================

Step 0 (create your Pushover account)
--------
1. Create your account at the Pushover website

Step 1 (install iPhone App)
--------
1. Install the iPhone App
2. Login to your account 
3. <There might be another step, but I did it back in 2012, so I can't remember the exact details.  Feel free to open an issue if you've got more detail here>

Step 2 (email notification to your iPhone)
--------
1. Go to your Pushover dashboard, and find your email address (which delivers to all your devices)
2. Send a short email to that address
3. Enjoy the sweet sound of the notification (and message) on your iPhone
4. Didnt' work ? Keep working at it, no sense going on until you figured this out

Step 3 (CLI message from Linux CLI to your iPhone)
--------
1. Login to your favorite Linux box
2. Go to the Pushover website (https://pushover.net)
2. At the top right, in big giant letters is "Your User Key". SAVE THIS (needed below, called "user")
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

Step 4a (Get your Secret key)
-----------------------------
1. This next part needs to be done once, and **can only be done via the command-line**
1. Login to a Linux box
1. Request your secret token
   * curl --form-string "email=[your-email-address]" --form-string "password=[pushover-acct-password]" https://api.pushover.net/1/users/login.json
```
{"status":1,"id":"<your-user-key>","secret":"<secret-token>","request":"<request-id>"}
```

Step 4b (Create your Desktop app and get your device_id)
-------------------------------------
1. Again, as the same Linux CLI
2. Create your Desktop app, and get your secret key
   * <code>curl --form-string "secret=[secret-token]" --form-string "name=[app-name]" --form-string "os=O" https://api.pushover.net/1/devices.json</code>
```
{"id":"<device-id>","status":1,"request":"<request-id>"}
```

OK, whew !  You should now have these two items:
1. Secret Key (we'll call this "secet")
2. Device ID (we'll call this "device_id")

Step 4c (configure your CLI listener)
-----------------------------
1. Log in to your linux box again
2. Go back to same directory where you cloned this repository
3. Create a file called "pushoverListen.config" in the following format (without the "<>" brackets, of course)
```
[pushoverListen]
secret=<secret>
device_id=<device-id>
```

Step 4d (startup your listen - WARNING, THIS DELETES ALL YOUR OUTSTANDING MESSAGES)
--------
1. That last part isn't really all that scary, just wanted you to know.
2. It's just how the API works, no way around it
3. OK, ready ?
4. Run this command "./pushoverListener.py -v"
5. It won't return your command-prompt, it's running in the shell foreground
6. Every 30s or so, you should see "Received tickler"

Step 4e (send a test message)
--------
1. You can send that test message however you want (easiest way is the website, I guess)
2. That command-line listener in the previous step should have woken up, and showed you the message
3. If you don't get the message with 5s, it's not coming

