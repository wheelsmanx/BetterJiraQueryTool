
# By Justin Hagerty
# Start: 2/3/2020
# JIRA documentation https://pypi.org/project/jira/


# these are disabled completely right now to ensure that if we accidentally reach out to jira it does not cause an issue
# from jira import JIRA
# import requests
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

# Some constants:
# - UFO
ufo_all_green = "/api?top_init&top=0|15|00ff00&top_morph=1000|5&bottom_init&bottom=0|15|00ff00&bottom_morph=1000|5"
ufo_init = "/api?top_init&bottom_init"


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
# - debug flags and configurations
# To turn on the ufo you need to set this to true - to turn off update of the ufo you need to set it to false.
ufo = True
# if debug hour is anything but false or of type None it will set a fake time
debug_hour = 13


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

    ### UFO COLOR CONFIG:
    ### should be able to select any color set in the config by name
    # Example: configurations["color"]["upperred"] would be 37609
    # remember config._sections returns all lower case so the colors must be referenced as all lower case chars
    colors = configurations["color"]
    ### UFO IP CONFIG:

    all_ufo = configurations["ufo"]["ufo_url"]

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
#Note: these will be used in conjunction with the dict colors[] which is set up at the top

def setUFOBOTTOM(color):
    log_date(f"BOTTOM OF UFO SET TO : {color}")
    send_UFO_Query("/api?bottom_init=1&bottom=15|15|" + code);
    return True

def setUFOTOP(color):
    log_date(f"TOP OF UFO SET TO : {color}")
    send_UFO_Query("/api?top_init=1&top=15|15|" + code)
    return True

def send_UFO_Query(query):
    log_date("Sending Query to all listed UFOs.")
    for x in all_ufo.split(','):
        log_date(f"Sending query of {query} to ufo:  https://{x} .... ")
        query_url = "http://" + str(x) + str(query)
        #r = requests.get(url=query_url)
    return True



### Slack bot handling:
def sendSlackBot():
    # TODO
    # add the script from "jiraQueryTool" that sends this to the RTC bot. https://github.com/wheelsmanx/jiraQueryAPITool/blob/master/jiraQueryAPITool.py
    log_date(f"Sending information to slack bot. Color is : {color}")
    return True


### While Cycle Counter:
cycleCounter = 0
### need to add "blue circle" request to init/set up
# TODO
# 1.) check if this (below) works and or make it work
#send_UFO_Query(init)

while(False):
    # add to the cycle counter after it is cycled
    cycleCounter = cycleCounter + 1
    for keys, values in filters.items():
        log_date(f"Filter: {keys}")
        log_date(f"Query String : {values.getString()}")
        try:
            # the line below can be uncommented when we are ready to query jira
            # filters[keys].setResult(jiraTicketsFromJQL(values.getString()))
            # the line below is a test function that will place a fake result in the result section of the filters dictionary for this key
            filters[keys].setResult(dictionaryCheck())
        except Exception as error:
            # TODO
            # need a way for us to check the connection and if it is bad then try to connect again.
            # there are a number of different libs but we are using this one: https://pypi.org/project/jira/
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
    # TODO
    # set the variable "hour" to always get the current hour for the below logic to ensure that we switch at a certain time
    if(str(fileFilters) == str(filters)):
        print("True")
        log_date("There were no changes and nothing will happen aside from querying jira.")
        # TODO
        # dont do anything because they are the same
    else:
        print("False")
        # TODO
        # do something because they are in fact different
        if(ufo == True):
            # NOTE BEFORE WORKING: I am not sure that I like this structure -- looking for thoughts on it.
            if (str(fileFilters["UFO TOP"]) == str(filters["UFO TOP"])):
                log_date("The ufo top filters have not changed and I wont do anything.")
            else:
                log_date("The ufo top filters have changed and we will set the top ring to a color based on this filter having anything in it.")

            if(hour < 15 or hour < "15"):
                #if the hour is less than 15 which is 3pm military time then do this filter comparison.
                if (str(fileFilters["UFO BOTTOM"]) == str(filters["UFO BOTTOM"])):
                    log_date("The ufo bottom filters have not changed and I wont do anything.")
                else:
                    log_date("The ufo bottom filters have changed and we will set the bottom ring to a color based on this filter having anything in it.")
            else:
                #if the hour is greater than 15 which is 3pm military time then do this filter instead of the first comparison filter.
                if(str(filters["UFO BOTTOM 3PM"]) == str(fileFilters["UFO BOTTOM 3PM"])):
                    log_date("The ufo bottom filters have not changed and I wont do anything.")
                else:
                    log_date("The ufo bottom 3pm filters have changed and I will set the bottom color based on this filter having anything in it.")
        else:
            log_date("The ufo section is turned off and we will not update the ufo's.")
    # write the final decoded object to the file for us in next cycle:
    writeToTicketFile(codecs.encode(pickle.dumps(filters), "base64").decode())
    # print cycle number
    log_date(f"Query cycle count is:  {cycleCounter}")
    # TODO
    # Need something that pulls an int from the config and says to check the config every x cycles (tbd later) this will allow for us to update the config with out restarting the tool

    # sleep function to add waiting to it
    log_date("Waiting..... 30 Seconds")
    time.sleep(5)

