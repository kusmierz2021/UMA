__author__ = "Rafał Kuśmierz"

import pandas as pd
import numpy as np
from collections import Counter
import random as r
# from random import randint

r.seed(305858)

class Node:
    """
    Class for creating nodes for a decision tree
    """
    CLASS_NUMBER = 0


    def __init__(self, data_dict, classes, depth=None, max_depth=4):
        """
        Inits a tree
        :param data_dict: dictionary - key = column_name, value = set of values in column - needed to random rule and its value
        :param classes: classes to be predicted
        :param depth: depth of node in current tree
        :param max_depth: pax depth of tree
        """
        self.depth = depth if depth else 0

        ## enable random classes, not
        # probability of being leaf

        # x = r.randint(0, 10)
        # if ((x <= 2 or self.depth == max_depth) and self.depth != 0):
        if self.depth == max_depth:
            self.value = Node.get_random_class(classes)
            self.rule = "leaf"
            self.left = None
            self.right = None

            return

        # not being a leaf

        self.rule, self.value = Node.get_random_rule(data_dict)
        self.right = Node(data_dict, classes, self.depth + 1)
        self.left = Node(data_dict, classes, self.depth + 1)

        return

    @staticmethod
    def get_random_class(classes):
        """

        :param classes: classes to be predicted
        :return:
        random class
        """
        x = Node.CLASS_NUMBER % len(classes)
        Node.CLASS_NUMBER = Node.CLASS_NUMBER + 1
        return classes[x]

    @staticmethod
    def get_random_rule(data_dict):
        """
        get random rule and value to comparison
        :param data_dict: dictionary - key = column_name, value = set of values in column - needed to random rule and its value
        :return:
        random rule and value
        """
        x = r.randint(0, len(list(data_dict.keys())) - 1)
        key = list(data_dict.keys())[x]
        rule = key
        x = r.randint(0, len(data_dict[key]) - 1)
        value = data_dict[key][x]
        return rule, value


    def print_info(self, width=4):
        """
        used by print_tree
        :param width: width of indentation for every next node
        """
        # Defining the number of spaces
        # const = int(self.depth * width ** 1.5)
        # spaces = "-" * const

        if self.depth == 0:
            print_in = self.depth * width * "-" + self.rule + " <= " + str(self.value) + '\n'
            print(print_in)
        else:
            print_in = self.depth * width * "-" + self.rule + " <= " + str(self.value) + '\n'
            print(print_in)

    def print_tree(self):
        """
        Print tree
        """
        self.print_info()

        if self.left is not None:
            self.left.print_tree()

        if self.right is not None:
            self.right.print_tree()

    def predict(self, row_dict):
        """
        predicts class for given data row
        :param row_dict: row of dataset to predict class
        :return:
        predicted class
        """
        # print_in = self.depth * 4 * "-" + self.rule + " <= " + str(self.value) + '\n'
        # print(print_in)
        if self.rule == "leaf":
            # print(f"predicted value = {self.value}")
            return self.value
        to_check = row_dict[self.rule]
        if to_check <= self.value:
            return self.left.predict(row_dict)
        else:
            return self.right.predict(row_dict)

    @staticmethod
    def get_init_population(size, result_dict, classes):
        """
        Get init random population
        :param size: size of population
        :param result_dict: dictionary - key = column_name, value = set of values in column - needed to random rule and its value
        :param classes: classes to be predicted
        :return:
        list of individuals
        """
        initial_population = []
        for i in range(size):
            initial_population.append(Node(result_dict, classes))
        return initial_population

    @staticmethod
    def create_dictionary_from_df(train_df):
        """

        :param train_df: training dataset
        :return:
        dictionary - key = column_name, value = set of values in column - needed to random rule and its value
        """
        result_dict = {}
        rules_list = train_df.columns.tolist()

        print(rules_list)
        for rule in rules_list:
            x = train_df[rule].tolist()

            for i in range(len(x)):
                if str(x[i]) == "nan":
                    x[i] = 0
            x = list(dict.fromkeys(x))
            x.sort()
            result_dict[rule] = x
        classes = result_dict[list(result_dict.keys())[-1]]
        result_dict.pop(list(result_dict.keys())[-1])
        return result_dict, classes


if __name__ == "__main__":
    pass