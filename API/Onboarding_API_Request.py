############################################################################
#
# Purpose:
#   Pulls Company information from the RMIS API. Works by inputting the dotNumber
#   followed by the userID and password into the command line. From this, the
#   dotNumber, userID, and password will be concat with the RMIS API url and send
#   and http request and the response will be in the form of an XML document.
#   The document will be saved into a temp file to be parsed using BeautifulSoup
#   and dumped into the appropriate File(s).   
#
#
# Extra Info:
#   Saved Company info will be saved at '../Data/temp/xml/'
#   Using XML element tree to parse the XML
#   You need prettytable to print
#
# pip installs:
#   pip install prettytable
#
# Run:
#   python ./API_Request.py 'userID' 'password' 'dot number'
#
# Ex: 
#   python ./SAFER_Scraper.py userID425 password123 123456
###############################################################################
def main():
    # Get the API Authentication Information
    clientID, password = Get_API_Auth_Info()
    
    # Get the Dot Number that will be looked up
    dotNumber = Get_DOT_Number()
    
    # Append the given Information to the API URL
    apiRequestURL = Get_Request_URL(clientID, password, dotNumber)
    
    # Send a Get request to the API URL and retrieve the companies info in XML
    requestXmlText = Retrieve_API_Info(apiRequestURL)
    print(apiRequestURL)
    
    # Dump the retrieved company information to XML
    Dump_To_File(dotNumber, "xml", requestXmlText)
    
    # Go through each individual child of the XML and print the tag with the value
    Traverse_XML(dotNumber, True)

###############################################################################
# returns the user ID followed by the password .. These are inputted into the
# 1st and 2nd positions of the command line
def Get_API_Auth_Info():
    import sys
    return sys.argv[1], sys.argv[2]

###############################################################################
# Returns the inputted DotNumber .. This will be the third command line argument
def Get_DOT_Number():
    import sys
    return sys.argv[3]

###############################################################################
# concacts the API URL with the dotNumber, clientID, and password
def Get_Request_URL(clientID, password, dotNumber):
    URL = 'http://api.gormis.com/_c/std/api/ExpandedCarrierAPI.aspx?clientID=' + str(clientID)
    URL += '&pwd=' + str(password) 
    URL += '&version=7&QueryType=DOT&QueryID=' + str(dotNumber)
    return URL

###############################################################################
# requests the inputted URL to the RMIS API and returns the XML response
def Retrieve_API_Info(apiRequestURL):
    import requests
    return requests.get(apiRequestURL).text

###############################################################################
def Dump_To_File(dotNumber, fileType, text):
    #with open("../Data/temp/company_info.xml", "w") as file:
    if fileType.lower() == "xml":
        with open("../Data/temp/xml/" + str(dotNumber) + "_company_info." + fileType, "w") as file:
            file.write(text)
    
    file.close()
    
###############################################################################
def Traverse_XML(dotNumber, wantPrintTable):
    import xml.etree.ElementTree as ET
    tree = ET.parse("../Data/temp/xml/" + str(dotNumber) + "_company_info.xml")
    root = tree.getroot()
    
    # Go through each of the tags beneath root
    # <Carrier> <Coverages>, etc.
    parsedParent = []
    headers = []
    for parent in root:
        headers.append(parent.tag)
        parsedChild = []
        tags = []

        # Want to update this later so it looks better, less repeating code        
        for levelOneChild in parent:
            for levelTwoChild in levelOneChild:
                for levelThreeChild in levelTwoChild:                                                
                    parsedData = levelThreeChild.text
                    if parsedData is None: parsedData = "N/A"
                    if Validate_Chars(parsedData): 
                        parsedChild.append(parsedData)
                        tags.append(levelThreeChild.tag)
                
                parsedData = levelTwoChild.text
                if parsedData is None: parsedData = "N/A"
                if Validate_Chars(parsedData): 
                    parsedChild.append(parsedData)
                    tags.append(levelTwoChild.tag)
            
            parsedData = levelOneChild.text
            if parsedData is None: parsedData = "N/A"
            if Validate_Chars(parsedData): 
                parsedChild.append(parsedData)
                tags.append(levelOneChild.tag)

        parsedParent.append(parsedChild)
        if wantPrintTable: Print_Table(parent.tag, tags, parsedChild)

###############################################################################
def Print_Table(tableHeader, tags, data):
    from prettytable import PrettyTable, DEFAULT
    table = PrettyTable([tableHeader, "Data"])
    for i in range (0, len(tags)):
        if (tags[i] == 'CoverageDescription' or tags[i] == 'CompanyName'): table.add_row(['',''])
        table.add_row([tags[i], data[i]])
        
    table.set_style(DEFAULT)
    table.align = "l"
    print(table, end="\n\n\n")
    
###############################################################################
# Validates that the chars in the string are within valid ascii range
# Used because the end tags will create a new row without any valid text associated
def Validate_Chars(string):
    # Check that the parsed data has all valid ascii alphanumeric chars
    for i in range (0, len(string)):
        if (ord(string[i]) == 10):
            return False
    return True

###############################################################################

main()