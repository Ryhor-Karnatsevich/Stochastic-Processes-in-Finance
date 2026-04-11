from data import Data
from simulations import Simulations
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf



# Class Simulations: iterations, s (start price), dt (default = 1/252)
# Class Data: ticker


# Data Preparing
ticker = "AAPL"
df = Data(ticker=ticker).load()
df = df[["Close"]].tail(505)
df["Return"] = df["Close"].pct_change()
df = df.dropna()
print(df)
# Metrics
returns = df["Return"].values
mean_annual_return = np.mean(returns) * 252
annual_volatility = np.std(returns) * np.sqrt(252)
starting_price = df["Close"].iloc[0].item()
print(round(mean_annual_return,4), round(annual_volatility,4))
long_term_mean = np.mean(df["Close"].values)
np.random.seed(52)


# ======================================================================================================================
# Execution
sim = Simulations(iterations=100, s=starting_price)

gbm = sim.geometric_brownian_motion(mean_annual_return = mean_annual_return, volatility = annual_volatility)

rw = sim.geometric_random_walk()

ou = sim.ornstein_uhlenbeck_process(long_term_mean=long_term_mean)

# Data transformation
real_returns = np.log(df["Close"].values[1:] / df["Close"].values[:-1])
gbm_returns = np.log(gbm[:, 1:] / gbm[:, :-1])
ou_returns = np.log(ou[:, 1:] / ou[:, :-1])
rw_returns = np.log(rw[:, 1:] / rw[:, :-1])


# =======================
# STATISTICS TABLE
# =======================

def autocorr(x):
    x = np.asarray(x).flatten()
    x = x[~np.isnan(x)]
    if len(x) < 2:
        return np.nan
    return np.corrcoef(x[:-1], x[1:])[0, 1]

def adf_pvalue(x):
    return adfuller(x)[1]

stats = {
    "Real": {
        "mean": np.mean(real_returns),
        "var": np.var(real_returns),
        "autocorr": autocorr(real_returns),
        "adf_pvalue": adf_pvalue(real_returns)
    },
    "RW": {
        "mean": np.mean(rw_returns.flatten()),
        "var": np.var(rw_returns.flatten()),
        "autocorr": autocorr(rw_returns.flatten()),
        "adf_pvalue": adf_pvalue(rw_returns.flatten())
    },
    "GBM": {
        "mean": np.mean(gbm_returns.flatten()),
        "var": np.var(gbm_returns.flatten()),
        "autocorr": autocorr(gbm_returns.flatten()),
        "adf_pvalue": adf_pvalue(gbm_returns.flatten())
    },
    "OU": {
        "mean": np.mean(ou_returns.flatten()),
        "var": np.var(ou_returns.flatten()),
        "autocorr": autocorr(ou_returns.flatten()),
        "adf_pvalue": adf_pvalue(ou_returns.flatten())
    }
}
# =======================
# PRINT TABLE
# =======================

import pandas as pd

table = pd.DataFrame(stats).T

print("\n=== STATISTICS SUMMARY ===\n")
print(table)


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

plt.tight_layout()
plt.show()
