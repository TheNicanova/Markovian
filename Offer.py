import numpy as np

class Offer:
  """
  A function of state. The reward, or the value/amount offered.
  """
  def __init__(self):
    pass

  def payoff(self, time, coord):
    return max(0, coord - self.strike_price)

  def payoff_state(self, state):
    return self.payoff(state.get_time(), state.get_coord())

class Call(Offer):
  """
  A call option
  """
  def __init__(self, strike_price):
    self.strike_price = strike_price

  def payoff(self, time, coord):
    return np.maximum(0, coord - self.strike_price)

  def payoff_state(self, state):
    return self.payoff(state.get_time(), state.get_coord())

