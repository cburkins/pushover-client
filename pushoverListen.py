#!/usr/bin/python

import ConfigParser
import urllib2
import urllib
import argparse
import sys

configFile = "./pushoverListen.config"
ConfigSection = "pushoverListen"
logFileName = "./pushoverListen.log"

# ---------------------------------------------------------------------------------

#  Input: The string to be printed
#  Descr: Prints the string, but only if the user has set the verbose flag via command
#         line
# Output: None

def vprint(print_me):

    import datetime
    import sys

    if verbose:
        # stdout.write means user must send line return within the string
        sys.stdout.write("%s" % print_me)
        sys.stdout.flush()
    if log:
        # Using "with" means the file will be automatically closed
        with open(logFileName, "a") as logfileObj:
            timestamp=datetime.datetime.now().strftime("%m%d%Y:%H:%M:%S")
            printString = str(print_me)
            for line in printString.splitlines():
                logfileObj.write("%s: %s\n" % (timestamp, line))
            
# ---------------------------------------------------------------------------------

def getParamsFromFile(configFile, ConfigSection):

    # Test to make sure file exists
    import os.path;
    if (not os.path.isfile(configFile)):
        print("Error: Config file '%s' doesn't exist" % configFile);
        exit();
    

    # Read in the configuration file 
    Config = ConfigParser.ConfigParser()
    Config.read(configFile)
    
    # Create empty dictionary
    configDict = dict();

    # Read in all options from the config file
    items = Config.items(ConfigSection)
    for (option,value) in items:
        configDict[option] = value

    vprint("Keys read in from Config File(%s)\n" % configFile);
    for key in configDict.keys():
        vprint("   Key=%s Value=%s\n" % (key,configDict[key]))
    vprint("\n")

    return (configDict)

# ---------------------------------------------------------------------------------

def backupFile (fileName):

    import os
    import shutil
    import datetime
    FilePath = fileName
    modifiedTime = os.path.getmtime(FilePath) 
    
    timeStamp =  datetime.datetime.fromtimestamp(modifiedTime).strftime("%b-%d-%y-%H:%M:%S")
    timeStamp =  datetime.datetime.now().strftime("%b-%d-%y-%H:%M:%S")

    newFilePath = "backups/"+FilePath+"_"+timeStamp
    shutil.copyfile(FilePath,newFilePath)

# ---------------------------------------------------------------------------------

def writeParamsToFile(configFile, ConfigSection, configDict):

    #print ("\nWriting new config file\n")
    with open(configFile, 'w') as configFile:
        conf = ConfigParser.ConfigParser()
        conf.add_section("fitbit");
        for key,value in configDict.items():
            conf.set('fitbit', key, value)
            #print("New option: key=" + key + "  value=" + value)
        conf.write(configFile)
    
# ---------------------------------------------------------------------------------
#
# Retrieves all outstanding messages from your PushOver queue
# There might be many of them
#

def getPushoverMessages(configDict):

    import pycurl
    import json
    from StringIO import StringIO
    from urllib import urlencode

    # Construct the full command-line for curl call
    buffer = StringIO()
    URL="https://api.pushover.net/1/messages.json"
    secret = configDict['secret']
    device_id = configDict['device_id']
    fullURL="%s?secret=%s&device_id=%s" % (URL, secret, device_id)
    vprint ("fullURL = %s\n" % fullURL);

    # Setup and execute the curl call (defined above)
    c = pycurl.Curl()
    c.setopt(c.URL, fullURL)
    #c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()
    
    # Extract message dictionary from returned buffer
    body = buffer.getvalue()
    messageDict = json.loads(str(body))
    return messageDict

# ---------------------------------------------------------------------------------
# Convert a Dictionary of messages over to one big string (within newlines between messages)
#

def MessagesToString(messageDict):

    StringList = [];
    for messageObj in messageDict['messages']:
        StringList.append("Id=%d: %s" % (messageObj['id'], messageObj['message']));
    # Join the list together into one big string separated by newlines
    return("\n".join(StringList) + "\n");

    
# ---------------------------------------------------------------------------------

def deleteAllMessages(configDict):

    messageDict = getPushoverMessages(configDict)
    lastMessageID = messageDict['messages'][lastIndex-1]['id']
    deleteMessagesByID(configDict, lastMessageID)


# ---------------------------------------------------------------------------------

def deleteMessagesByID(configDict, message_id):

    # Needs to be a POST request
    import pycurl
    import json
    from StringIO import StringIO
    from urllib import urlencode

    buffer = StringIO()
    device_id = configDict['device_id'];
    secret = configDict['secret'];
    URL="https://api.pushover.net/1/devices/%s/update_highest_message.json" % device_id
    post_data = {'secret': secret, 
                 'message': message_id} 

    # Form data must be provided already urlencoded.
    postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c = pycurl.Curl()
    c.setopt(c.URL, URL)
    c.setopt(c.POSTFIELDS, postfields)

#    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()
    
    body = buffer.getvalue()

    #vprint(body+"\n\n")

# ---------------------------------------------------------------------------------

def sendPushover(token, user, message):

    import pycurl
    from StringIO import StringIO
    from urllib import urlencode

    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://api.pushover.net/1/messages.json')

    post_data = {'token': token, 
                 'user': user, 
                 'device': 'iPhone6',
                 'message': message}

    # Form data must be provided already urlencoded.
    postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)

#    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()
    
    body = buffer.getvalue()
    # Body is a string in some encoding.
    # In Python 2, we can print it without knowing what the encoding is.
    print(body)

# ---------------------------------------------------------------------------------
# ---------------------- Main -----------------------------------------------------
# ---------------------------------------------------------------------------------

# Get the data structure containing all the HTTP GET params
import cgi
form = cgi.FieldStorage()
verbose = False
log = False

# Check to see if we got called via command-line or HTTP GET
if (form.keys() != []):

    # Check for verbose flag
    if (("verbose" in form) and (form['verbose'].value == 'true')):
        verbose = True
    # Check for log flag
    if (("log" in form) and (form['log'].value == 'true')):
        log = True

    # Print a separator
    vprint("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")

    # Looks like we got called via HTTP GET, and have at least one key
    vprint("Keys from CGI FieldStorage\n");
    for key in form.keys():
        vprint("  Key=%s  Value=%s\n" % (key, form[key].value))
    vprint("\n");

else:
    # We didn't get any keys from HTTP GET, maybe we got called via command line ?
    vprint ("Keys: No keys\n")

# Read config params from the config file
configDict = getParamsFromFile(configFile, ConfigSection)

# Find latest message
messageDict = getPushoverMessages(configDict)
lastIndex=len(messageDict['messages'])

# If there are pre-existing messages, print helpful info, then delete them
if (lastIndex > 0):
    vprint("Number of messages = %d\n" % lastIndex)
    vprint (MessagesToString(messageDict));
    lastMessageID = messageDict['messages'][lastIndex-1]['id']
    vprint("Last message ID = %s\n" % lastMessageID)
    vprint ("Deleting all messages\n")

    # Delete all messages
    deleteAllMessages(configDict)

    # Print messages to be sure all got deleted
    messageDict = getPushoverMessages(configDict)
    vprint (MessagesToString(messageDict));
    lastIndex=len(messageDict['messages'])
    vprint("Number of messages = %d\n" % lastIndex)



# OK, we've cleared the PushOver message queue
# Create a websocket to listen for new messages
import websocket
import thread
import time
import logging
logging.basicConfig();

def on_message(ws, message):
    vprint ("Recived tickler: %s" % message);
    if (message == "!"):
        vprint ("We received a new message ! Retrieving it...")
        messageDict = getPushoverMessages(configDict)
        sys.stdout.write(MessagesToString(messageDict));
        sys.stdout.flush();
        deleteAllMessages(configDict)

def on_error(ws, error):
    print "### websocket error ###"
    print error

def on_close(ws):
    print "### websockt closed ###"

def on_open(ws):
    def run(*args):
        secret = configDict['secret']
        device_id = configDict['device_id']
        loginMsg="login:%s:%s" % (device_id, secret)
        ws.send(loginMsg)
        vprint("Sent login, and now listening...\n")
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    # Enable verbose debugging on websocket connection
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://client.pushover.net/push",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

# --------------------------------------- End --------------------------------------------------------
