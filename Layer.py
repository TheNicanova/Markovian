import numpy as np
import Token

from Regression import *


class Layer:

    def update(self, token):
        pass

    @classmethod
    def wrap(cls, n, params=None):
        return [cls(params) for i in range(n)]


class LangStaffAbstract(Layer):
    def __init__(self, regression_model=None):
        if regression_model is None:
            regression_model = PolynomialRegression()
        self.regression_model = regression_model


class LangStaffInitial(LangStaffAbstract):

    def update(self, token):
        token.continuation[token.cursor] = 0.0

        token.policy[token.cursor] = True

        token.value[token.cursor] = token.offers[token.cursor]

        surface = token.offer.payoff

        return surface

class LangStaffLayer(LangStaffAbstract):

    def update(self, token):
        token.continuation[token.cursor] = token.value[token.get_precedent_cursor()]

        surface = self.regression_model.fit(token.coords[token.cursor], token.continuation[token.cursor])

        token.policy[token.cursor] = token.offers[token.cursor] > surface(token.coords[token.cursor])

        token.value[token.cursor] = token.policy[token.cursor] * token.offers[token.cursor] \
                                  + np.logical_not(token.policy[token.cursor]) * token.continuation[token.cursor]
        return surface

class LangStaffTerminal(LangStaffAbstract):
    pass