import numpy as np
from config import *

#TODO: Probably best to add a state to regression model containing the params

class Regression():
    def __init__(self, param=default["degree"]):
        self.param = param

    def fit(self, coord, offer_model, param):
        pass

    def is_fittable(self):
        pass

class PolynomialRegression(Regression):
    def fit(self, coord, targets):  # here param is the degree

        p = np.polynomial.Polynomial.fit(coord, targets, self.param)
        return lambda x: np.maximum(0, p(x))

    def is_fittable(self, coord, targets):
        if  len(coord) > self.param:
            return True
        else:
            return False
