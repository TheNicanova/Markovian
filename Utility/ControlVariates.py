import numpy as np

def priceBS(S, K, sigma, r, q, T):
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

    a = np.log(S / K);
    b = r - q + 0.5 * sigma ** 2;
    c = sigma * np.sqrt(T);
    d1 = (a + b * T) / c;
    d2 = d1 - c;

    Peu = - S * np.exp(-q * T) * norm.cdf(-d1) + K * np.exp(-r * T) * norm.cdf(-d2)
    Delta = -np.exp(-q * T) * norm.cdf(-d1)

    return Peu, Delta