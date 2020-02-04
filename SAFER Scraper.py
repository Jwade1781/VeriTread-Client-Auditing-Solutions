import urllib.request

from bs4 import BeautifulSoup #The library used to parse in the table data

def spaces(string):
    out = ''
    for i in range(len(string)):
        if string[i] != ' ' or string[i + 1] != ' ':
            if string[i].isalpha or string[i] == ',':
                if string[i] != chr(160) and string[i] != chr(13) and string[i] != chr(10):
                    out += string[i]
    return out

def clean(string):
    out = spaces(spaces(string))
    return out


#The Dot number that will be input from user
DotNum = input("Enter your USDOT Number: ")

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
    pyhsicalAddress = soup.find("a", text="Physical Address:").find_parent().find_next_sibling('td').text   #Searches website for text 'Physical Address' and checks following table data
    phone = soup.find("a", text="Phone:").find_parent().find_next_sibling('td').text                        #Searches website for text 'Phone' and checks following table data
    usdotNum = soup.find("a", text="USDOT Number:").find_parent().find_next_sibling('td').text              #Searches website for text 'USDOT Number' and checks following table data
    drivers = soup.find("a", text="Drivers:").find_parent().find_next_sibling('td').text                    #Searches website for text 'Drivers' and checks following table data

    entityType = entityType.strip()             #Gets rid of whitespace
    pyhsicalAddress = pyhsicalAddress.strip()   #Gets rid of whitespace

    # Prints out table data in console
    print("Entity Type: ",entityType)
    print("Operating Status: ",status)
    print("Legal Name: ",legalName)
    print("Pyhsical Address: ", clean(pyhsicalAddress))
    print("Phone: ",phone)
    print("USDOT NUMBER: ", usdotNum)
    print("Drivers: ", drivers)
