from Node import *
from random import randint
import pandas as pd
from tqdm import tqdm
import pickle

class Evolution:

    def cross(tree1, tree2):
        level = randint(1, 3)
        to_do_1 = "tree1"
        to_do_2 = "tree2"
        for lev in range(level):
            side_num = randint(0,1)
            side = "right" if side_num == 0 else "left"
            to_do_1 = to_do_1 + "." + side
            to_do_2 = to_do_2 + "." + side

        temp1 = eval(to_do_1)
        temp2 = eval(to_do_2)

        to_do_1 = to_do_1 + " = temp2"
        to_do_2 = to_do_2 + " = temp1"

        exec(to_do_1)
        exec(to_do_2)

        return tree1, tree2


    def mutation(tree, data_dict):
        level = randint(0, 6)
        to_do = "tree"

        for lev in range(0, level, 2):
            side_num = randint(0, 1)
            side = "right" if side_num == 0 else "left"
            to_do = to_do + "." + side

        new_rule, new_value = Node.get_random_rule(data_dict)
        to_do_rule = to_do + ".rule = new_rule"
        to_do_value = to_do + ".value = new_value"

        exec(to_do_rule)
        exec(to_do_value)
        return tree

    def fitness(tree, train_df):
        correct = 0
        incorrect = 0
        for i in tqdm(range(train_df.shape[0])):
            if tree.predict(train_df.iloc[i]) == train_df.iloc[i]['satisfaction']:
                correct = correct + 1
            else:
                incorrect = incorrect + 1
        grade = correct / (incorrect + correct)
        print(grade)
        return grade

if __name__ == "__main__":

    train_df = pd.read_csv("airline-passenger-satisfaction/test.csv")
    train_df.drop("Unnamed: 0", inplace=True, axis=1)
    result_dict, classes = Node.create_dictionary_from_df(train_df)


    # population = Node.get_init_population(20, result_dict, classes)
    # pickle.dump(population, open("population.sav", 'wb'))

    population = pickle.load(open("population.sav", 'rb'))
    # population[0].print_tree()
    population[0].print_tree()
    # Evolution.fitness(population[0], train_df)
