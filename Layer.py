import numpy as np

class Layer:
  def update(self, data):
    data.cursor = -1 * data.iterationstate - 1
    data.offers[:, data.cursor] = data.offer_model(data.coords[:, data.cursor])

class LangstaffAbstract(Layer):
  def __init__(self, regression_model):
    self.regression_model = regression_model

class LangstaffInitial(LangstaffAbstract):
  def update(self, data):
    super().update(self, data) # updates offers (#1)
    data.continuation[:, data.cursor] = float('-inf')
    data.value[:, data.cursor] = data.offers[:, data.cursor]
    data.policy[:, data.cursor] = True
    data.cursor = data.cursor - 1

class LangstaffLayer(LangstaffAbstract):
 def update(self,data):
    super().update(self,data) # updates offers (#1)
    data.continuation[:, data.cursor] = data.value[:, data.cursor + 1]
    surface = self.regression_model(data.coords[:, data.cursor], data.value[:, data.cursor])  # This is our proxy for the continuation value

    data.policy[:, data.cursor] =  data.offers[:, data.cursor] > surface(data.coords[:, data.cursor])
    data.value[:, data.cursor] = self.decision(data.offers[:, data.cursor], surface(data.coords[:, data.cursor]), data.continuation[:, data.cursor])

 def decision(self, offer_value, other_value, continuation_value):
       return offer_value if offer_value > other_value else continuation_value