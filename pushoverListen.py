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

    # Convert string (containing JSON object) to Python Object
    messageObject = json.loads(str(body))
    return messageObject

# ---------------------------------------------------------------------------------
# Convert a Dictionary of messages over to one big string (within newlines between messages)

def MessagesToString(allMessageObject):

    StringList = [];

    # There's a key in the Python object called "messages", within there's an array of messages
    for singleMessageObj in allMessageObject['messages']:
        StringList.append("Id=%d: message=%s title=%s" % (singleMessageObj['id'], singleMessageObj['message'], singleMessageObj['title']));
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

    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()
    
    body = buffer.getvalue()

# ---------------------------------------------------------------------------------
# ---------------------- Main -----------------------------------------------------
# ---------------------------------------------------------------------------------

# Get the data structure containing all the HTTP GET params
import cgi
form = cgi.FieldStorage()
verbose = False
log = False

import getpass
import argparse
 
# Parse command-line arguments (Create ArgumentParser object)
# By default, program name (shown in 'help' function) will be the same as the name of this file
# Program name either comes from sys.argv[0] (invocation of this program) or from prog= argument to ArgumentParser
# epilog= argument will be display last in help usage (strips out newlines)
parser = argparse.ArgumentParser(description='Listens to PushOver for new messages')
 
# Test for verbose
parser.add_argument('-v', dest='verbose', action='store_true', help='verbose_mode')
 
# Get the object returned by parse_args
args = parser.parse_args()
verbose = args.verbose;
 
# Prints command-line params
vprint(" ")
vprint("Command Line Parameters")
vprint("---------------------------")
vprint("verbose = %s" % args.verbose)
vprint(" ")
 
# Read config params from the config file
configDict = getParamsFromFile(configFile, ConfigSection)

# Find latest message
allMessageObject = getPushoverMessages(configDict)
lastIndex=len(allMessageObject['messages'])

# If there are pre-existing messages, print helpful info, then delete them
if (lastIndex > 0):
    vprint("Number of pre-existing messages = %d\n" % lastIndex)
    vprint (MessagesToString(allMessageObject));
    lastMessageID = allMessageObject['messages'][lastIndex-1]['id']
    vprint("Last message ID = %s\n" % lastMessageID)
    vprint ("Deleting all pre-existing messages\n")

    # Delete all messages
    deleteAllMessages(configDict)

    # Print messages to be sure all got deleted
    allMessageObject = getPushoverMessages(configDict)
    vprint (MessagesToString(allMessageObject));
    lastIndex=len(allMessageObject['messages'])
    vprint("Number of messages = %d\n" % lastIndex)

# OK, we've cleared the PushOver message queue
# Create a websocket to listen for new messages
import websocket
import thread
import time
import logging

# causes better errors to be printed from websocket
logging.basicConfig();

def on_message(ws, message):
    vprint ("Recived tickler: %s\n" % message);
    if (message == "!"):
        vprint ("We received a new message, retrieving it...\n")
        messageObject = getPushoverMessages(configDict)
        sys.stdout.write(MessagesToString(messageObject));
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
    # Uncomment next line to enable verbose debugging on websocket connection
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://client.pushover.net/push",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

# --------------------------------------- End --------------------------------------------------------
