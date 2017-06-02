#!/usr/bin/python

import ConfigParser
import urllib2
import urllib
import argparse

configFile = "./pushover.config"
ConfigSection = "pushover"
logFileName = "./pushover.log"

RESTAPI="https://api.fitbit.com/1/user/-/activities/steps/date/today/7d.json";
refreshAPI="https://api.fitbit.com/oauth2/token"

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
    if log:
        # Using "with" means the file will be automatically closed
        with open(logFileName, "a") as logfileObj:
            timestamp=datetime.datetime.now().strftime("%m%d%Y:%H:%M:%S")
            printString = str(print_me)
            for line in printString.splitlines():
                logfileObj.write("%s: %s\n" % (timestamp, line))
            
# ---------------------------------------------------------------------------------

def getParamsFromFile(configFile, ConfigSection):

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

def sendPushover(token, user, message):

    import pycurl
    from StringIO import StringIO
    from urllib import urlencode

    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://api.pushover.net/1/messages.json')

    post_data = {'token': token, 
                 'user': user, 
                 'message': message}

    # Form data must be provided already urlencoded.
    postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)

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
log = False
verbose = False

import getpass
import argparse
 
# Parse command-line arguments (Create ArgumentParser object)
# By default, program name (shown in 'help' function) will be the same as the name of this file
# Program name either comes from sys.argv[0] (invocation of this program) or from prog= argument to ArgumentParser
# epilog= argument will be display last in help usage (strips out newlines)
parser = argparse.ArgumentParser(description='Queries DataDomain appliances for relevant capacity statistics')
 
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

# Send PushOver message
sendPushover(configDict['token'], configDict['user'], "Hi there, Chad")

# --------------------------------------- End --------------------------------------------------------
