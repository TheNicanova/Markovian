import numpy as np

import Options
import config as config
import UnderlyingModels

from scipy.stats import norm


class European:

    def __init__(self, underlying_model=None, option=None, maturity=None):

        if underlying_model is None:
            underlying_model = UnderlyingModels.GeometricBrownianMotion()

        self.underlying_model = underlying_model
        self.rate = self.underlying_model.rate
        self.sigma = self.underlying_model.sigma
        self.dividend = self.underlying_model.dividend

        if maturity is None:
            maturity = config.default["terminal_time"]

        self.maturity = maturity

        if option is None:
            option = Options.Put()

        self.option = option
        self.strike_price = self.option.strike_price

    def put_price(self, node):

        underlying_price = node.get_coord()
        underlying_time = node.get_time()
        strike_price = self.strike_price
        time_to_maturity = self.maturity - underlying_time

        if time_to_maturity < 0.00001:
            european_put_price = max(0, strike_price - underlying_price)
        else:
            a = np.log(underlying_price / strike_price)
            b = self.rate - self.dividend + 0.5 * self.sigma ** 2
            c = self.sigma * np.sqrt(time_to_maturity)
            d1 = (a + b * time_to_maturity) / c
            d2 = d1 - c
            european_put_price = (-1) * underlying_price * norm.cdf(-d1) + strike_price * norm.cdf(-d2)

        return european_put_price
