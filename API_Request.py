############################################################################
#
# Purpose:
#       Pulls Company information from the RMIS API. Works by inputting the dotNumber
#   followed by the userID and password into the command line. From this, the
#   dotNumber, userID, and password will be concat with the RMIS API url and send
#   and http request and the response will be in the form of an XML document.
#   The document will be saved into a temp file to be parsed using BeautifulSoup
#   and dumped into the appropriate File(s).   
#
#
# Extra Info:
#   You need beautifulsoup and prettytable to run
#
# pip installs:
#   pip install beautifulsoup4
#   pip install prettytable
#
# Run:
#   python ./API_Request.py 'dot number' 'userID' 'password'
#
# Ex: 
#   python ./SAFER_Scraper.py 100969 userID425 password123
###############################################################################
def main():
    try:
        dotNumber = Get_DOT_Number()
        clientID, pwd = Get_API_Auth_Info()
        apiRequestURL = Get_Request_URL(dotNumber, clientID, pwd)
        requestXmlText = Retrieve_API_Info(apiRequestURL)
        #print(apiRequestURL)
        Dump_To_File(requestXmlText)
        Parse_XML(dotNumber)
    except:
        print("Invalid Dot Number")

###############################################################################
# Returns the inputted DotNumber .. This will be the first command line argument
def Get_DOT_Number():
    import sys
    return sys.argv[1]

###############################################################################
# returns the user ID followed by the password .. These are inputted into the
# 2nd and 3rd position of the command line .. Can be pulled from salted / hashed
# file if wanted later
def Get_API_Auth_Info():
    import sys
    return sys.argv[2], sys.argv[3]

###############################################################################
# concacts the API URL with the dotNumber, clientID, and password
def Get_Request_URL(dotNumber, clientID, pwd):
    URL = 'http://api.gormis.com/_c/std/api/ExpandedCarrierAPI.aspx?clientID=' + str(clientID)
    URL += '&pwd=' + str(pwd) 
    URL += '&version=7&QueryType=DOT&QueryID=' + str(dotNumber)
    return URL

###############################################################################
# requests the inputted URL to the RMIS API and returns the XML response
def Retrieve_API_Info(apiRequestURL):
    import requests
    return requests.get(apiRequestURL).text

###############################################################################
def Dump_To_File(requestXmlText):
    #with open("../Data/temp/company_info.xml", "w") as file:
    with open("company_info.xml", "w") as file:
        file.write(requestXmlText)
    file.close()

###############################################################################
# Parses the XML file and prints it into a table
def Parse_XML(dotNumber):
    from bs4 import BeautifulSoup
    companyTags = ['dot_LegalName', 'OperatingStatus']
    addressTags = ['Address1', 'City', 'St', 'Zip']
    contactTags = ['Phone', 'Fax', 'Email']
    #contactTags = ['CLAIMS', 'CORPORATE', 'DISPATCH', 'SALES', 'ACCOUNTSPAYABLE', 'AFTERHOURS', 'BILLING']
    coverageTags = ['CoverageDescription', 'PolicyNumber', 'ExpirationDate', 'CancelDate', 'Producer', 'ProducerPhone', 'Underwriter']
    
    companyXMLFile = open("company_info.xml", "r")
    soup = BeautifulSoup(companyXMLFile.read(),"xml")
    parsedInfo = []
    from prettytable import PrettyTable, MSWORD_FRIENDLY, PLAIN_COLUMNS, DEFAULT
    companyTable = PrettyTable(['Company Info', 'Data'])
    coverageTable = PrettyTable(['Coverage Info', 'Data'])
    for i in range(0,len(companyTags)):
        foundInfo = soup.find(companyTags[i]).text
        companyTable.add_row([companyTags[i], foundInfo])
        parsedInfo.append(foundInfo)
        
    for i in range(0, len(addressTags)):
        foundInfo = soup.find(addressTags[i]).text
        companyTable.add_row([addressTags[i], foundInfo])
        parsedInfo.append(foundInfo)
        
    for i in range(0, len(contactTags)):
        foundInfo = soup.find(contactTags[i]).text
        companyTable.add_row([contactTags[i], foundInfo])
        parsedInfo.append(foundInfo)
    
    for i in range (0, len(coverageTags)):
        foundInfo = soup.find(coverageTags[i]).text
        coverageTable.add_row([coverageTags[i], foundInfo])
        parsedInfo.append(foundInfo)
        
    companyTable.set_style(DEFAULT)
    coverageTable.set_style(DEFAULT)
    #.header = False
    companyTable.align = "l"
    coverageTable.align = "l"
    print(companyTable)
    print(coverageTable)
    #Dump_To_CSV(parsedInfo, dotNumber)

        
###############################################################################
# Dumps the component to the appropriate SQL table
def Dump_To_CSV(parsedInfo, dotNumber):
    import csv
    #open('parsedInfo)
    with open('parsedInfo' + str(dotNumber), 'wb') as parsedInfoFile:
        wr = csv.writer(parsedInfoFile, quoting=csv.QUOTE_ALL)
        wr.writerow(parsedInfo)
    
###############################################################################
main()