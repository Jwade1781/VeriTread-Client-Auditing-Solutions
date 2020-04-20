############################################################################
# Purpose:
#   The purpose of this program is to retrieve a JSON file containing a list
#   of companies that have been updated. This Program will parse the list and
#   send each company ID to the onboarding API program to be updated
#
# Extra Info:
#   JSON testing file is stored at '../Data/Test/Delta_API/Test_Json.json'
#   Companies info will be saved from the onboarding api program at 
#   '../Data/temp/xml/'
#
#
#   Timeout functionality built in to be checked every xx seconds
#   Time can be set by days, hours, etc. at Get_Timeout_Seconds()
#
#
# pip installs:
#   --
#
# Run:
#   python ./Delta_Api_Request.py 'userID' 'password'
#
# Ex: 
#   python ./Delta_Api_Request.py userID425 password123
###############################################################################
def main():
    # Get API Authentication Info
    clientID, password = Get_API_Auth_Info()
    
    # Get the required API URL
    apiRequestURL = Get_Request_URL()

    # Get the time to pass before every new post request from RMIS    
    totalTimeoutSeconds = Get_Timeout_Seconds()
    
    import time
    while True:
        # Send a Post Request to the API URL and fetch the JSON response
        responseJsonText = Retrieve_API_Info(clientID, password, apiRequestURL)
        #responseJsonText = Test_Json_Parse()
    
        # Parse the JSON Response of the list of companies that were updated
        updateCompanyList = Parse_Json(responseJsonText)
    
        # If there were companies in the retrieved list, update them using the onboarding API
        if updateCompanyList is not None:
            Update_Company_Info(clientID, password, updateCompanyList)

        time.sleep(totalTimeoutSeconds)        

###############################################################################
# returns the user ID followed by the password .. These are inputted into the
# 2nd and 3rd position of the command line
def Get_API_Auth_Info():
    from sys import argv
    return argv[1], argv[2]

###############################################################################
def Get_Request_URL():
    URL = "https://api.rmissecure.com/_c/std/api/DeltaAPI.aspx"
    return URL

###############################################################################
# requests the inputted URL to the RMIS API and returns the JSON response
# this response contains the list of IDs that have been updated since the last
# update call    
def Retrieve_API_Info(clientID, password, apiRequestURL):
    from requests import post
    from json import dumps
    payload = '{"clientID" :\"' + str(clientID) + '\", "clientPassword":\"' + str(password) + '\", "apiMode" : "FETCH", "maxRecs":"50"}'
    headers = {"Content-Type" : "application/json"}
    response = post(apiRequestURL, data=payload, headers=headers)
    print(response.text)
    return dumps(response.json()) #dumps Json to string

###############################################################################
# Test Function used for parsing .. The API is not guarenteed to have any new updated
# Data since last called. This may be used as a substitute for testing purposes
def Test_Json_Parse():
    from json import dumps, load
    PATH = "../Data/Test/"
    FILENAME = "Test_Json.json"
    with open(PATH + FILENAME) as f:
        data = load(f)
        
    return dumps(data)

###############################################################################
def Get_Timeout_Seconds():
    daysTimeOut = 0
    hoursTimeOut = 3
    minutesTimeOut = 0
    secondsTimeout = 0
    
    return (daysTimeOut * 24 * 60 * 60) + (hoursTimeOut * 60 * 60) +  (minutesTimeOut * 60) + secondsTimeout
    
###############################################################################
# Parse the given Json response for the list of company ids that have been updated
def Parse_Json(responseJsonText):
    import json
    data = json.loads(responseJsonText)
    updateCompanyList = []
    
    # Checks to see if there were errors in the API call
    if data['RMISDeltaAPI']['Header']['Result'].upper() == 'SUCCESS': 
        
        try: # parsing will fail only if ['InsdID'] does not exist meaning no updates
            for companyID in data['RMISDeltaAPI']['FETCH']['InsdID']:
                updateCompanyList.append(companyID)
                
        # there was no ['InsdID'] field in data due to no new updates     
        except BaseException:
            print("No new updates were found")
            return
        
    # Was not successful at sending request; print / log reason
    else:
        print("Error found in response:", data['RMISDeltaAPI']['Header']["Errors"]["Error"])
    
    print("List of updated Companies:", updateCompanyList)
    return updateCompanyList
        
###############################################################################
def Update_Company_Info(clientID, password, updateCompanyList):
    import subprocess
    for company in updateCompanyList:
        print("Updating", company)
        subprocess.call(['python', 'Onboarding_API_Request.py', clientID, password, company], shell=True)
    
main()
