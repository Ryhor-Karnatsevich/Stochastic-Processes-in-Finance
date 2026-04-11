from data import Data
from simulations import Simulations
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



# Class Simulations: iterations, s (start price), dt (default = 1/252)
# Class Data: ticker


# Data Preparing
df = Data(ticker="AAPL").load()
df = df[["Close"]].tail(505)
df["Return"] = df["Close"].pct_change()
df = df.dropna()
print(df)
# Metrics
returns = df["Return"].values
mean_annual_return = np.mean(returns) * 252
annual_volatility = np.std(returns) * np.sqrt(252)
starting_price = df["Close"].iloc[0]
print(round(mean_annual_return,4), round(annual_volatility,4))
long_term_mean = np.mean(df["Close"].values)


# Execution
sim = Simulations(iterations=5,s = starting_price)


rw = sim.random_walk()

gbm = sim.geometric_brownian_motion(
    volatility=annual_volatility,
    mean_annual_return=mean_annual_return
)

ou = sim.ornstein_uhlenbeck_process(
    volatility=annual_volatility,
    long_term_mean=long_term_mean
)






# Plots
# returns distribution
fig, axes = plt.subplots(2, 2, figsize=(20, 14))
fig.suptitle("Returns Distribution",fontweight="bold",fontsize=30)
# Stock returns
axes[0,0].hist(returns, bins=60, label="Stock", color="C0")
axes[0,0].legend(fontsize="14")

# random walk returns
rw_returns = []
for ele in rw:
    series = pd.Series(np.ravel(ele))
    rw_returns.extend(series.pct_change().dropna().to_numpy())
rw_returns = np.array(rw_returns, dtype=float)
axes[0,1].hist(rw_returns, bins=24, label="Random Walk",color="C2")
axes[0,1].legend(fontsize="14")

# gbm returns distribution
gbm_returns = []
for ele in gbm:
    series = pd.Series(np.ravel(ele))
    gbm_returns.extend(series.pct_change().dropna().to_numpy())
gbm_returns = np.array(gbm_returns, dtype=float)
axes[1,0].hist(gbm_returns, bins=60, label="Geometric Brownian Motion", color="C1")
axes[1,0].legend(fontsize="14")

# ou returns distribution
ou_returns = []
for ele in ou:
    series = pd.Series(np.ravel(ele))
    ou_returns.extend(series.pct_change().dropna().to_numpy())
ou_returns = np.array(ou_returns, dtype=float)
axes[1,1].hist(ou_returns, bins=60, label="Ornstein-Uhlenbeck Process", color="C3")
axes[1,1].legend(fontsize="14")

plt.show()


# Prices
fig, axes = plt.subplots(1, 1, figsize=(20, 14))
plt.plot(df["Close"].values, label='Real AAPL')
plt.plot(gbm[0], label='GBM Simulation')
plt.plot(rw[0], label='Random Walk')
plt.plot(ou[0], label='Ornstein Uhlenbeck Process')
plt.legend(fontsize="14")
plt.show()
