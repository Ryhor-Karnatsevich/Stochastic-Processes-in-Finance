from data import Data
from simulations import Simulations
import matplotlib.pyplot as plt
import numpy as np



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



# Execution
sim = Simulations(iterations=1,s = starting_price)

gbm_paths = sim.geometric_brownian_motion(
    volatility=annual_volatility,
    mean_annual_return=mean_annual_return
)
plt.plot(gbm_paths[0], label='GBM Simulation')
plt.plot(df["Close"].values, label='Real AAPL')
plt.legend()
plt.show()

# rw_paths = sim.random_walk(walk_length=504)
# ou_paths = sim.ornstein_uhlenbeck_process(walk_length=504)