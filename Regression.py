import numpy as np

class Regression():
  def fit(self, coord, offer_model, param):
    pass

class PolynomialRegression(Regression):
  def fit(self, coord, targets, param = 2): # here param is the degree
      p = np.polynomial.Polynomial.fit(coord, targets, param)
      return p