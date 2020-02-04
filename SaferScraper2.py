import urllib.request

from bs4 import BeautifulSoup           #The library used to parse in the table data
from prettytable import PrettyTable     #The library used to make the table
from prettytable import MSWORD_FRIENDLY
from prettytable import PLAIN_COLUMNS
from prettytable import DEFAULT

def n_a(list):
    for i in range(len(list)):
        if list[i] == chr(160):
            list[i] = "N/A"
        list[i] = single_space(list[i])
    return list

def single_space(string):
    if string[0] == ' ':                #If the first char is a space
        out = ''
        for i in range(1, len(string)): #Prints out every char after the space
            out += string[i]
        string = out
    return string                       #Returns string

def spaces(string):                     #checks the string for double spaces and replaces them
    out = ''
    for i in range(len(string)):
        if string[i] != ' ' or string[i + 1] != ' ':                                            #Checks for double space
            if string[i].isalpha or string[i] == ',':                                           #Checks if char is an alphanumeric or comma
                if string[i] != chr(160) and string[i] != chr(13) and string[i] != chr(10):     #Checks that char is not a random ascii character
                    out += string[i]
    return out

def clean(string):
    out = single_space(spaces(spaces(string)))      #Runs the cleanup functions
    return out


#The Dot number that will be input from user
#DotNum = input("Enter your USDOT Number: ")
DotNum = '114448'

#The url website that we're parsing
url = 'https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=' + DotNum

page = urllib.request.urlopen(url)
soup = BeautifulSoup(page,"html.parser")


#Checking if record exists

if "Record Not Found" in str(soup):
    print("RECORD NOT FOUND") #To find RECORD
elif "INACTIVE" in str(soup):
    print("INACTIVE") #To find INACTIVE Website
else:
    #Active

    # find table header that contains an anchor with the table header we need, go back to parent, find sibling which is table data and extract data

    entityType = soup.find("a", text="Entity Type:").find_parent().find_next_sibling('td').text             #Searhes website for text 'Entity Type' and checks following table data
    status = soup.find("a", text="Operating Status:").find_parent().find_next_sibling('td').text            #Searches website for text 'Operating Status' and checks following table data
    legalName = soup.find("a", text="Legal Name:").find_parent().find_next_sibling('td').text               #Searches website for text 'Legal Name' and checks following table data
    physicalAddress = soup.find("a", text="Physical Address:").find_parent().find_next_sibling('td').text   #Searches website for text 'Physical Address' and checks following table data
    phone = soup.find("a", text="Phone:").find_parent().find_next_sibling('td').text                        #Searches website for text 'Phone' and checks following table data
    usdotNum = soup.find("a", text="USDOT Number:").find_parent().find_next_sibling('td').text              #Searches website for text 'USDOT Number' and checks following table data
    drivers = soup.find("a", text="Drivers:").find_parent().find_next_sibling('td').text                    #Searches website for text 'Drivers' and checks following table data

    entityType = entityType.strip()             #Gets rid of whitespace
    physicalAddress = physicalAddress.strip()   #Gets rid of whitespace


    list1 = ['Entity Type', 'Operating Status', 'Legal Name', 'Physical Address', 'Phone', 'USDOT Number', 'Drivers']
    list2 = [entityType, status, legalName, clean(physicalAddress), phone, usdotNum, drivers]

    list2 = n_a(list2)

    table = PrettyTable(['Categories', 'Information'])
    for x in range(0,7):
        table.add_row([list1[x], list2[x]])

    table.set_style(DEFAULT)            #Style can be MSWORD_FRIENDLY, DEFAULT, or PLAIN_COLUMN
    table.header = False
    table.align = 'l'
    print(table)
