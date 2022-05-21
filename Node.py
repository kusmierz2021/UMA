import pandas as pd
import numpy as np
from collections import Counter
from random import randint

def create_dictionary_from_csv(path):
    result_dict = {}
    train_df = pd.read_csv(path)
    rules_list = train_df.columns.tolist()
    rules_list = rules_list[1:]
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


class Node:
    """
    Class for creating nodes for a decision tree
    """

    def __init__(self, data_dict, classes, depth=None, max_depth=5):
        self.depth = depth if depth else 0

        # probability of being leaf
        x = randint(0, 10)
        if ((x <= 2 or self.depth == max_depth) and self.depth != 0):
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
        x = randint(0, len(classes) - 1)
        return classes[x]

    @staticmethod
    def get_random_rule(data_dict):
        x = randint(0, len(list(data_dict.keys())) - 1)
        key = list(data_dict.keys())[x]
        rule = key
        x = randint(0, len(data_dict[key]) - 1)
        value = data_dict[key][x]
        return rule, value

    # def get_rule(self, data_dict, classes, probability=30):
    #     x = randint(1, 100)
    #     if ((x <= 2 or self.depth == max_depth) and self.depth != 0):
    #         x = randint(0, len(classes) - 1)
    #         self.value = classes[x]
    #         self.rule = "leaf"
    #         self.left = None
    #         self.right = None
    #         self.print_in = self.depth * 4 * "-" + self.rule + ": " + self.value
    #         return

    def print_info(self, width=4):
        """
        Method to print the infromation about the tree
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
        Prints the whole tree from the current node to the bottom
        """
        self.print_info()

        if self.left is not None:
            self.left.print_tree()

        if self.right is not None:
            self.right.print_tree()

    def predict(self, row_dict):
        print_in = self.depth * 4 * "-" + self.rule + " <= " + str(self.value) + '\n'
        print(print_in)
        if self.rule == "leaf":
            print(f"predicted value = {self.value}")
            return self.value
        to_check = row_dict[self.rule]
        if to_check <= self.value:
            return self.left.predict(row_dict)
        else:
            return self.right.predict(row_dict)

    @staticmethod
    def get_init_population(size):
        initial_population = []
        for i in range(size):
            initial_population.append(Node(result_dict, classes))
        return initial_population




if __name__ == "__main__":
    result_dict, classes = create_dictionary_from_csv("airline-passenger-satisfaction/train.csv")
    #     tree_1 = Node(result_dict, classes)
    #     tree_2 = Node(result_dict, classes)
    #     tree_3 = Node(result_dict, classes)
    #     tree_4 = Node(result_dict, classes)
    #     tree_5 = Node(result_dict, classes)
    #     tree_6 = Node(result_dict, classes)
    #     tree_7 = Node(result_dict, classes)
    #     tree_8 = Node(result_dict, classes)
    #     tree_9 = Node(result_dict, classes)
    #     tree_10 = Node(result_dict, classes)
    #     initial_population = [tree_1, tree_2, tree_3, tree_4, tree_5, tree_6, tree_7, tree_8, tree_9, tree_10]
    initial_population = Node.get_init_population(10)

    train_df = pd.read_csv("airline-passenger-satisfaction/train.csv")
    train_df.drop("Unnamed: 0", inplace=True, axis=1)

    initial_population[0].predict(train_df.iloc[1])

    print(train_df.iloc[1])
    train_df.iloc[1]['satisfaction']
    initial_population[0].print_tree()
