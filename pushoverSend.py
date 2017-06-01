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

def urllib2BasicAuth(configDict):

    headers = {
        'Authorization': 'Basic %s' % configDict['basictoken'],
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = urllib.urlencode({"grant_type":"refresh_token","refresh_token":configDict['refreshtoken']})
    
    # Pass data to urlopen as param, rather than adding data to URL string (triggers POST instead of GET)
    vprint ("headers for urlib2 call\n--------------------------\n%s\n\n" % headers)
    vprint ("data for urllib2 call\n------------------------\n%s\n\n" % data)
    req = urllib2.Request(refreshAPI, data, headers)

    vprint ("\nMaking the refresh API call\n---------------------------------\n")
    try:
        resp = urllib2.urlopen(req)
    except Exception, e:
        import traceback
        vprint('Generic Exception: \n------------------------\n%s\n\n' % str(traceback.format_exc()))
        vprint("Basic error object\n------------------\n%s\n\n" % str(e))
        vprint("Headers of error object\n------------------\n%s\n\n" % str(e.headers))
        vprint("Content of error object\n------------------\n%s\n\n" % str(e.read()))
    else:
        vprint(resp.read())

        # Get HTTP POST response.  It's a string, but looks like a dict.  Convert to a real dictionary
        import ast
        content=ast.literal_eval(resp.read())

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

sendPushover(configDict['token'], configDict['user'], "Hi there, Chad")

# --------------------------------------- End --------------------------------------------------------
