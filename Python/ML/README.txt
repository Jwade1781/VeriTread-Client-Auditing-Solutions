
=======================================================
************** README file for reg_dt.py **************
=======================================================
This script utilizes sklearn to create a decision tree
that will determine whether an inputted company should
be able to register or not within the VeriTread Server.

This Program is only to setup and train multiple 
decision trees with the most accurate decision tree to
be dumped into a pkl file to be used later in the actual
determination process.

A list of helper command line arguments is built in, do:

python ./reg_dt.py -h 

to receive a list of all commands
=======================================================
	Dependant Libraries needed to be installed:
sklearn
pandas
numpy
joblib

=======================================================
		System Libraries:
os
sys

=======================================================
		Pip installs
pip install sklearn
pip install pandas
pip install numpy
pip install joblib

=======================================================
		Versions using when created
Python 3.7.3
Numpy 1.16.4
Pandas 0.24.2
Sklearn 0.21.2
Joblib 0.13.2

=======================================================
		  Files and Directories
directories:
dataset -> MUST be present in the same directory as this program.
	   Holds the training dataset: reg_dataset.csv

models  -> Optional, in the same directory as this program, 
	   if does not exist will create itself. 
	   Holds all models that were dumped after running

files:
reg_dataset.csv -> MUST be present within the dataset directory
	           Holds all training values to be used by the model

=======================================================
	How to view decision tree's decisions
cd dotfiles
dot -Tpng graphviz.dot -o pngfile.png

navigate with file explorer to the dotfiles folder and 
open the newly created pngfile.png file

