import algorithmselector.ml as ml
import algorithmselector.plots as plots

import pandas as pd
from sklearn.metrics import mean_squared_error

# loading the example data
x = pd.read_csv("x_example_data.csv", index_col=False)
x.drop(columns=x.columns[0], inplace=True, axis=1)
y = pd.read_csv("y_example_data.csv", index_col=False)
y.drop(columns=y.columns[0], inplace=True, axis=1)

#data processing
x_train, x_test, y_train, y_test = ml.data_processing(x,y, test_size=0.3, normalize=True, better_smaller=True)

#create and train the model
method_name = 'RandomForestRegressor'
trainedModels=ml.train_as(x_train, y_train, method_name, n_estimators=300, min_samples_split=16)
#predictions
y_pred=ml.predict_as(models=trainedModels, data=x_test, option_names=y_test.columns.values)

############################################

# show the model accuracy
print('\n')
for i in range(y_test.shape[1]):
    mse = mean_squared_error(y_test.iloc[:,i], y_pred.iloc[:,i])
    print(y_pred.columns.values[i]+" MSE: {:.4f}".format(mse))
print('\n')

#create the plots
plots.boxplot('boxplot.png',y_pred,y_test)
plots.performance_comparison_plot('fig_comp.png',y_pred,y_test)
plots.ranking_plot('ranking.png',y_pred,y_test)