import matplotlib.pyplot as plt
import numpy as np
from config import *


class Option:
    """
  A function of state. The reward, or the value/amount offered.
  """

    def __init__(self):
        pass

    def get_name(self):
        return "Option"

    def payoff(self, time, coord):
        pass

    def payoff_state(self, state):
        return self.payoff(state.get_time(), state.get_coord())

    def plot(self, time, ax=None):
        if ax is None:
            fig, ax = plt.subplots()

        x_min = default["x_min"]
        x_max = default["x_max"]
        x_res = default["x_res"]
        x = np.linspace(x_min, x_max, x_res)
        ax.plot(x, self.payoff(time, x), label=self.get_name())
        return ax




