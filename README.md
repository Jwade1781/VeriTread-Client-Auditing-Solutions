# VeriTread Registration Solutions
## Senior Design FPU FA 2019 - SP 2020
 ~~-- Currently the ML and Email modules are created in python with the plan of 
    running each from a C# program if approved. If not, recreate each using equivalent C# libraries, i.e. Sklearn -> ML.NET~~ 
    
    (No longer in current scope [Part of Task 1 Extended])
    
## Updates
  11/29/2019 - Initial README.MD created
  
  2/28/2020 - Update to reflect changes in project; Access to RMIS APIs / No database access

## Description
This project is to create solutions for the Online Freight
Broker VeriTread. It will be used to pull the appropriate information
from both potential client's and already registered client's information that
have been updated via RMIS' APIs. 

First program will have a dot number inputted into it that will be 

# Tasks that must be implemented
[1] Create an automatic USDoT Checker that will pull information 
    from RMIS' onboarding API. This must work by the user submitting 
    a DoT Number from their browser to VeriTread's server. The server 
    will then run a specific program with the inputted DoT Number that
    will pull any of the company's information. This information must
    be stored in a CSV file.
      
[2] Create an automatic USDoT Checker that will pull all
    currently registered DoT numbers from VeriTreads customer
    database. This can be achieved using the RMIS Delta API,
    showing companies that have had any changes.
    
Optional ** If Completed Before End of SP 2020 Semester

Task [1] Extended - 
    Use some sort of method, i.e. Machine Learning, 
    that will determine if the found company pulled 
    from RMIS API is a suitable customer for VeriTread.
    If the system deems that the customer is not suitable
    deny registration and display a message.

[3] Create a new user GUI that will display the information that
    was found attached to the DOT Number
    
# Dependencies (Tested versions in brackets)
    [1] PrettyTable (Used for print formating) [0.7.2]
    [2] lxml (XML Parser) [4.4.1]

# Pip installs
    [1] pip install prettytable
    [2] pip install lxml

# How to Run Programs 
Pulling individual Client Information: (Onboarding API)

    python ./Onboarding_API_Request.py 'userID' 'password' 'dot number'
    
Pulling list of all companies that have had changes: (Delta API)

    python ./Delta_Api_Request.py 'userID' 'password'
  
Setup the directories && Install Dependencies

    python ./Setup.py 'Install Required Modules (True/False)'
