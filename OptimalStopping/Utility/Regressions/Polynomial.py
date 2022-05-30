import numpy as np
import OptimalStopping.config as config

from OptimalStopping.Utility.Regressions.Regression import Regression


class Polynomial(Regression):

    def __init__(self, param=config.default["degree"]):
        super().__init__(param)
        self.param = param

    def fit(self, coord, target):  # here param is the degree

        p = np.polynomial.Polynomial.fit(coord, target, self.param)
        return lambda x: np.maximum(0, p(x))
    # TODO: send in the actual result, not a lambda

    def can_fit(self, coord, targets):
        return len(coord) > self.param
