import numpy as np

import config
from config import *
import numpy as np
from config import *
from scipy.stats import norm


def BM_European(node, strike_price=None, sigma=None, rate=None, dividend=None, time_to_maturity=None):
    ''' The Black–Scholes formula calculates the price of European put option.

    Parameters
    ==========
    S    : (float) initial value of the stock prices.
    K     : (float) the strike or exercise price.
    sigma : (float) volatility.
    r     : (float) risk-free interest rate.
    q     : (float) dividend yield rate.

    Returns
    =======
    Peu : float
        the price of European put option
    '''

    if rate is None: rate = gbm_default['rate']
    if sigma is None: sigma = gbm_default['sigma']
    if dividend is None: dividend = gbm_default['dividend']
    if time_to_maturity is None: time_to_maturity = default["terminal_time"] - node.get_time()
    if strike_price is None: strike_price = config.default["put_strike"]

    current_price = node.get_coord()

    if time_to_maturity < 0.00001:
        return max(0, strike_price - current_price)

    a = np.log(current_price / strike_price)
    b = rate - dividend + 0.5 * sigma ** 2
    c = sigma * np.sqrt(time_to_maturity)
    d1 = (a + b * time_to_maturity) / c
    d2 = d1 - c

    european_price = (-1) * current_price * norm.cdf(-d1) + strike_price * norm.cdf(-d2)

    return european_price
