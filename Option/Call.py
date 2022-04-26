from Option.Option import *
import numpy as np
import config


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
        return "Call option with strike price " + str(self.strike_price)

    def payoff(self, time, coord):
        return np.maximum(0, coord - self.strike_price)
