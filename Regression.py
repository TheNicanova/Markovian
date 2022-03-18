import numpy as np
from config import *

#TODO: Probably best to add a state to regression model containing the params

class Regression():
    def fit(self, coord, offer_model, param):
        pass


class PolynomialRegression(Regression):
    def fit(self, coord, targets, param=default["degree"]):  # here param is the degree

        p = np.polynomial.Polynomial.fit(coord, targets, param)
        return lambda x: np.maximum(0, p(x))
