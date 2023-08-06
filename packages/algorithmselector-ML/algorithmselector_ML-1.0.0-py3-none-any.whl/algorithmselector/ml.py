import sklearn.ensemble
import pickle
import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split

def data_processing(x,y,test_size=0.25,normalize=False,better_smaller=True):

    """
    Preprocesses the data according to the parameters set by the user and returns the training sets and test sets.

    The x parameter (dataframe) contains the problems (rows) and its features (columns) and the y parameter (dataframe) 
    contains the outputs. Each column is an option. The segmentation will be done based on the test_size value, which 
    indicates the percentage of instances in the test data. If normalize parameter is True the output (y_train and y_test) 
    will take values between 0 and 1, being 1 the best option. The parameter better_smaller indicates the option to choose 
    during normalization, minimize or maximize.
    """
    
    x_train, x_test, y_train, y_test=train_test_split(x,y, test_size=test_size)
    c=0.001

    if normalize and better_smaller:
        #define lambda function for use with apply
        min_div_val = lambda x: min(x+c) / (x+c)
        #apply function to dataframe
        y_train = y_train.apply(min_div_val, axis=1)
        y_test = y_test.apply(min_div_val, axis=1)

    elif normalize and not better_smaller:
        #define lambda function for use with apply
        max_div_val = lambda x: (x+c)/max(x+c)
        #apply function to dataframe
        y_train = y_train.apply(max_div_val, axis=1)
        y_test = y_test.apply(max_div_val, axis=1)
    
    return x_train, x_test, y_train, y_test

def train_as(x, y, method, **parameters):

    """
    Trains multiple models using the method passed as parameter. It is based on sklearn library. 
    The output will have as many models as options to be evaluated.

    The x parameter (dataframe) contains the problems (rows) and its features (columns) and the y 
    parameter (dataframe) contains the outputs. The method parameter indicates the name of the sklearn 
    method to be used for the training. The user can introduce all the parameters accepted by the method, 
    see sklearn documentation for more information.
    """

    method = getattr(sklearn.ensemble, method)
    if not method:
        raise NotImplementedError("Method not available. Make sure that the name is correct and you have sklearn installed.")
    
    clf=method(**parameters)
    #show the used arguments
    print("Method arguments: ",parameters)
    index=y.shape[1]
    trainedModels={}

    #path where the models will be saved
    isExist = os.path.exists('./models')
    if not isExist:
        os.makedirs('./models')

    for i in range(index):
        #train the model using the training sets 
        model=clf.fit(x,y.iloc[:,i])
        #save the model to disk
        trainedModels[i] = './models/model'+str(i)+'.sav'
        pickle.dump(model, open(trainedModels[i], 'wb'))
    
    return trainedModels

def predict_as(models,data,option_names):

    """
    Generates the predictions from the models passed as parameters. This function is based on the sklearn library.

    The models parameter contains the path to the models saved during the training process. The data parameter 
    contains the new data to use for the prediction (for example x_test). The option_names parameter contains the 
    name of the options that the user is evaluating (headers of y_train).
    """
    
    predictions=pd.DataFrame()

    for i in range(len(models)):
        # load the model from disk
        loaded_model = pickle.load(open(models[i], 'rb'))
        # Predict on new data 
        predictions[str(option_names[i])] = loaded_model.predict(data)

    return predictions

def algorithm_portfolio(y_test,y_pred):

    """
    Creates the potfolio with the best option for each instance (compared with the true optimal option). 
    This function should be used with normalized data. If there is a tie all the optimal options will be shown.

    The y_pred dataframe is used to create the ML_value and ML_option_name columns and the y_test dataframe 
    is used for the Optimal_solution column. For each row the closest value to 1 will be selected.
    """

    res=pd.DataFrame()
    options=y_test.columns.values
    res['ML_value'] = [np.max(y_pred.iloc[i,:]) for i in range(y_pred.shape[0])] 
    res['ML_option_name'] = [options[np.argmax(y_pred.iloc[i,:])] for i in range(y_pred.shape[0])] 
    res['Optimal_solution'] = [options[np.where(y_test.iloc[i,:] == 1)] for i in range(y_test.shape[0])] 
    
    return res