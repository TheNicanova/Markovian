import numpy as np
from _config import *
from sklearn.neighbors import KNeighborsRegressor


class Regression:

    def __init__(self, param=None):
        self.param = param

    def fit(self, coord, targets):
        pass

    def get_name(self):
        return self.__class__.__name__ + "(" + str(self.param) + ")"


class Polynomial(Regression):

    def __init__(self, param=default["degree"]):
        super().__init__(param)
        self.param = param

    def fit(self, coord, target):  # here param is the degree

        p = np.polynomial.Polynomial.fit(coord, target, self.param)
        return lambda x: np.maximum(0, p(x))

    def is_fittable(self, coord, targets):
        return len(coord) > self.param


class NearestNeighbors1D(Regression):

    def __init__(self, param=default["num_neighbor"]):
        super().__init__(param)
        self.param = param

    def fit(self, coord, target):
        knnr = KNeighborsRegressor(n_neighbors=self.param)
        knnr.fit(np.array(coord).reshape(-1, 1), target)
        return lambda x: knnr.predict([[x]])[0]

    def is_fittable(self, coord, targets):
        return len(coord) > self.param
