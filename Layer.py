import numpy as np
from Regression import *
class Layer:
  def update(self, data):
    pass

class LangstaffAbstract(Layer):
  def __init__(self, regression_model = PolynomialRegression()):
    self.regression_model = regression_model

class LangstaffInitial(LangstaffAbstract):

  def update(self, data):

    data.continuation[data.cursor] = float('-inf')

    data.policy[data.cursor] = True

    data.value[data.cursor] = data.offers[data.cursor]

    data.update_cursor()

class LangstaffLayer(LangstaffAbstract):

 def update(self, data):

    data.continuation[data.cursor] = data.value[data.get_precedent_cursor()]

    surface = self.regression_model.fit(data.coords[data.cursor], data.continuation[data.cursor])

    data.policy[data.cursor] = data.offers[data.cursor] > surface(data.coords[data.cursor])

    data.value[data.cursor] = data.policy[data.cursor] * data.offers[data.cursor] \
                              + np.logical_not(data.policy[data.cursor]) * data.continuation[data.cursor]
    data.update_cursor()
