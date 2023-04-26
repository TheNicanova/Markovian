import OptimalStopping.config as config
import numpy as np
import matplotlib.pyplot as plt


class Option:
    """
  A function of state. The reward, or the value/amount offered.
  """

    def __init__(self):
        pass

    def get_name(self):
        return

    def payoff(self, time, coord):
        pass

    def payoff_state(self, state):
        return self.payoff(state.get_time(), state.get_coord())


