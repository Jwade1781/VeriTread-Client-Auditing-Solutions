############################################################################
#
# Purpose:
#   Takes all previously entered companies from a file, sends it to
#   SAFER_Scraper.py and scrapes all of their information. The information is
#   then dumped a file in the saved companies directory. Added threading to decrease the
#   time spent running the program.
#
# Extra Info:
#   You need beautifulsoup and prettytable to run. The list of dot numbers is
#   stored at ../Data/Dataset/all_companies.csv
#
#   The files will be dumped at ../Data/Saved_Companies/
#
# pip installs:
#   pip install beautifulsoup4
#   pip install prettytable
#
# Run: (use auto or -1 for thread count to use the same number as logical cores on computer or half for half of them)
#   python ./Scrape_All_Previous_Companies.py 'thread count' 
#
# Ex: 
#   python ./Scrape_All_Previous_Companies.py auto
#   or
#   python ./Scrape_All_Previous_Companies.py 12
#
##############################################################################
# Gathers all of the saved previous companies and then splits them into
# seperate threads that will generate their files.
# The number of threads to use for the program is dependant upon the number
# of cores/threads the processor has.

dotNumbers = []

##############################################################################
def main():
    Get_DotNumbers()
    TOTALTHREADS = Get_Total_Threads()
    Split_And_Start_Threads(TOTALTHREADS)

##############################################################################
# Retrieves all of the DOT numbers from a given CSV file 
# The numbers are then placed in a global array that is accessible by all of the 
# threads.
def Get_DotNumbers():
    path = "../Data/Dataset/"
    filename = "all_companies.csv"
    fullPath = path + filename
    import csv
    with open(fullPath) as allCompaniesCSV:
        readCSV = csv.reader(allCompaniesCSV, delimiter=',')
        for row in readCSV:
            row = str(row).replace('\'', '')
            row = str(row).replace("]", "")
            row = str(row).replace("[", "")
            dotNumbers.append(row)

##############################################################################
# Get the total number of threads the program will use to split the work of
# Scraping the DOT numbers with through the command line
# inputting 'auto' or '-1' as the argument will use the same number of cores
# as the computer has.
# ** Using 'auto' may severely slow all other processes **
def  Get_Total_Threads():
    import sys
    import multiprocessing
    TOTALTHREADS = sys.argv[1]
    
    if (TOTALTHREADS == 'auto' or TOTALTHREADS == '-1' or TOTALTHREADS == ''):
        TOTALTHREADS = multiprocessing.cpu_count()
        
    elif (TOTALTHREADS == 'half'):
        TOTALTHREADS = multiprocessing.cpu_count()/2

    return int(TOTALTHREADS)
        

##############################################################################
# Creates all of the threads these threads are based upon either the
# inputted number wanted or how many cores the computer has
def Split_And_Start_Threads(TOTALTHREADS):
    import threading
    for threadsCreated in range (0, TOTALTHREADS):
        newThread = threading.Thread(target=Execute_Scraper, args=(TOTALTHREADS, threadsCreated, TOTALTHREADS-1))
        print("Starting Thread:", threadsCreated)
        newThread.start()
        #print("New thread created:", threadsCreated)
        
    newThread.join()

##############################################################################
# The thread will execute the SAFER_Scraper.py script. The work will be split
# depending upon the thread's threadnumber. If the work cannot be split evenly amongst
# all of the threads, the final thread will take on the extra workload. This should
# not effect the runtime too much; average DOT lookup is about ~1.5-2.5 seconds and on 12 cores
# it should take about 16.5-27.5 additional seconds for 11 extra items that were not split.

def Execute_Scraper(TOTALTHREADS, threadNumber, lastThread):
    import subprocess
    import time
    #print('\n\nDot number length: ', len(dotNumbers), '\n\n')
    #print("Starting thread for : ", threadNumber)
    # Total amount of work the thread has to do
    totalThreadCompanies = int((len(dotNumbers)/TOTALTHREADS))        

    # The first threads work
    if (threadNumber == 0):
        threadWork = dotNumbers[:totalThreadCompanies]

    # Other threads work will be dependant upon what their threading number is
    # If cannot split work equally the last thread will take the remaining numbers
    else:
        threadDotNumbers = totalThreadCompanies * threadNumber
        threadCompanyStart = threadDotNumbers
        threadCompanyEnd = threadCompanyStart + totalThreadCompanies
        threadWork = dotNumbers[threadCompanyStart:threadCompanyEnd]

        if (len(dotNumbers) % TOTALTHREADS != 0):
            if (threadNumber == lastThread):
                threadWork = dotNumbers[threadCompanyStart:]

    # Execute the python script to scrape SAFER Site
    # The final thread will print the amount of work complete/estimated time left
    howOftenToPrint = 5 # How many cycles will be passed before the thread will print progress
    startTime = time.time()
    for i in range (0, len(threadWork)):
        subprocess.call(['python', 'SAFER_Scraper.py', threadWork[i]])
        if (threadNumber == lastThread and i % howOftenToPrint == 0 and i != 0):
            PrintProgress(threadNumber, i, startTime, len(threadWork))     

##############################################################################
# Prints the current progress of the thread and estimates how much longer until
# completion based on the average lookup time and the amount of work left
def PrintProgress(threadNumber, totalCompleted, startTime, totalWork):
    import time
    elapsedTime = (time.time() - startTime)
    averageTime = (elapsedTime/totalCompleted)
    estimatedCompletionTime = (averageTime * (totalWork - totalCompleted))

    print("Thread [" + str(threadNumber) + "] Created file for ", totalCompleted, "/", (totalWork), end='\t')
    print("Elapsed Time: ", round(time.time() - startTime, 2), "seconds", end='\t')
    print("Estimated Time til Completion: [" + str(round(estimatedCompletionTime, 2)) + "] seconds", end='\t')
    print("Average Lookup time:", str(round(averageTime, 2)))
    
            
##############################################################################
main()