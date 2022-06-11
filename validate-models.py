__author__ = "Michał Podolec"

import pandas as pd
import pickle
from evolution import Evolution


if __name__ == "__main__":
    ## loading test.csv from proper folder
    test_df = pd.read_csv("airline-passenger-satisfaction/test.csv")
    ## loading best.tree of desired kind for validation
    best_tree = pickle.load(open("evolution-satisfaction-20-no-crossing.best.tree.sav", 'rb'))

    rate = Evolution.fitness(best_tree, test_df)
    print(rate)
