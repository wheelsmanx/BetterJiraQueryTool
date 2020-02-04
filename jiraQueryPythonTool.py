
# By Justin Hagerty
# Start: 2/3/2020


from jira import JIRA
import requests
import time
import configparser
import os
import logging
import traceback
from datetime import datetime
import pickle
import codecs


class query:
    queryString = ""
    queryResult = ""
    def __init__(self, queryString, queryResult):
        self.queryString = queryString
        self.queryResult = queryResult
    def getResult(self):
        return self.queryResult
    def getString(self):
        return self.queryString
    def setResult(self, new_result):
        self.queryResult = new_result
    def __repr__(self):
        return str(self.queryResult)

### Utility functons:
# - log date time stamp function
def log_date(log_text):
    try:
        # Log the error in both the log file and the console
        logging.warning(str("{:%B %d, %Y %H:%M:%S}".format(datetime.now())) + " " + log_text)
        print(str("{:%B %d, %Y %H:%M:%S}".format(datetime.now())) + " " + log_text)
    except Exception as error:
        # Log the error if we cant print the warning for some reason print and the console its self.
        logging.warning(str("{:%B %d, %Y %H:%M:%S}".format(datetime.now())) + " ERROR: " + str(error))
        print(str("{:%B %d, %Y %H:%M:%S}".format(datetime.now())) + " ERROR: " + str(error))

#print info about variable
def debugVar(inputVariable):
    print("################### DEBUG START ###################")
    print("Type is: " + str(type(inputVariable)))
    print("Output of the variable is: " + str(inputVariable))
    print("################### DEBUG   END ###################")

### Settings:
# - config settings
# Note: if this is not set it will not work unless you edit the below settings where configurations is
configFile = "./config.ini"
configurations = dict()


# - Configuration file set up
config = configparser.ConfigParser()
config.read(configFile)
try:
    configurations = config._sections
    debugVar(configurations)
except Exception as error:
    log_date(error)

try:
    # - ticket storage settings
    ticketStorageFile = os.path.dirname(os.path.realpath(__file__)) + "\\" + configurations["ticketStorage"]["ticketstoragefile"]
    # - log settings
    logFile = configurations["log"]["logfile"]
    # - filter settings
    # NOTES:
    # Jira filters data structure:
    # filters[<name of filter>]["string"] = <filter string>
    # filters[<name of filter>]["result"] = <result of JQL search>
    filters = dict()
    ### TEST:
    filters["TEST"] = query(configurations["filters"]["testfilter"], "")
    ### UFO TOP:
    filters["UFO TOP"] = query(configurations["filters"]["filter01"], "")
    ### UFO BOTTOM:
    filters["UFO BOTTOM"] = query(configurations["filters"]["filter02"], "")
    ### UFO BOTTOM After 3PM:
    filters["UFO BOTTOM 3PM"] = query(configurations["filters"]["filter03"], "")
    # - jira settings
    jiraUser = configurations["jira"]["jirauser"]
    jiraPass = configurations["jira"]["jirapass"]
    jiraBaseUrl = configurations["jira"]["jirabaseurl"]
    jiraAPIURL = configurations["jira"]["jiraapiurl"]
    # - bot settings
    botURL = configurations["bot"]["boturl"]
    # - ufo settings
    # - - add stuff
except Exception as error:
    log_date(error)
    log_date(traceback.format_exc())

### Setup:
# - Logging setup:
logging.basicConfig(filename=logFile, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

# - Jira setup:
#jira = JIRA(options={'server' : str(jiraAPIURL)} ,basic_auth=(jiraUser, jiraPass))


### Jira handling tools:
# - write to ticket file
def writeToTicketFile(ticketsDict):
    f = open(ticketStorageFile, "r+")
    f.truncate()
    f.write(str(ticketsDict))
    f.close()

# - get previous tickets from file
def getPreviousTickets():
    try:
        f = open(ticketStorageFile, "r+")
        jiraTicketsFromFile = f.read()
    except Exception as error:
        log_date(error)
        jiraTicketsFromFile = None
    f.close()
    return jiraTicketsFromFile

# - get tickets from jira
def jiraTicketsFromJQL(filter):
    filterSearchExec = dict()
    for issue in jira.search_issues(filter, maxResults=100):
        filterSearchExec[str(issue.key)] = str(issue.fields.summary)
    return filterSearchExec

def dictionaryCheck():
    return "test this thing here for us"


### UFO handling:
def setUFOBOTTOM(color):
    log_date(f"BOTTOM OF UFO SET TO : {color}")
    return True
def setUFOTOP(color):
    log_date(f"TOP OF UFO SET TO : {color}")
    return True

### Slack bot handling:
def sendSlackBot():
    log_date(f"Sending information to slack bot. Color is : {color}")
    return True

### While Cycle Counter:
cycleCounter = 0

while(True):
    # add to the cycle counter
    cycleCounter = cycleCounter + 1
    for keys, values in filters.items():
        log_date(f"Filter: {keys}")
        log_date(f"Query String : {values.getString()}")
        filters[keys].setResult(dictionaryCheck())
        log_date(f"Results : {values.getResult()}")
        log_date("########################################### NEW QUERY")

    try:
        # Try to load in the serialized encoded object from the file:
        fileFilters = pickle.loads(codecs.decode(getPreviousTickets().encode(), "base64"))
    except Exception as error:
        log_date(error)
        log_date(traceback.format_exc())
        log_date("File is likely to be empty on first run. This is not a cause for alarm.")
        fileFilters = None

    if(str(fileFilters) == str(filters)):
        print("True")
        # TODO
        # dont do anything because they are the same
    else:
        print("False")
        # TODO
        # do something because they are in fact different
        for x in

    # write the final decoded object to the file for us in next cycle:
    writeToTicketFile(codecs.encode(pickle.dumps(filters), "base64").decode())
    # print cycle number
    log_date(f"Query cycle count is:  {cycleCounter}")
    # sleep function to add waiting to it
    log_date("Waiting..... 30 Seconds")
    time.sleep(5)

