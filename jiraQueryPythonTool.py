
# By Justin Hagerty
# 2/3/2020

from jira import JIRA
import requests
import json
import time
import configparser
import os
import sys
import logging
import traceback
from datetime import datetime


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
        self.result = new_result



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
    ticketStorageFile = "./tickets.txt"
    # - log settings
    logFile = configurations["log"]["logfile"]
    # - filter settings

    # Jira filters data structure:

    # filters[<name of filter>]["string"] = <filter string>
    # filters[<name of filter>]["result"] = <result of JQL search>


    filters = dict()
    ### TEST:
    filters["TEST"] = query(configurations["filters"]["testfilter"], dict())
    ### UFO TOP:
    #filters["UFO TOP"]["string"] = configurations["filters"]["filter01"]
    ### UFO BOTTOM:
    #filters["UFO BOTTOM"]["string"] = configurations["filters"]["filter02"]
    ### UFO BOTTOM After 3PM:
    #filters["UFO BOTTOM 3PM"]["string"] = configurations["filters"]["filter03"]
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
print(str(jiraAPIURL))
print("TEST")

jira = JIRA(options={'server' : str(jiraAPIURL)} ,basic_auth=(jiraUser, jiraPass))


### Jira handling tools:
# - write to ticket file
def writeToTicketFile(ticketsDict):
    f = open(ticketStorageFile, "r+")
    f.truncate()
    f.write(json.dumps(ticketsDict))
    f.close()

# - get previous tickets from file
def getPreviousTickets():
    try:
        f = open(ticketStorageFile, "r+")
        jiraTicketsFromFile = json.loads(f.read())
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

### While Cycle Counter:
cycleCounter = 0

### run the main loop for the program:

filters["TEST"].setResult(jiraTicketsFromJQL(filters["TEST"].getString()))

print(filters["TEST"].getResult())

"""
while(True):
    # add to the cycle counter
    cycleCounter = cycleCounter + 1

    # run through the JQL filters and identify them
    for keys, value in filters.items():
        filters[keys]["result"] = jiraTicketsFromJQL(filters[keys]["string"])
        log_date(filters[keys]["string"])
        log_date(filters[keys]["result"])

    jiraTicketsFromFile = getPreviousTickets()
    for keys, value in jiraTicketsFromFile.items():
        log_date("Processing: " + keys)
        for ticketNum, ticket in jiraTicketsFromFile[keys]["result"]:
            del filters[keys]["result"][ticketNum]
            log_date("Deleting :" + keys + ", " + ticketNum)
"""

















### TODO:
# rotate logs after 1 day always keeping a buffer of 1 day.
# query jira
# change it after 3pm

# add that info to the UFO
# save to ticket tracking file
# query