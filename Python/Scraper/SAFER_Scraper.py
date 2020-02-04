############################################################################
#
# Purpose:
#   Scrapes the SAFER website looking for any valuable information based on
#   the adjanct informations <th> label/header value
#
# Extra Info:
#   You need beautifulsoup and prettytable to run
# pip installs:
#   pip install beautifulsoup4
#   pip install prettytable
#
# Run:
#   python ./SAFER_Scraper.py 'dot number'
#
# Ex: 
#   python ./SAFER_Scraper.py 144448

##############################################################################
def main():
    dotNumber = Get_Dot_Number()
    url = Get_URL(dotNumber)
    parsedElementLabels, parsedElements = Scrape_SAFER(url)
    Print_Scraped_Elements(parsedElementLabels, parsedElements)
    Dump(parsedElementLabels, parsedElements, dotNumber)
    return

##############################################################################
# Get the DOT Number from the Command Line / User Input
def Get_Dot_Number():
    #The Dot number that will be input from user
    #dotNum = input("Enter your USDOT Number: ")
    import sys
    dotNumber = sys.argv[1]
    return dotNumber

##############################################################################
# Get the URL from the safer website by concating the constant query url
# with the inputted DOT Number
def Get_URL(dotNumber):
    SAFER_QUERY_URL = 'https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string='
    return SAFER_QUERY_URL + dotNumber

##############################################################################
# Pull the SAFER website, check to see if the record is good & if so, continue with parsing, else exit

# The first array, parsedElementLabels, holds the labels that will be looked for within the HTML. 
# These MUST match how the <th> value is stored within the page; add more labels directly to this to pull more data
# The second array, parsedElements, holds the element values that were scraped based on their neighboring <th>
def Scrape_SAFER(url):
    import urllib.request
    from bs4 import BeautifulSoup #The library used to parse in the table data

    MOSTATTEMPTS = 10
    for attempts in range (MOSTATTEMPTS):
        try:
            page = urllib.request.urlopen(url)
            break

        # Most likely did not receive a response from server (error 504) indicating that their servers may be down
        # Will attempt 10 times. if Final attempt is unsuccessful, exit. Could be extended to create a 
        # dump log if wanted later.
        except:
            print("****** Something went wrong parsing..", url, "trying again *********", end='\n\n')
            if (attempts == MOSTATTEMPTS -1):
                print("No response from server.. All Attempt Used.. Aborting")
                exit(0)
            continue

    soup = BeautifulSoup(page,"html.parser")

    if (not Check_Record_Status(soup)): # Check the status of the page, if bad exit, else continue
        exit(0)

    parsedElementsLabels = ["USDOT Number:", "Entity Type:", "Operating Status:", "Legal Name:", 
                            "Physical Address:", "Mailing Address:", "Phone:", "Drivers:",
                            "Power Units:", "DUNS Number:", "Crashes"]
    parsedElements = []

    # Go through all of the elements and parse them from the page; 
    # saving the pulled values into an array called parsedElements
    for i in range (0, len(parsedElementsLabels)):
        parsedElements.append((Parse_Page(soup, parsedElementsLabels[i])))

    return parsedElementsLabels, parsedElements

##############################################################################
# Check if the record exists/inactive: 
# if not/inactive -> print bad record and return (false)
# else -> return that record was good (true)
def Check_Record_Status(soup):
    if "Record Not Found" in str(soup):
        #print("RECORD NOT FOUND") #To find RECORD
        return False
    elif "INACTIVE" in str(soup):
        #print("INACTIVE") #To find INACTIVE Website
        return False
    return True # Record was good, return and continue with parsing

##############################################################################
# find table header that contains an anchor with the table header we need, 
# go back to parent, find sibling which is table data and extract data
def Parse_Page(soup, parsingElement):
    try:
        parsedElement = soup.find("a", text=parsingElement).find_parent().find_next_sibling('td').text 

    except:
        parsedElement = soup.find("th", text=parsingElement).find_next_sibling('td').text
        print(parsedElement)

    parsedElement = Format_Characters(parsedElement)
    return parsedElement

##############################################################################
# Format the parsed Element to get rid of unwanted characters such as double space and new lines
# The Ascii value was used on some of these due to not knowing the equivalent character
def Format_Characters(parsedElement):
    parsedElement = parsedElement.replace(chr(10), "")   # New Line Feed
    parsedElement = parsedElement.replace(chr(13), "")   # Carriage Return 
    parsedElement = parsedElement.replace(chr(160), "")  # Extended Ascii, creates new line from byte issue with UTF-8
    
    # Removes all of the double spaces, looped due to removing a double space
    # Could still cause another double space to be present if an odd number of double spaces
    # Are present..
     
    for i in range (0, len(parsedElement)):
        if (parsedElement.count("  ") > 0):
            parsedElement = parsedElement.replace('  ', ' ', 1)
            i += 1

    # Change the seperation, allowing for using CSV files.. Can be changed back later if using JSON or SQL 
    parsedElement = parsedElement.replace(',', '^')      

    # If the first char in the element is a space, get rid of it. Same if last
    # There may be no characters within the element
    # if none, write the element as N/A -> input DOT 1140344 phone for example
    if (len(parsedElement) > 0):
        if (parsedElement[0] == ' '):
            parsedElement = parsedElement.replace(' ', '', 1)

        if (parsedElement[len(parsedElement)-1] == ' '):
            parsedElement = parsedElement[:-1]

    # The element holds no characters, meaning not found
    else:
        parsedElement = "N/A"

    #for i in range(0, len(parsedElement)):
    #    print(str(ord(parsedElement[i])), parsedElement[i])

    return parsedElement

##############################################################################
# Looks for what type of address needs to be found: addressType (Physical / Mailing)
# Parses the address's so that the street name, state, and zip code so it can be stored individually
# First looks for the position of the comma, indicating that directly to the right
# of that is the state seperated by a space and then the zip.
# Directly right of the comma is the Street Address

# ** Currently not outputting all correct info due to weird info being parsed, weird placement
# of commas etc. Leaving in to be used later if needed
def Parse_Address(parsedElementLabels, parsedElements, addressType):
    try:
    # Look  for the state to be parsed directly right of the comma in the string
        for i in range(0, len(parsedElementLabels)):
            if (parsedElementLabels[i] == addressType):
                statePositionStart = parsedElements[i].find('^')

                # Look to find the first position after the comma that is a letter
                # If position is found, look for the end position of the state that is not a letter
                for statePositionStart in range (statePositionStart, len(parsedElements[i])):
                    if (parsedElements[i][statePositionStart] != ' ' and parsedElements[i][statePositionStart] != '^'):
                        for statePositionEnd in range (statePositionStart, len(parsedElements[i])):
                            if (not parsedElements[i][statePositionEnd].isalpha()):
                                #print("End found at: ", statePositionEnd)
                                break
                        break
            
                # Format and save each of the parsed elements to be returned
                streetString = Format_Characters(parsedElements[i][:statePositionStart - 2]) # - 2 due to the position of the last space/comma
                stateString = Format_Characters(parsedElements[i][statePositionStart:statePositionEnd])
                zipString = Format_Characters(parsedElements[i][statePositionEnd:]) 

                return streetString, stateString, zipString
                
    # There was no valid address provided
    except:
        return 'N/A', 'N/A', 'N/A'

##############################################################################
# Dumps the scraped elements into csv file that can be extracted in the ML program
# Changed the delimiter to ^ due to physical address having a ',' 
# Could change it back if we split physical address up to street, state, zip, etc.
def Dump(parsedElementLabels, parsedElements, dotNumber):
    try:
        PATH = "../Data/Saved_Companies/"
        fullPath = PATH + str(dotNumber) +'.csv'
        import csv
        with open(fullPath, mode='w') as companyCsvFile:
            companyWriter = csv.writer(companyCsvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            companyWriter.writerow(parsedElementLabels)
            companyWriter.writerow(parsedElements)

        #print("\nDumped Found Info to: " + fullPath)

    except:
        print("Could not dump found info to", fullPath, ". Make sure that the path exists")

##############################################################################
# Print all the elements that were parsed from SAFER website
# Uses prettytable with the first item in the row being a label and
# the second item to be the scraped data
def Print_Scraped_Elements(parsedElementLabels, parsedElements):
    #The library used to make the table
    from prettytable import PrettyTable, MSWORD_FRIENDLY, PLAIN_COLUMNS, DEFAULT

    table = PrettyTable(['Labels', 'Information'])
    # add each label and scraped info into a new table row
    for i in range(0, len(parsedElements)):
        table.add_row([parsedElementLabels[i], parsedElements[i]])
    table.set_style(DEFAULT)
    table.header = False
    table.align = "l"
    print(table)
    
##############################################################################

main()
