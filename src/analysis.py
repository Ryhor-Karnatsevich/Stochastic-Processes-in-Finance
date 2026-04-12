import matplotlib.pyplot as plt
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf
import pandas as pd

from metrics import skewness, kurtosis, max_drawdown, autocorr, adf_pvalue
from data import Data
from simulations import Simulations
from style import print_styled_table

# Additional configurations for pycharm console
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.options.display.float_format = '{:.4f}'.format



# Setup
np.random.seed(52)
index = True  # Do you want to model index or stock ?
if index:
    ticker = "^VIX"
    theta = 1.5
else:
    ticker = "AAPL"
    theta = 0.25


# Load data from yfinance
df = Data(ticker=ticker).load()
ticker = ticker.replace("^", "") # just for beauty
df = df[["Close"]].tail(505) # 505 to have the same walk length = 2 years ( 2 * 252)
df["Return"] = np.log(df["Close"]) - np.log(df["Close"].shift(1)) # returns in logarithmic space for consistency
df = df.dropna()


# Parameters
starting_price = df["Close"].iloc[0].item()
# logarithmic parameters
real_returns = df["Return"].values
mean_annual_return = np.mean(real_returns) * 252
annual_volatility = np.std(real_returns) * np.sqrt(252)
log_prices = np.log(df["Close"].values) # price mean
long_term_mean = np.mean(log_prices)


# ======================================================================================================================
# Execution
sim = Simulations(iterations=100, s=starting_price)

rw = sim.geometric_random_walk()

gbm = sim.geometric_brownian_motion( mean_annual_return = mean_annual_return, volatility = annual_volatility)

ou = sim.ornstein_uhlenbeck_process( long_term_mean=long_term_mean, volatility=annual_volatility, theta=theta)

# ======================================================================================================================

# Data transformation
gbm_returns = np.log(gbm[:, 1:] / gbm[:, :-1])
ou_returns = np.log(ou[:, 1:] / ou[:, :-1])
rw_returns = np.log(rw[:, 1:] / rw[:, :-1])



# STATISTICS TABLE
stats = {
    f"{ticker}": {
        "mean": np.mean(real_returns) * 252,
        "volatility": np.std(real_returns) * np.sqrt(252),
        "autocorr": autocorr(real_returns),
        "adf_pvalue": adf_pvalue(real_returns),
        "adf_price": adf_pvalue(df["Close"].values),
        "skewness": skewness(real_returns),
        "kurtosis": kurtosis(real_returns),
        "max_drawdown": max_drawdown(df["Close"].values)
    },

    "Random Walk": {
        "mean": np.mean(rw_returns.flatten()) * 252,
        "volatility": np.std(rw_returns.flatten()) * np.sqrt(252),
        "autocorr": autocorr(rw_returns.flatten()),
        "adf_pvalue": adf_pvalue(rw_returns.flatten()),
        "adf_price": np.mean([adf_pvalue(path) for path in rw]),
        "skewness": skewness(rw_returns.flatten()),
        "kurtosis": kurtosis(rw_returns.flatten()),
        "max_drawdown": np.mean([max_drawdown(path) for path in rw])
    },

    "Geometric Brownian Motion": {
        "mean": np.mean(gbm_returns.flatten()) * 252,
        "volatility": np.std(gbm_returns.flatten()) * np.sqrt(252),
        "autocorr": autocorr(gbm_returns.flatten()),
        "adf_pvalue": adf_pvalue(gbm_returns.flatten()),
        "adf_price": np.mean([adf_pvalue(path) for path in gbm]),
        "skewness": skewness(gbm_returns.flatten()),
        "kurtosis": kurtosis(gbm_returns.flatten()),
        "max_drawdown": np.mean([max_drawdown(path) for path in gbm])
    },

    "Ornstein–Uhlenbeck": {
        "mean": np.mean(ou_returns.flatten()) * 252,
        "volatility": np.std(ou_returns.flatten()) * np.sqrt(252),
        "autocorr": autocorr(ou_returns.flatten()),
        "adf_pvalue": adf_pvalue(ou_returns.flatten()),
        "adf_price": np.mean([adf_pvalue(path) for path in ou]),
        "skewness": skewness(ou_returns.flatten()),
        "kurtosis": kurtosis(ou_returns.flatten()),
        "max_drawdown": np.mean([max_drawdown(path) for path in ou])
    }
}

# PRINT TABLE
table = pd.DataFrame(stats).T
print_styled_table(table, f"STATISTICAL COMPARISON: {ticker} vs MODELS")



# ======================================================================================================================
#  PRICE CURVES
plt.figure(figsize=(12,6))

real_prices = df["Close"].values

plt.plot(real_prices, label=f"{ticker}")
plt.plot(rw[0][:len(real_prices)], label="Random Walk",alpha=0.5)
plt.plot(gbm[0][:len(real_prices)], label="Geometric Brownian Motion")
plt.plot(ou[0][:len(real_prices)], label="Ornstein-Uhlenbeck Process",alpha=0.8)

plt.legend()
plt.title("Price Paths Comparison",fontsize=24)
plt.xlabel("Steps",fontsize=20)
plt.locator_params(axis='x', nbins=20)
plt.ylabel("Price",fontsize=20)
plt.grid(alpha=0.3)

plt.show()


# ======================================================================================================================
# MEAN PRICE CURVES
plt.figure(figsize=(12,6))

real_prices = df["Close"].values

gbm_mean = np.mean(gbm, axis=0)
rw_mean = np.mean(rw, axis=0)
ou_mean = np.mean(ou, axis=0)

plt.plot(real_prices, label=f"{ticker}")
plt.plot(rw_mean[:len(real_prices)], label="Random Walk", alpha=0.5)
plt.plot(gbm_mean[:len(real_prices)], label="Geometric Brownian Motion")
plt.plot(ou_mean[:len(real_prices)], label="Ornstein-Uhlenbeck Process", alpha=0.8)

plt.legend()
plt.title("Mean Price Paths Comparison", fontsize=24)
plt.xlabel("Steps", fontsize=20)
plt.locator_params(axis='x', nbins=20)
plt.ylabel("Price", fontsize=20)
plt.grid(alpha=0.3)

plt.show()


# ======================================================================================================================
# RETURNS DISTRIBUTION (2x2)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Returns Distribution",fontsize=24)

axes[0,0].hist(real_returns, bins=50, color="C0",alpha=0.7)
axes[0,0].set_title(f"{ticker}", fontsize=20)

axes[0,1].hist(rw_returns.flatten(), bins=50, color="C1",alpha=0.7)
axes[0,1].set_title("Random Walk", fontsize=20)

axes[1,0].hist(gbm_returns.flatten(), bins=50, color="C2",alpha=0.7)
axes[1,0].set_title("Geometric Brownian Motion",fontsize=20)

axes[1,1].hist(ou_returns.flatten(), bins=50, color="C3",alpha=0.7)
axes[1,1].set_title("Ornstein-Uhlenbeck Process",fontsize=20)

plt.show()


# ======================================================================================================================
# AUTOCORRELATION PLOTS
lag = 20

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(f"Autocorrelation (Lag={lag})",fontsize=24)

plot_acf(real_returns, lags=lag, ax=axes[0,0])
axes[0,0].set_title(f"{ticker}", fontsize=20)
axes[0,1].set_ylim(-0.25, 0.25)

plot_acf(rw_returns.flatten(), lags=20, ax=axes[0,1])
axes[0,1].set_title("Random Walk", fontsize=20)
axes[0,1].set_ylim(-0.05, 0.05)

plot_acf(gbm_returns.flatten(), lags=20, ax=axes[1,0])
axes[1,0].set_title("Geometric Brownian Motion",fontsize=20)
axes[1,0].set_ylim(-0.05, 0.05)

plot_acf(ou_returns.flatten(), lags=20, ax=axes[1,1])
axes[1,1].set_title("Ornstein-Uhlenbeck Process",fontsize=20)
axes[1,1].set_ylim(-0.05, 0.05)

plt.tight_layout()
plt.show()
