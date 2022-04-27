import numpy as np
from config import *


class Regression():
    def __init__(self, param=default["degree"]):
        self.param = param

    def fit(self, coord, targets):
        pass


class PolynomialRegression(Regression):
    def fit(self, coord, targets):  # here param is the degree

        p = np.polynomial.Polynomial.fit(coord, targets, self.param)
        return lambda x: np.maximum(0, p(x))

    def is_fittable(self, coord, targets):
        return len(coord) > self.param
