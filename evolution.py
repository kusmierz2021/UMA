__author__ = "Rafał Kuśmierz, Michał Podolec"

from node import *
from random import randint
import pandas as pd
from tqdm import tqdm
import pickle


NAME_BEST_TREE_TO_SAVE = "evolution-satisfaction-100-real-no-crossing.best.tree.sav"

class Evolution:
    BEST_TREE = None
    BEST_RATE = None

    @staticmethod
    def cross(tree1, tree2):
        """
        Get two trees and cross them at random point
        :param tree1: first tree to be crossed
        :param tree2: second tree to be crossed
        :return:
        two trees after crossing
        """
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

    @staticmethod
    def mutation(tree, data_dict):
        """
        Get tree and make mutation
        :param tree: tree to be mutate
        :param data_dict: dictionary - key = column_name, value = set of values in column - needed to random rule and its value
        :return:
        modified tree
        """
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
    def fitness_for_conf_mtx(tree, train_df):
        """
        Calculate the ratio of good predictions
        :param tree: tree to be grade
        :param train_df: testing data if final grade calculated
        :return:
        proper: list of proper classes
        predicted: list of predicted classes
        """
        correct = 0
        incorrect = 0
        predicted = []
        proper = []
        for i in tqdm(range(0, len(train_df))):
            predicted.append(tree.predict(train_df.iloc[i]))
            proper.append(train_df.iloc[i][-1])
            if tree.predict(train_df.iloc[i]) == train_df.iloc[i][-1]:
                correct = correct + 1
            else:
                incorrect = incorrect + 1
        grade = correct / (incorrect + correct)
        return proper, predicted

    @staticmethod
    def fitness(tree, train_df):
        """
        Calculate the ratio of good predictions
        :param tree: tree to be grade
        :param train_df: training data
        :return:
        grade: the ratio of good predictions
        """
        correct = 0
        incorrect = 0
        for i in range(1000):
        # for i in range(0, len(train_df)):
            if tree.predict(train_df.iloc[i]) == train_df.iloc[i][-1]:
                correct = correct + 1
            else:
                incorrect = incorrect + 1
        grade = correct / (incorrect + correct)
        return grade

    def tournaments(population_rates, size=3):
        """
        Tournament selection
        :param size: amount of trees to take part in single tournament, default 3
        :return:
        next generation of population
        """
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
        """
        Get population and make crossing
        :param population: population to be crossed
        :return:
        population after crossing
        """
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
        """
        make evolution living, while working function saves best tree using NAME_BEST_TREE_TO_SAVE name
        :param iterations: number of iteration of evolution
        :param population: initial population
        :param train_df: training data
        :param result_dict: dictionary - key = column_name, value = set of values in column - needed to random rule and its value
        :return:
        final population
        """
        if Evolution.BEST_TREE is None:
            Evolution.BEST_TREE = population[0]
            Evolution.BEST_RATE = Evolution.fitness(Evolution.BEST_TREE, train_df)
        for i in tqdm(range(iterations)):
            rates_list = []
            for i in range(len(population)):
                rate = Evolution.fitness(population[i], train_df)
                if rate > Evolution.BEST_RATE:
                    Evolution.BEST_RATE = rate
                    Evolution.BEST_TREE = population[i]
                    pickle.dump(Evolution.BEST_TREE, open(NAME_BEST_TREE_TO_SAVE, 'wb'))
                rates_list.append(rate)
            population_rates = list(zip(population, rates_list))

            ## IMPORTANT PART FOR EXPERIMENTS ##
            ## include or exclude different processes by commenting desired line

            population = Evolution.tournaments(population_rates)
            # population = Evolution.crossing(population)
            population = [Evolution.mutation(x, result_dict) for x in population]

            ## END OF EXPERIMENT POSSIBILITIES ##

            ## show actual best classificator via console
            print(Evolution.BEST_RATE)

        return population


if __name__ == "__main__":

    df = pd.read_csv("airline-passenger-satisfaction/train.csv")

    ## two lines for deleting unnecessary columns if needed
    df.drop("Unnamed: 0", inplace=True, axis=1)
    df = df.drop("id", axis=1)
    ##

    ## get classes and values for each column
    result_dict, classes = Node.create_dictionary_from_df(df)

    ## init population if yet not exist
    population = Node.get_init_population(20, result_dict, classes)

    ## to save created population
    # pickle.dump(population, open("population.sav", 'wb'))

    ## to load already created population
    # population = pickle.load(open("populations/population.sav", 'rb'))
    train_df = pd.read_csv("airline-passenger-satisfaction/train.csv")
    train_df.drop("Unnamed: 0", inplace=True, axis=1)
    train_df = train_df.drop("id", axis=1)

    ## division dataset for test and training subsets if yet not exist
        # train_df, test_df = train_test_split(df, test_size=0.2)
        # train_df.to_csv('train.csv', index=False)
        # test_df.to_csv('test.csv', index=False)

    population = Evolution.train(100, population, train_df, result_dict)

    ## we have ability to save last population and start evolution again from that moment
    # pickle.dump(population, open("last_population", 'wb'))
