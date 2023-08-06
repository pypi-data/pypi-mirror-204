from algorithmselector.ml import algorithm_portfolio

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import statistics as st


def boxplot(path,y_pred,y_test):

    """
    Represents the boxplot taking into account the number of times each option is selected as the best. It should be used
    with the normalized data. The ML box is also created by selecting the best option for each instance (i.e. the closest
    value to one after normalizing). Each box will represent the number of times that the option was selected as the best.

    The result image is saved at path. The y_pred dataframe is used to create the ML box and the y_test dataframe
    is used for the other boxes. They will be passed to the algorithm_portfolio function, which will return the best
    option for each instance.
    """

    #select the best option for each problem
    df=y_test.copy()
    selected = [np.argmax(y_pred.iloc[i,:]) for i in range(y_pred.shape[0])]
    df["ML_sel"] = [y_test.iloc[i][selected[i]] for i in range(y_test.shape[0])]
    plt.rcParams["figure.figsize"] = (12,7)

    #prepare the plot
    sns.set()
    sns.set_style("darkgrid", {"axes.facecolor": ".9"})
    flierprops = dict(marker='o', markerfacecolor='.2', markersize=4,  markeredgecolor='black')
    sns.boxplot(data=df, whis=1.5,flierprops=flierprops)

    plt.title("Boxplot Comparison")
    plt.tight_layout()

    plt.savefig(path)

def performance_comparison_plot(path,y_pred,y_test):

    """
    Creates the bar plot or the stacked bar plot that represent percentage of times (percentage of problems) that
    each option is selected by ML compared with the optimal solution. In other words, it compares the number of times
    that the ML selects the best possible option.

    The result image is saved at path. The y_pred dataframe is used to create the ML_option column and the y_test dataframe
    is used for the Optimal_solution column. Best solution for each instance will be selected.
    """

    df=pd.DataFrame()
    options=y_pred.columns.values
    #select the best option for each problem with the predicted data
    df['ML_option'] = [options[np.argmax(y_pred.iloc[i,:])] for i in range(y_pred.shape[0])]
    #select the best option for each problem with the test data (real result)
    df['Optimal_solution'] = [options[np.argmax(y_test.iloc[i,:])] for i in range(y_test.shape[0])]

    plt.rcParams["figure.figsize"] = (22,10)
    sns.set()
    sns.set_style("darkgrid", {"axes.facecolor": ".9"})

    #count the number of occurrences of each algorithm for each method
    counts = df.apply(pd.Series.value_counts)
    counts = counts.T

    #calculate the percentage of problems solved by each algorithm for each method
    percentages = counts.apply(lambda x: x / x.sum(), axis=1)

    ax = percentages.plot.bar(stacked=True, figsize=(8, 6))
    #set the title and axis labels
    ax.set_title('Algorithm Performance Comparison')
    #show the legend
    ax.legend(title='Option', bbox_to_anchor=(0.5, 0.5))
    #format the y-axis tick labels as percentages
    ax.yaxis.set_ticks([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

    plt.savefig(path)

def ranking_plot(path,y_pred,y_test):

    """
    This function generates a plot where, for each instance, the branching rules are ranked from best to worst, according to the
    normalized output. Stacked bar graphs represent percentage of problems in each rank position per option. It should be used with the
    normalized data.

    The result image is saved at path. The y_pred dataframe is used to create the ML_option column and the y_test dataframe
    is used for the other columns.
    """

    #rank the algorithms for each problem
    ranked = y_test.rank(axis=1, method='min', ascending=False)
    ml = pd.DataFrame()
    #get the real output value for each option selected in ml
    selected = [np.argmax(y_pred.iloc[i,:]) for i in range(y_pred.shape[0])]
    ml['ML'] = [y_test.iloc[i][selected[i]] for i in range(y_test.shape[0])]

    #get the ranking that each option of ml has in ranked dataframe (this way the ml data does not affect the ranking)
    mls = pd.DataFrame()
    mls = [ranked.iloc[i,np.argmax((y_test == ml.values).iloc[i])] for i in range(ranked.shape[0])]
    ranked['ML'] = mls
    plt.rcParams["figure.figsize"] = (22,10)
    plt.rcParams['font.size'] = 2
    sns.set()
    sns.set_style("darkgrid", {"axes.facecolor": ".9"})

    #create the stacked bar plot
    fig, ax = plt.subplots(figsize=(8,6))
    #set up the colormap
    colors = plt.cm.get_cmap('prism_r', len(y_test.columns.values))

    #iterate over the sorted algorithms and plot each bar
    for i, opt in enumerate(ranked.columns.values):
        ax.bar(x=ranked.columns, height=(ranked == i+1).sum() / len(ranked), bottom=(ranked <= i).sum() / len(ranked),
            color=colors(i), width=0.9, alpha=0.4, label=opt)

    #.patches is everything inside of the chart
    for rect in ax.patches:
        #find where everything is located
        height = rect.get_height()
        width = rect.get_width()
        #the height of the bar is the data value and can be used as the label
        label_text = f'{height:.2f}' #to format decimal values
        #plot only when height is greater than specified value
        if height > 0.02:
            ax.text(rect.get_x() + width / 2, rect.get_y() + height / 2, label_text, ha='center', va='center', fontsize=8)
    ax.yaxis.set_ticks([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])

    plt.savefig(path)
