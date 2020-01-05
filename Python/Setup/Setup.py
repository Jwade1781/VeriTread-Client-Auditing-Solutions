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
# -- This currently does not populate the needed Datasets subdirectory to
#    run all of the other programs. This can be extended later to pull the training/testing
#    dataset from a database if wanted
#
# Run:
# python ./Setup.py
#
#######################################################################
def __main():
    Install_Imports()
    Create_Directories()

####################################################################### 
# install all of the required imports using pip
def Install_Imports():
    import subprocess, sys
    imports = ['scipy', 'joblib', 'python-docx', 'pandas']

    for i in range (len(imports)):
        subprocess.check_call([sys.executable, "-m", "pip", "install", imports[i]])

#######################################################################
# Create the Data directory and the subdirectories of it
def Create_Directories():
    import os
    path_directory = '..\Data'

    # Create the Data Folder
    try:  
        os.mkdir(path_directory)
        print(path_directory + ' was created')
    except:
        print(path_directory + ' was already created')

    # Create the needed subdirectories of Data
    needed_subdirectories = ['Assets', 'Datasets', 'Dotfiles', 'Models', 'Saved_Companies', 'Saved_Predictions', 'temp']
    for i in range (len(needed_subdirectories)):
        # Attempt to create the directory.. if exists go to the next directory to be created
        path_subdirectory = path_directory + '\\' + needed_subdirectories[i]
        try:
            os.mkdir(path_subdirectory)
            print(path_subdirectory + ' was created')
        except:
            print(path_subdirectory + ' was already created')
            continue

#######################################################################
__main()