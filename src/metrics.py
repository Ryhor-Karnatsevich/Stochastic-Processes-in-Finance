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


def monte_carlo_summary(paths):
    """Terminal changes and pathwise drawdown probabilities, not daily returns."""
    paths = np.asarray(paths, dtype=float)
    if (paths.ndim != 2 or min(paths.shape) < 2
            or not np.all(np.isfinite(paths)) or np.any(paths <= 0)):
        raise ValueError("Expected at least two finite, positive price paths")
    changes = paths[:, -1] / paths[:, 0] - 1
    peaks = np.maximum.accumulate(paths, axis=1)
    drawdowns = np.min(paths / peaks - 1, axis=1)
    probability = np.mean(changes < 0)
    drawdown_probability = np.mean(drawdowns < -0.20)
    n = len(paths)
    return dict(
        mean=np.mean(changes), median=np.median(changes),
        q05=np.quantile(changes, 0.05), q95=np.quantile(changes, 0.95),
        loss_probability=probability, drawdown_probability=drawdown_probability,
        mean_se=np.std(changes, ddof=1) / np.sqrt(n),
        loss_se=np.sqrt(probability * (1 - probability) / n),
        drawdown_se=np.sqrt(drawdown_probability * (1 - drawdown_probability) / n),
    )


