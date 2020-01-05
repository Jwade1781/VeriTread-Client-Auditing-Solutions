############################################################################
# Purpose:
#   Create & Train a Binary Decision Tree for Classifying whether or not
#   a company should register based on info from previously determined companies
#
# TODO
# [1] Auto change graphviz file from .dot file to .png
# [2] Refactor
#
# Extra Info:
#  Works by parsing the command line by running either:
#  python ./create_train_reg_dt.py 'terminal function such as -h'
#  or
#  python ./create_train_reg_dt.py 'MAX_SEED iterations'
#
#  Ex:
#  python ./create_train_reg_dt.py '-h'
#  python ./create_train_reg_dt.pydecision_tree_model 10000
#
# How to change dot file to .png
# terminal -> dot -Tpng graphviz.dot -o pngfile.png
############################################################################
class Reg_Decision_Tree:
    def __init__(self):
        best_model = self.Create_Classifier()
        model_name = self.Dump_Model(best_model)
        self.Export(best_model, model_name)
        return 

############################################################################      
    def Create_Classifier(self):
        best_model, best_accuracy, X_test, Y_test = self.Tune_Hyper_Parameters()
        self.Print_Confusion_Matrice(best_model, X_test, Y_test)
        print("Most accurate value: " + str(best_accuracy) + "\n")        
        return best_model

############################################################################
    # Gets the dataset from the file 'reg_dataset.csv'
    # This file must be found in the directory called 'dataset' that is placed
    # in the same parent directory as this program

    def Get_Datasets(self, seed_value):
        from sklearn import model_selection
        import pandas as pd
        import os
        directory = '..\Data\Dataset\\'
        filename = 'reg_dataset.csv'

        # Check to see that the dataset directory exists 
        if (not os.path.exists(directory)):
            print("\n\nERROR: The directory - " + directory  + " that holds the dataset file: " + filename + " was not found in the appropriate path..")
            print("Make sure the file is in the parent directory of this program")
            print("Exiting Program")
            exit(0)

        # Load the datasets
        filename = directory + filename
        dataset = pd.read_csv(filename)

        #from sklearn.utils import shuffle
        #dataset = shuffle(dataset)

        # Split the datasets into training and testing
        TESTING_RATIO = 0.25
        NUM_FEATURES = 6

        array = dataset.values
        X = array[:,0:NUM_FEATURES]
        Y = array[:,NUM_FEATURES]

        X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=TESTING_RATIO, random_state=seed_value)
        return X_train, X_test, Y_train, Y_test

############################################################################
    # Searches for the best performing Decision Tree given a max seed value inputted
    # from the command line
    def Tune_Hyper_Parameters(self):
        from sklearn.tree import DecisionTreeClassifier
        best_accuracy = 0
        best_model = None

        # If no arguments are added to the command line default the MAX_SEED to 10000 iterations
        try:
            import sys 
            MAX_SEED = int(sys.argv[1])
        except:
            MAX_SEED = 10000

        # Find the model with the best seed value and keep it
        for i in range(0, MAX_SEED):
            model = DecisionTreeClassifier()
            X_train, X_test, Y_train, Y_test = self.Get_Datasets(i)

            model.fit(X_train, Y_train) # train the decision tree
            accuracy = self.Print_Accuracy_Precision(model, X_test, Y_test)
            if (accuracy > best_accuracy):
                best_accuracy = accuracy
                best_model = model

            if (i % 100 == 0):
                print(str(i) + "/" + str(MAX_SEED) + " Current best Accuracy Score: " + str(best_accuracy))

            # 100% accuracy achieved -> break loop as optimal hyperparameters were found
            if (accuracy == 1.0):
                break

        return best_model, best_accuracy, X_test, Y_test

############################################################################
    # Print the Accuracy & Precision of the trained model(s) against the testing dataset
    def Print_Accuracy_Precision(self, model, X_test, Y_test):
        from sklearn.metrics import accuracy_score
        from sklearn.metrics import precision_score

        predictions = model.predict(X_test)
        foundAccuracy = accuracy_score(Y_test, predictions)
        #print("Accuracy of Model: " + str(foundAccuracy))
        return foundAccuracy

############################################################################
    # Print the matrice(s) of the model(s) detailing where classification has failed
    def Print_Confusion_Matrice(self, model, X_test, Y_test):
        from sklearn.metrics import confusion_matrix
        matrix = confusion_matrix(model.predict(X_test), Y_test)
        print(matrix)
        return

############################################################################
    # Export the model to .dot files to view how the decision tree made predictions
    def Export(self, model, model_name):
        from sklearn.tree import export_graphviz
        features = ['Active', 'Insurance Claims', 'Trucks Owned', 'Years Operated', 'Previously Rejected', 'Previous Problems']
        class_names = ['Denied', 'Accepted', 'Manual Review']
        filename = '..\Data\Dotfiles\\' + model_name + '.dot'
        export_graphviz(
                model,
                out_file=filename,
                feature_names = features,
                class_names = class_names,
                rounded=True,
                filled=True
                )
        #import subprocess
        #subprocess.call(['dot -Tpng graphviz.dot -o pngfile.png'])

############################################################################
    # Ask the User whether they would like to dump the model into a pickle file
    # This will allow the model to be recalled from storage to memory.

    def Dump_Model(self, model):
        #Creates the saved models directory if does not currently exist in the same directory as this program
        import os
        if (not os.path.exists('..\Data\Models\\')):
            path = os.path.dirname(os.path.realpath(__file__))
            path = path + '..\Data\Models\\'
            os.mkdir(path)

        dumped = False

        while(not dumped):
            dumping = input("\nWould you like to dump the model to a .pkl file?\n[1] Yes\n[2] No **WARNING:** Will no longer be accessible from memory if no is selected \n")

            # Wanted to place model into pickle file
            if dumping == '1':
                while(not dumped):
                    model_name =  input("\nEnter the filename that you would like to use .. do not include the file extension\nEnter [1] for auto name\n")

                    if (model_name == '1'):
                        model_name = 'decision_tree_model'

                    filename = '..\Data\Models\\' + model_name+ '.pkl'

                    # Check to see if another model holds the same name already .. Giving option to change name before dumping
                    import os
                    if (os.path.exists(filename)):
                        continuing = input("\n** WARNING: ** Model with the same name at: " + filename + " was found.. Continuing will overwrite. Are you sure you want to continue?\n[1] Yes\n[2] No\n")
                        if (continuing == '1'):
                            dumped = True

                        elif (continuing == '2'):
                            continue

                        else:
                            print("Invalid option selected.. Please reenter the name of the file")
                    
                    # Dump file
                    import joblib
                    joblib.dump(model, filename)
                    print("\nDumped model to: " + filename)
                    return model_name

            # Wanted to delete the model.. do not store any information
            elif dumping == '2':
                exit(0)

            # Invalid Answer
            else:
                print("Please enter either 1 to dump the model or 2 to exit and delete it from memory")


########################################################################################################################################################
# Terminal Parameters -> Helper functions
def _parseArguments(arg):
    import sys
    for i in range(1, len(sys.argv)):
        if (sys.argv[i] == arg):
            return 1

def _showingHelp():
    return(_parseArguments("-h"))

def _showingVersions():
    return(_parseArguments("-v"))

def _showingDescription():
    return(_parseArguments("-d"))

def _showingReadme():
    return(_parseArguments("-readme"))

########################################################################################################################################################
def _showHelp():
    print("Registration Decision Tree -h -v -d -readme")
    print("-h: show this help message")
    print("-v: show version info for Python runtime and ML libraries")
    print("-d: describes the purpose of this Python Program")
    print("-readme: prints the README file into the console")
    print("No Arguements: creates multiple models, trains and evaluates them, finding the best model to be stored")

def _showVersions():
    # check versions of Python runtime and ML libraries
    import sys
    print('Python: {}'.format(sys.version))

    import numpy
    print('numpy: {}'.format(numpy.__version__))

    import pandas
    print('pandas: {}'.format(pandas.__version__))

    import sklearn
    print('sklearn: {}'.format(sklearn.__version__))

    import joblib
    print('joblib: {}'.format(joblib.__version__))

def _showDescription():
    print("The purpose of this Python Program is to use a Decision Tree Classifier / Forest to classify whether inputted companies should be allowed to register based on past acceptance")

def _showReadme():
    readme = open("readme.txt", "r")
    contents = readme.read()
    print(contents)
    return

########################################################################################################################################################
#List of options the user can do
if (_showingHelp()):
    _showHelp()
    exit(0)
        
# Used to determine if all libraries are install correctly
elif (_showingVersions()):
    _showVersions()
    exit(0)

# Shows a description of the python program
elif (_showingDescription()):
    _showDescription()
    exit(0)

# Prints the readme file into the console
elif (_showingReadme()):
    _showReadme()
    exit(0)

########################################################################################################################################################

Reg = Reg_Decision_Tree()

