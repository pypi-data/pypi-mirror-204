# Algorithm Selection Portfolio with ML

This project shows an algorithm selection library using ML based on the scikit-learn library.

### Context

This project arose after the writing of the paper [Learning for Spatial Branching: An Algorithm Selection Approach](https://arxiv.org/abs/2204.10834)

> The use of machine learning techniques to improve the performance of branch-and-bound optimization algorithms is a very active area in the context of mixed integer linear problems, but little has been done for non-linear optimization. To bridge this gap, we develop a learning framework for spatial branching and show its efficacy in the context of the Reformulation-Linearization Technique for polynomial optimization problems.

This library is intended to generalize the analysis performed in the above-mentioned paper. It analyzes multiple algorithms on a set of problems, defined by their features, and seeks to provide a series of metrics and graphs to compare their performance. Not only compares the performance of the algorithms on the dataset, but also provides a learning-based solution of the optimal choice of algorithm based on the problem's features.

### Table of Contents
- [Introduction](#Introduction)

- [ML module](#ML-module)

- [Plots module](#Plots-module)

- [Execution example](#Execution-example)  

## Introduction
Thanks to this library you will be able to run the training and prediction 
of several models at once, preprocess the data and generate a performance 
measure based on the maximization or minimization of the generated output.
In addition, three functions are included to generate comparison plots of 
the options to be analyzed.
Therefore, starting from two data sets x and y (containing x the 
characteristics of the problems to be used and y the generated output) 
this library is able to:
- Create the test sets.
- Normalize the output (the user can choose between maximization or 
minimization).
- Train the necessary models.
- Create the prediction for the previously generated test sets and models.
- Create various plots that facilitate the understanding of the results.

## ML module

The following is a list of the functions included in the ML module:

### data_processing
Preprocesses the data according to the parameters set by the user and 
returns the training sets and test sets.

The x parameter (dataframe) contains the problems (rows) and its features 
(columns) and the y parameter (dataframe) contains the outputs. Each 
column is an option. The segmentation will be done based on the test_size 
value, which indicates the percentage of instances in the test data. If 
normalize parameter is True the output (y_train and y_test) will take 
values between 0 and 1, being 1 the best option. The parameter 
better_smaller indicates the option to choose during normalization, 
minimize or maximize.

### train_as
Trains multiple models using the method passed as parameter. It is based 
on sklearn library.

The output will have as many models as options to be evaluated.
The x parameter (dataframe) contains the problems (rows) and its features 
(columns) and the y parameter (dataframe) contains the outputs. The method 
parameter indicates the name of the sklearn method to be used for the 
training. The user can introduce all the parameters accepted by the 
method, see sklearn documentation for more information.

### predict_as
Generates the predictions from the models passed as parameters. This 
function is based on the sklearn library.

The models parameter contains the path to the models saved during the 
training process. The data parameter contains the new data to use for the 
prediction (for example x_test). The option_names parameter contains the 
name of the options that the user is evaluating (headers of y_train).

### algorithm_portfolio
Creates the potfolio with the best option for each instance (compared with 
the true optimal option).
This function should be used with normalized data. If there is a tie all 
the optimal options will be shown.

The y_pred dataframe is used to create the ML_value and ML_option_name 
columns and the y_test dataframe is used for the Optimal_solution column. 
For each row the closest value to 1 will be selected.

## Plots module
The following is a list of the functions included in the plots module:

### boxplot
Represents the boxplot taking into account the number of times each option 
is selected as the best. It should be used with the normalized data. The 
ML box is also created by selecting the best option for each instance 
(i.e. the closest value to one after normalizing). Each box will represent 
the number of times that the option was selected as the best.

### performance_comparison_plot
Creates the bar plot or the stacked bar plot that represent percentage of 
times (percentage of problems) that each option is selected by ML compared 
with the optimal solution. In other words, it compares the number of times 
that the ML selects the best possible option.

### ranking_plot
This function generates a plot where, for each instance, the branching 
rules are ranked from best to worst, according to the normalized output. 
Stacked bar graphs represent percentage of problems in each rank position 
per option. It should be used with the normalized data.

## Execution example

If you want to try the library an example python script and two csv files 
are provided. You just have to execute:

    python3 example.py
The output will be the images of the three generated plots and will be 
stored in the path where the example.py file is located. In addition, a 
model will be generated for each option and stored in the models folder.
If you wish to see the obtained results, it is enough to add the following 
lines of code:

Option 1 (prints the best solution for each problem obtained by ML):

    res=ml.algorithm_portfolio(y_test,y_pred)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	    print(res)

Option 2 (prints the predictions generated by ML):

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	    print(y_pred)

## Developers
- Caseiro Arias, María
- Gómez Casares, Ignacio
- González Díaz, Julio
- González Rodríguez, Brais
- Pateiro López, Beatriz
