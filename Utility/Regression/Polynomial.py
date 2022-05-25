import _config
import Utility.Regression.Regression as Interface
import numpy as np


class Polynomial(Interface.Regression):

    def __init__(self, param=_config.default["degree"]):
        super().__init__(param)
        self.param = param

    def fit(self, coord, target):  # here param is the degree

        p = np.polynomial.Polynomial.fit(coord, target, self.param)
        return lambda x: np.maximum(0, p(x))
    # TODO: send in the actual result, no a lambda

    def can_fit(self, coord, targets):
        return len(coord) > self.param
