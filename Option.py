import matplotlib.pyplot as plt
import numpy as np
import config


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

    def plot(self, time, ax=None, x_min=None, x_max=None):
        if ax is None:
            fig, ax = plt.subplots()
        if x_min is None:
            x_min = config.default["x_min"]
        if x_max is None:
            x_max = config.default["x_max"]

        x_res = config.default["x_res"]
        x = np.linspace(x_min, x_max, x_res)
        ax.plot(x, self.payoff(time, x), label=self.get_name())
        return ax

class Put(Option):
    """
    A put option
    """

    def __init__(self, strike_price=None):
        super().__init__()
        if strike_price is None:
            strike_price = config.default["put_strike"]

        self.strike_price = strike_price

    def get_name(self):
        return "Put(" + str(self.strike_price) + ")"

    def payoff(self, time, coord):
        return np.maximum(0, self.strike_price - coord)

class Call(Option):
    """
  A call option
  """

    def __init__(self, strike_price=None):
        super().__init__()
        if strike_price is None:
            strike_price = config.default["call_strike"]

        self.strike_price = strike_price

    def get_name(self):
        return "Call(" + str(self.strike_price) + ")"

    def payoff(self, time, coord):
        return np.maximum(0, coord - self.strike_price)



