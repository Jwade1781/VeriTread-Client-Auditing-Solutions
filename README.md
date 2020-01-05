# VeriTread Registration Solutions
## Senior Design FPU FA 2019 - SP 2020
 -- Currently the ML and Email modules are created in python with the plan of 
    running each from a C# program if approved. If not, recreate each using equivalent C# libraries, i.e. Sklearn -> ML.NET
    
## Updates
  11/29/2019 - Initial README.MD created

## Description
This project is to create solutions for the Online Freight
Broker VeriTread.

# Tasks that must be implemented

[1] Create an automatic USDoT Checker that will pull
    information from RMIS via API calls and/or SAFER. This must
    worker by the user entering a DoT Number into their browser
    that will be checked against either solutions and send back 
    if the entered DoT number is valid & active.
      -- If it is valid & active, allow registration
      -- if either check fails, deny and display message.
      
[2] Create an automatic USDoT Checker that will pull all
    currently registered DoT numbers from VeriTreads customer
    database. Send the DoT numbers to RMIS/SAFER and determine
    if the numbers activity is still marked as active/inactive.
    Update the database if changed.

Optional ** If Completed Before End of SP 2020 Semester

Task [1] Extended - 
    Use some sort of method, i.e. Machine Learning, 
    that will determine if the found company pulled 
    from RMIS API is a suitable customer for VeriTread.
    If the system deems that the customer is not suitable
    deny registration and display a message.
    
# How to Run Programs 
        Install all python dependencies, create necessary directories
    [1 first run only] run Setup.py
    
        Create the Decision Tree and save it    
    [2] run /ML/Registration_Decision_Tree.py
    
    [3] -- TBD
