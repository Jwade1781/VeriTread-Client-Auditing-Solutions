############################################################################
# Purpose:
#   Create a web scraper that will be used to scrape the SAFER website
#   given an inputted DOT number from the command line.
#
# TODO
# [FIN] Convert datatype of scraped data from np.ndarray to strings to migrate data between programs easier
# [ 2 ] Dump any found useful information that could be used for determining elig .. see ../ML/Data/Dataset/reg_dataset.csv 
# [ 3 ] Refactor/update comments -- I made it look long & ugly :(
#
# Extra Info:
#  Works by parsing the command line by running either:
#  python ./SAFER_Scraper.py 'dotnumber'
#
#  Ex:
#  python ./SAFER_Scraper.py 1140344
#
#  or to run a test without inputting a dot_number: (defaults to 1140344)
#  python ./SAFER_Scraper.py test
#
#   Uses pandas.read_Html to retrieve the tables from the SAFER website
#
#   This program most likely will be needed to be updated if any changes to 
#   the SAFER website are made
#
##########################################################################################

def __main():
    import time
    start_time = time.time()
    dot_number = _parse_command_line()

    query_url = 'https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=' + str(dot_number)
    ScrapeSafer(query_url, dot_number)

    print("\n\nTotal execution time: %s seconds" % (time.time() - start_time))

###########################################################################################
# Parse the command line to retrieve the entered dot number
# if 'test' is inputted, default to the dot number 1140344; Must be replaced later
#
# An error will be flagged if either an invalid dot number is entered (has non numerical characters)
# or if the command line is left blank

def _parse_command_line():
    try:
        import sys
        dot_number = (sys.argv[1])
        if (dot_number == 'test'):
            dot_number = 1140344
        
        dot_number = int(dot_number)
        return dot_number

    except:
        print("** ERROR ** Parsing Dot number from command line.. Exiting")
        exit(0)

###########################################################################################
# Scrapes the SAFER website given the inputted DOT number concat with the SAFER url
#
# Works by using pandas' read_html module
# the wanted scraped data's indices must be hard coded into the program
# 
# ex: 
# we want the 6th table in the html code. This table holds majority of the information that 
# we are interested in like the number of drivers, address, and operating status.
#
# From this table we hardcode which X, Y values we want to look for.
# To view the X values of the table, use the function PrintIndicesLocation(df)
# This will print all the scraped data in the data with their correspondant x value; the y value needs
# to be found manually in that row.. (either value 0, 1, 2)
#
# If the program breaks, the website most likely changed; these should be looked at and changed first
#

def ScrapeSafer(url, dot_number):
    import pandas as pd

    tables = pd.read_html(url, index_col=0)

    # try to extract the table information into a dataframe.. if error occurs the inputted DoT number was not valid / inactive
    try:
        # Tables --
        # Table1: General Comp info: Dot Number, Operating Status, Company Type, Company name, Owner Name, Mailing/physical Addresses, Total Drivers, Duns Number, State Carrier ID
        # Table2: 24 month Inspection Info: Out of service vehicles %
        # Table3: 24 month crash reports: Fatal, Injury, Tow, Total
        x_indices_table_1, y_indices_table_1, extracted_data_labels_table_1, TABLE_1_INDEX = GetTable1Indices()
        x_indices_table_2, y_indices_table_2, extracted_data_labels_table_2, TABLE_2_INDEX = GetTable2Indices(len(tables))
        x_indices_table_3, y_indices_table_3, extracted_data_labels_table_3, TABLE_3_INDEX = GetTable3Indices(len(tables))
        
        df_table_1 = tables[TABLE_1_INDEX].values
        df_table_2 = tables[TABLE_2_INDEX].values
        df_table_3 = tables[TABLE_3_INDEX].values
    
    except:
        print('** ERROR ** The inputted DoT number was not found within safer.. May no longer be in service.. Could not extract data.. Exiting')
        exit(0)
        
    print("\n\nInputted DOT Number: " + str(dot_number))
    print("================================ Printing Scraped Information ================================\n")
    # Used for formatting print info .. finds how many spaces to add
    longest_label_length = 0
    longest_label_length = GetFormatInfo(extracted_data_labels_table_1, 0)
    longest_label_length = GetFormatInfo(extracted_data_labels_table_2, longest_label_length)

    print('************************************ General Company Info ************************************')
    PrintFoundInformation(df_table_1, x_indices_table_1, y_indices_table_1, extracted_data_labels_table_1, longest_label_length, 'Table 1')

    print('\n\n************************************* Inspection Info **************************************')
    PrintFoundInformation(df_table_2, x_indices_table_2, y_indices_table_2, extracted_data_labels_table_2, longest_label_length, 'Table 2')
    
    print('\n\n*************************************** Crash Info *****************************************')
    PrintFoundInformation(df_table_3, x_indices_table_3, y_indices_table_3, extracted_data_labels_table_3, longest_label_length, 'Table 3')

    # Find all locations to be printed -> Used to help figure out table index / row locations
    #print("\n\n================================ Printing all index locations ================================")
    #PrintIndicesLocations(tables, 'All Tables')
    #PrintIndicesLocations(df_table_1, 'General Comp Table')
    #PrintIndicesLocations(df_table_2, 'Inspections Table')
    #PrintIndicesLocations(df_table_3, 'Crashes Table')
    #print(type(df_table_2))
###########################################################################################
# return the wanted row X, Y values with their labels.
# This is hard coded and may change upon website being updated .. all table rows share the same
# class name of 'queryfield' so it was done this way
#
#
# The index of each of the elements in x_indices, y_indices, and extracted_data_labels must match to have correct results.
# if out of range error occurs, make sure the label was placed in the correct location in extracted_data_labels, else look at
# the index of the other lists.

def GetTable1Indices():
    # Acronyms
    # -- DBA - Doing Bussiness As; The trade name of the company
    # -- DUNS - Data Universal Numbering System

    TABLE_1_INDEX = 6

    COMPANY_TYPE_X_INDEX = [0]
    COMPANY_TYPE_Y_INDEX = [0]
    
    OPERATING_STATUS_X_INDEX = [1]
    OPERATING_STATUS_Y_INDEX = [0]

    LEGAL_NAME_X_INDEX = [2]
    LEGAL_NAME_Y_INDEX = [0]

    DBA_NAME_X_INDEX = [3] 
    DBA_NAME_Y_INDEX = [0]

    PHYSICAL_ADDRESS_X_INDEX = [4]
    PHYSICAL_ADDRESS_Y_INDEX = [0]

    MAILING_ADDRESS_X_INDEX = [6]
    MAILING_ADDRESS_Y_INDEX = [0]

    DOT_NUMBER_X_INDEX = [7]
    DOT_NUMBER_Y_INDEX = [0]
    
    STATE_CARRIER_ID_X_INDEX = [7]
    STATE_CARRIER_ID_Y_INDEX = [2]

    MC_NUMBER_X_INDEX = [8]
    MC_NUMBER_Y_INDEX = [0]

    DUNS_NUMBER_X_INDEX = [8]
    DUNS_NUMBER_Y_INDEX = [2]

    TOTAL_DRIVERS_X_INDEX = [9]
    TOTAL_DRIVERS_Y_INDEX = [2]
    
    x_indices = [DOT_NUMBER_X_INDEX, OPERATING_STATUS_X_INDEX, COMPANY_TYPE_X_INDEX, LEGAL_NAME_X_INDEX, 
                DBA_NAME_X_INDEX, PHYSICAL_ADDRESS_X_INDEX, MAILING_ADDRESS_X_INDEX, STATE_CARRIER_ID_X_INDEX, 
                MC_NUMBER_X_INDEX, DUNS_NUMBER_X_INDEX, TOTAL_DRIVERS_X_INDEX]

    y_indices = [DOT_NUMBER_Y_INDEX, OPERATING_STATUS_Y_INDEX, COMPANY_TYPE_Y_INDEX, LEGAL_NAME_Y_INDEX, 
                DBA_NAME_Y_INDEX, PHYSICAL_ADDRESS_Y_INDEX, MAILING_ADDRESS_Y_INDEX, STATE_CARRIER_ID_Y_INDEX, 
                MC_NUMBER_Y_INDEX, DUNS_NUMBER_Y_INDEX, TOTAL_DRIVERS_Y_INDEX]

    extracted_data_labels = ['Dot Number', 'Operating Status', 'Company Type:', 'Legal Name:', 'Trade Name:', 
                            'Physical Address:', 'Mailing Address:','State Carrier ID:', 'MC Number:', 'Duns Number:', 
                            'Total Drivers']

    return x_indices, y_indices, extracted_data_labels, TABLE_1_INDEX

###########################################################################################
def GetTable2Indices(total_tables):
    # Inspection Information Table
    # Tested with USDoT 478072

    # Some companies have more / less tables than others ..
    # This throws off which index to pull. So we have to look at
    # How many total tables are in the html page. It seems that if there are
    # 25 tables the index is 19 and all others are at 23

    if  (total_tables == 25):
        INSPECTION_TABLE_INDEX = 19
    else:
        INSPECTION_TABLE_INDEX = 23

    OUT_OF_SERVICE_VEHICLES_X_INDEX = [1]
    OUT_OF_SERVICE_VEHICLES_Y_INDEX = [0]

    PERCENT_OUT_OF_SERVICE_VEHICLES_X_INDEX = [2]
    PERCENT_OUT_OF_SERVICE_VEHICLES_Y_INDEX = [0]

    x_indices = [OUT_OF_SERVICE_VEHICLES_X_INDEX, PERCENT_OUT_OF_SERVICE_VEHICLES_X_INDEX]
    y_indices = [OUT_OF_SERVICE_VEHICLES_Y_INDEX, PERCENT_OUT_OF_SERVICE_VEHICLES_Y_INDEX]
    extracted_data_labels = ['[24 months] Total Out Of Service Vehicles', '[24 months] Percent of Vehicles Out of Service']
    return x_indices, y_indices, extracted_data_labels, INSPECTION_TABLE_INDEX

###########################################################################################
def GetTable3Indices(total_tables):
    # Crash Report Table
    # Tested with USDoT 478072

    # Some companies have more / less tables than others ..
    # This throws off which index to pull. So we have to look at
    # How many total tables are in the html page

    if (total_tables == 25):
        CRASH_TABLE_INDEX = 20
    else:
        CRASH_TABLE_INDEX = 24

    x_indices = []
    y_indices = []

    FATAL_CRASHES_X_INDEX = [0]
    FATAL_CRASHES_Y_INDEX = [0]

    INJURY_CRASHES_X_INDEX = [0]
    INJURY_CRASHES_Y_INDEX = [1]

    TOW_CRASHES_X_INDEX = [0]
    TOW_CRASHES_Y_INDEX = [2]

    TOTAL_CRASHES_X_INDEX = [0]
    TOTAL_CRASHES_Y_INDEX = [3]

    x_indices = [FATAL_CRASHES_X_INDEX, INJURY_CRASHES_X_INDEX, TOW_CRASHES_X_INDEX, TOTAL_CRASHES_X_INDEX]
    y_indices = [FATAL_CRASHES_Y_INDEX, INJURY_CRASHES_Y_INDEX, TOW_CRASHES_Y_INDEX, TOTAL_CRASHES_Y_INDEX]
    extracted_data_labels = ['Fatal Crashes', 'Involved Injury', 'Involved Tow', 'Total Crashes']
 
    return x_indices, y_indices, extracted_data_labels, CRASH_TABLE_INDEX

###########################################################################################
def GetFormatInfo(table, current_longest):
    # Find the longest label name, this will be used for spacing
    # such that when printing, all printed attributes will line up
    # for easier viewing

    for i in range(0, len(table)):
        if (current_longest < len(table[i])):
            current_longest = len(table)
    return current_longest

###########################################################################################
def PrintFoundInformation(table, x_indices, y_indices, labels, longest_label_length, tablename):
    # Prints any of the found information that was pulled based on the location in the table
    # casts any of the info to a string using np.array2string() before placing in the
    # found_info list; allowing for easier migration

    try:
        import numpy as np
        found_info = []
        for i in range (0, len(x_indices)):
            info = table[x_indices[i]][0]

            found_info.append(FormatElementStrings(np.array2string(info[y_indices[i]])))
            current_label = labels[i]
            print('*', current_label, end='')

            # Adds space formatting to the found scraped info
            for j in range (0, longest_label_length - len(current_label) + 50):
                print(' ', end='')
            
            #found_info[i] = 

            print(found_info[i])

    except:
        print("** ERROR ** Possiblly indices are not lined up properly .. Look at " + tablename + '\'s GetTableIndices module.. Exiting')
        exit(0)

###########################################################################################
# Formats a found element to remove unncessary characters
def FormatElementStrings(info):
    info = info.replace("['", "")
    info = info.replace("']", "")
    info = info.replace("[", "")
    info = info.replace("]", "")
    info = info.replace("MC-", "MC") # Change the formatting such that it lines up with RMIS Format for MC numbers
    return info


###########################################################################################
def PrintIndicesLocations(df, tablename):
    # Prints out the X indix locations for the dataframes
    # must find out the corresponding location
    # Used for development
    print("Indice locations of table: " + tablename)
    for i in range(0, len(df)):
        print(df[i], '\t\t', end='')
        print(str(i), '\n\n')

###########################################################################################
__main()