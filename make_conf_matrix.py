__author__ = "Michał Podolec"

import pandas as pd
import pickle
from evolution import Evolution
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

if __name__ == "__main__":
    ## choose desired validation dataset '.csv'
    test_df = pd.read_csv("airline-passenger-satisfaction/test.csv")
    ## choose desired, already generated tree from '.sav' file
    best_tree = pickle.load(open("airline-passenger-satisfaction/evolution-satisfaction-100-real-no-crossing.best.tree.sav", 'rb'))

    proper, predicted = Evolution.fitness_for_conf_mtx(best_tree, test_df)
    conf_matrix = confusion_matrix(proper, predicted)

    print(conf_matrix)

    ax = sns.heatmap(conf_matrix/np.sum(conf_matrix), annot=True, fmt='.2%', cmap='Blues')

    ax.set_title('Airline-satisfaction (TM)')
    ax.set_xlabel('Predicted Values')
    ax.set_ylabel('Actual Values ')

    ## Ticket labels - List must be in alphabetical order
    labels = ['neutral or dissatisfied', 'satisfied']
    ax.xaxis.set_ticklabels(labels)
    ax.yaxis.set_ticklabels(labels)

    ## Display the visualization of the Confusion Matrix.
    plt.show()
