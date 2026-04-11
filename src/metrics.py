import numpy as np
from scipy.stats import skew, kurtosis as scipy_kurtosis
from statsmodels.tsa.stattools import adfuller


def skewness(data):
    data = np.asarray(data).flatten()
    return skew(data)


def kurtosis(data):
    data = np.asarray(data).flatten()
    return scipy_kurtosis(data, fisher=False)


def max_drawdown(prices):
    prices = np.asarray(prices)
    cumulative_max = np.maximum.accumulate(prices)
    drawdowns = (prices - cumulative_max) / cumulative_max
    return np.min(drawdowns)

def autocorr(x):
    x = np.asarray(x).flatten()
    x = x[~np.isnan(x)]
    if len(x) < 2:
        return np.nan
    return np.corrcoef(x[:-1], x[1:])[0, 1]

def adf_pvalue(x):
    return adfuller(x)[1]


