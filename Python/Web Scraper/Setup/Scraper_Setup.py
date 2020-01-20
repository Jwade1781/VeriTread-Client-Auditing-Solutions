#######################################################################
#
# Purpose:
# The purpose of this program is to easily allow the user to install all
# dependencies within the system, using pip.
#
# TODO:
# [1] Ensure that all libraries used in the programs are in the list of 
#     imports to be checked
#
# Extra Info:
# Should be the first run program to ensure all imports are installed
# & the data directory / subdirectories are created
#
# Works by iterating through a list of libraries that must be installed
# for the programs to work correctly. It will check to see if the library
# has already been installed, if not, it will install it using pip command.
#
# After the libraries are installed, the program will create the Data directory
# and the subdirectories 
#
#
# Run:
# python ./Scraper_Setup.py
#
#######################################################################
def __main():
    Install_Imports()

####################################################################### 
# install all of the required imports using pip
def Install_Imports():
    import subprocess, sys
    imports = ['pandas', 'numpy']

    for i in range (len(imports)):
        subprocess.check_call([sys.executable, "-m", "pip", "install", imports[i]])

#######################################################################
__main()