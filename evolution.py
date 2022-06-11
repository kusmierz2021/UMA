__author__ = "Rafał Kuśmierz, Michał Podolec"

from Node import *
from random import randint
import pandas as pd
from tqdm import tqdm
import pickle

from sklearn.model_selection import train_test_split



class Evolution:
    BEST_TREE = None
    BEST_RATE = None

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
        for mut in range(5):
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

    @staticmethod
    def fitness(tree, train_df):
        correct = 0
        incorrect = 0
        # for i in tqdm(range(train_df.shape[0])):
        for i in tqdm(range(0, len(train_df))):
        # for i in range(1000, 3000):
            if tree.predict(train_df.iloc[i]) == train_df.iloc[i]['Drug']:
                correct = correct + 1
            else:
                incorrect = incorrect + 1
        grade = correct / (incorrect + correct)
        return grade

    def tournaments(population_rates, size=3):
        new_population = []
        while True:
            tournament = []
            for i in range(size):
                x = randint(0, len(population_rates)-1)
                tournament.append(population_rates[x])
            best_rate = -1
            for i in range(len(tournament)):
                if tournament[i][1] > best_rate:
                    best_rate = tournament[i][1]
                    best_tree = tournament[i][0]
            new_population.append(best_tree)
            if len(new_population) == (len(population_rates)-1):
                new_population.append(Evolution.BEST_TREE)
                return new_population

    @staticmethod
    def crossing(population):
        population_after_crossing = []
        for i in range(10):
            t1 = randint(0, len(population)-1)
            tree1 = population.pop(t1)
            t2 = randint(0, len(population) - 1)
            tree2 = population.pop(t2)
            tree1, tree2 = Evolution.cross(tree1, tree2)
            population_after_crossing.append(tree1)
            population_after_crossing.append(tree2)

        return population_after_crossing

    @staticmethod
    def train(iterations, population, train_df, result_dict):
        if Evolution.BEST_TREE is None:
            Evolution.BEST_TREE = population[0]
            Evolution.BEST_RATE = Evolution.fitness(Evolution.BEST_TREE, train_df)
        for i in range(iterations):
            rates_list = []
            for i in range(len(population)):
                rate = Evolution.fitness(population[i], train_df)
                if rate > Evolution.BEST_RATE:
                    Evolution.BEST_RATE = rate
                    Evolution.BEST_TREE = population[i]
                    pickle.dump(Evolution.BEST_TREE, open("evolution-drugs-random.best.tree.sav", 'wb'))
                rates_list.append(rate)
            population_rates = list(zip(population, rates_list))

            population = Evolution.tournaments(population_rates)
            population = Evolution.crossing(population)
            population = [Evolution.mutation(x, result_dict) for x in population]
            print(Evolution.BEST_RATE)
        return population, Evolution.BEST_TREE



if __name__ == "__main__":

    df = pd.read_csv("DrugsABCXY/train.csv")
    # # line for deleting unnecessary columns ? if needed
        # train_df.drop("Unnamed: 0", inplace=True, axis=1)
        # train_df = train_df.drop("id", axis=1)

    result_dict, classes = Node.create_dictionary_from_df(df)

    # # init of population if yet not exist
        # population = Node.get_init_population(20, result_dict, classes)
        # pickle.dump(population, open("population.sav", 'wb'))

    population = pickle.load(open("population-drugs.sav", 'rb'))
    train_df = pd.read_csv("DrugsABCXY/train.csv")

    # # division dataset for test and training subsets
        # train_df, test_df = train_test_split(df, test_size=0.2)
        # train_df.to_csv('train.csv', index=False)
        # test_df.to_csv('test.csv', index=False)

    population = Evolution.train(1, population, train_df, result_dict)

    # pickle.dump(population, open("last_population-wine.sav", 'wb'))

