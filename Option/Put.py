import Option
import config
import numpy as np


class Put(Option):
    """
    A put option
    """

    def __init__(self, strike_price=None):
        super().__init__()
        if strike_price is None:
            strike_price = config.default["put_strike"]

        self.strike_price = strike_price

    def payoff(self, time, coord):
        return np.maximum(0, self.strike_price - coord)
