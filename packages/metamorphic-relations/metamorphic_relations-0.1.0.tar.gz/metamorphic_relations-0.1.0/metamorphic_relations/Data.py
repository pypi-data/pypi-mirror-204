import numpy as np
import random


class Data:
    """
    Stores the data

    :param train_x: a numpy array, the first dimension is the index of elements for training
    :param train_y: a 1D numpy array of label indices for training
    :param test_x: a numpy array, the first dimension is the index of elements for testing
    :param test_y: a 1D numpy array of label indices for testing
    :param max_y: the largest y value possible
    """

    def __init__(self, train_x: np.array, train_y: np.array, test_x: np.array, test_y: np.array, max_y: int):

        self.train_x = train_x
        self.train_y = train_y
        self.test_x = test_x
        self.test_y = test_y

        self.train = (train_x, train_y)
        self.test = (test_x, test_y)

        self.max_y = max_y

        self.shuffle_train()

    def update_train(self, train_x: np.array, train_y: np.array):
        """
        Updates the training data

        :param train_x: new training x data
        :param train_y: new training y data
        """

        if len(train_x) != len(train_y):
            raise Exception("train_x and train_y must be of the same length")

        self.train_x = train_x
        self.train_y = train_y
        self.train = (train_x, train_y)

    def shuffle_train(self):
        """
        Rearranges the order of the training data
        """

        train_data = list(zip(self.train_x, self.train_y))
        random.shuffle(train_data)

        train_x = [train[0] for train in train_data]
        train_y = [train[1] for train in train_data]

        train_x = np.array(train_x)
        train_y = np.array(train_y)

        self.update_train(train_x, train_y)

    def update_test(self, test_x: np.array, test_y: np.array):
        """
        Updates the testing data

        :param test_x: new testing x data
        :param test_y: new testing y data
        """

        if len(test_x) != len(test_y):
            raise Exception("test_x and test_y must be of the same length")

        self.test_x = test_x
        self.test_y = test_y
        self.train = (test_x, test_y)

    @staticmethod
    def concat_lists(lists: list[tuple[np.array, np.array]]) -> tuple[np.array, np.array]:
        """
        Takes a list of pairs of numpy arrays of xs and ys and makes them a single xs and ys list

        :param lists: a numpy array of pairs of numpy arrays of xs and ys e.g. [[xs1, ys1], [xs2, ys2]]
        :return: a tuple of xs and ys e.g. (xs1 + xs2, ys1 + ys2)
        """

        if len(lists[0]) != 2:
            raise Exception("The input must have exactly 2 elements in the second dimension")

        xs = np.zeros(tuple([0] + list(lists[0][0].shape)[1:]))
        ys = np.zeros((0,), dtype=int)

        for i in range(len(lists)):

            if len(lists[i][0]) != len(lists[i][1]):
                raise Exception("Each pair of xs and ys must have the same length")

            xs = np.concatenate((xs, lists[i][0]))
            ys = np.concatenate((ys, lists[i][1]))

        return np.array(xs), np.array(ys)

    @staticmethod
    def group_by_label(y: np.array, max_y: int) -> list[list[int]]:
        """
        Groups an array of ints by their values.
        E.g. ([3, 3, 2, 3, 1, 0], 5) -> [[5], [4], [2], [0, 1, 3], []]

        :param y: a numpy array of ints
        :param max_y: the maximum possible number of values
        :return: a list of y indices for each possible y value
        """

        group_indices = [[] for _ in range(max_y)]

        for i in range(y.shape[0]):

            if y[i] < 0:
                raise Exception("y values must be positive")
            elif y[i] > max_y:
                raise Exception("max y must be at least as large as the largest y value given")

            group_indices[y[i]].append(i)

        return group_indices

    def get_train_subset(self, i_min: int = 0, i_max: int = 9999999) -> tuple[np.array, np.array]:
        """
        Gets a subset of the training data

        :param i_min: the lower bound index (inclusive)
        :param i_max: the upper bound index (not inclusive)
        :return: train_x_subset, train_y_subset
        """

        return self.train_x[i_min:i_max], self.train_y[i_min:i_max]
