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

        continuation_model = lambda x: x * 0 # trick needed for broadcasting to work

        token.policy[token.cursor] = True

        token.value[token.cursor] = token.offers[token.cursor]

        token.layer_payload[token.cursor] = continuation_model


class LangStaffLayer(LangStaffAbstract):

# TODO: change token.coord[token.cursor] into token.get_current_coords()
    def update(self, token):
        token.continuation[token.cursor] = token.value[token.get_precedent_cursor()]

        continuation_model = self.regression_model.fit(token.coords[token.cursor], token.continuation[token.cursor])

        continuation_model_evaluated = continuation_model(token.coords[token.cursor])

        token.policy[token.cursor] = token.offers[token.cursor] > continuation_model_evaluated

        token.value[token.cursor] = token.policy[token.cursor] * token.offers[token.cursor] \
                                    + np.logical_not(token.policy[token.cursor]) * token.continuation[token.cursor]

        token.layer_payload[token.cursor] = continuation_model


class LangStaffTerminal(LangStaffAbstract):
    def update(self, token):
        token.continuation[token.cursor] = np.average(token.value[token.get_precedent_cursor()])
        token.policy[token.cursor] = token.offers[token.cursor] > token.continuation[token.cursor]
        token.value[token.cursor] = np.maximum(token.continuation[token.cursor], token.offers[token.cursor])
        # no payload

    pass


class BinomialInitial(Layer):
    def update(self, token):
        token.continuation[token.cursor] = 0.0

        token.policy[token.cursor] = True

        token.value[token.cursor] = token.offers[token.cursor]


class Binomial(Layer):
    def update(self, token):
        token.continuation[token.cursor] = token.value[token.get_precedent_cursor()]

        continuation_model = self.regression_model.fit(token.coords[token.cursor], token.continuation[token.cursor])

        continuation_model_evaluated = continuation_model(token.coords[token.cursor])

        token.policy[token.cursor] = token.offers[token.cursor] > continuation_model_evaluated

        token.value[token.cursor] = token.policy[token.cursor] * token.offers[token.cursor] \
                                    + np.logical_not(token.policy[token.cursor]) * token.continuation[token.cursor]

        token.layer_payload[token.cursor] = continuation_model
