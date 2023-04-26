import numpy as np
import config as config
from Utility.Regressions.Regression import Regression


class Polynomial(Regression):

    def __init__(self, param=config.default["degree"]):
        super().__init__(param)
        self.param = param

    def fit(self, source, target):  # here param is the degree

        p = np.polynomial.Polynomial.fit(source, target, self.param)
        return p

    def can_fit(self, source, target):
        return len(source) > self.param
