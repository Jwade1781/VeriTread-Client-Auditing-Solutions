############################################################################
#
# Purpose:
#   Load the stored Decision Tree model from storage into memory and classify
#   a new company based on provided attributes..
#
#
# TODO
# [1 COMPLETE] Determine how the attributes will be inputted into the trained model..
#     can parse arguments from the command line or only require the arguments
#     be the DoT Number of the registering company itself.. With that look
#     for a file containing the DoT number as the name
#
# [2 WIP] Train model with more instances of Previously Rejected -> Currently sees it 
#     as a positive rather than a negative attribute against a company
#
# Extra Info:
#  The file extension of the model does not have to be provided in the command line
#  'auto' can be provided in the model name argument to run the auto named model (decision_tree_model).
#  See below for example for running program in command line
#
# ** Currently works by loading the model from storage and parsing a dot number
#    Can work like this.. but would be more optimal to perhaps have the model
#    Already loaded and the program to poll until a new request is sent. 
#    Depends how often the model has to make predictions. ** 
#
# Run:
# python ./Determine_Elig.py 'model name' 'dot number'
#
# Ex: python ./Determine_Elig.py decision_tree_model 124
############################################################################

def __main():
    from sklearn.tree import DecisionTreeClassifier
    model_name, dot_number = Parse_Command_Line()
    model = Load_Model(model_name)
    dataset = Read_Attributes(dot_number)
    acceptance = Make_Prediction(model, dataset)
    print("\nDot Number: " + dot_number)
    print("Predicted Value: " + acceptance)
    Save_Prediction(dot_number, acceptance)
    return 

############################################################################
# First Argument is the name of the model to use; second is the inputted DoT
# Input 'auto' for the generated auto named model
def Parse_Command_Line():
    import sys
    try:
        model_name = sys.argv[1]
        if (model_name == 'auto'):
            model_name = 'decision_tree_model'

        dot_number = sys.argv[2]
        return model_name, dot_number
    
    except:
        print("\n\n** Error Parsing Command line.. **")
        print("Make Sure that the command line arguments hold the name of the model (can input auto for the auto named model) followed by the DOT Number")
        print("Ex: python ./Determine_Elig.py decision_tree_model 124\n\n")
        exit(0)

############################################################################
# Loads the inputted model from the models directory that is stored in a pkl file
def Load_Model(model_name):
    from sklearn.tree import DecisionTreeClassifier
    import joblib
    try:
        model = joblib.load('..\Data\Models\\' + model_name + '.pkl')
        return model

    except:
        print('\n\n** Error Model Not Found.. **')
        print('The model name inputted was not found ..')
        print('Type \'auto\' as the model name argument if you would like to use the last saved auto named model\n\n')
        exit(0)

############################################################################
# This can be pulled from a SQL database later if it is decided to be stored
# there rather than csv files ..
def Read_Attributes(dot_number):
    import pandas as pd
    directory = '..\Data\Saved_Companies\\'
    filename = directory + dot_number + '.csv'
    dataset = pd.read_csv(filename).values
    return dataset

############################################################################
def Make_Prediction(model, dataset):
    # Makes a prediction based on which model was pulled and the inputted
    # Data of the individual company -> 
    # Returns whether they were accepted, denied, or requires manual review (too many less critical attributes are missing / value 0)
    prediction = model.predict(dataset)
    if (prediction == 0):
        prediction = 'Denied'
    elif (prediction == 1):
        prediction = 'Accepted'
    else:
        prediction = 'manual review'

    return prediction

  ############################################################################
def Save_Prediction(dot_number, acceptance):
    #Save the prediction into a text file that can be opened later
    file = open('..\Data\Saved_Predictions\\' + str(dot_number) + '.txt', 'w+')
    # Write the current time into the text file .. can be used to view when last
    # registration attempt was
    from datetime import datetime
    date_now = datetime.now()
    file.write(date_now.strftime("%d/%b/%Y\n"))
    file.write(acceptance)
    file.close()

__main()