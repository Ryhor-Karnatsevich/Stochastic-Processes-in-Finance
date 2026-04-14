# Stochastic Processes in Finance
 
The goal of this research is to explore how different theoretical stochastic processes can be applied in real modeling.

Explore if those models are useful to simulate the behavior of financial assets.

And Prove or deny four Hypothesis on example of stock and index.

## Hypotheses

1. Financial returns exhibit weak-form market efficiency, meaning no significant autocorrelation in returns.


2. Asset price dynamics can be approximated by a random walk process, based on the statistical behavior of returns.


3. Returns distribution matches the assumptions of the Geometric Brownian Motion model.


4. Asset prices exhibit mean-reverting behavior, which can be detected using stationarity tests.

## Methodology
### Data
- User can choose either stock or index
- Data source: local CSV or yfinance
- csv Files Date = 12.04.2026
- Time horizon: last 505 observations (~2 years)
- Based on preferred option, will be extracted real data for processes:
  - Returns
  - Starting Price
  - Average Return (Annualized)
  - Average Volatility (Annualized)
  - Long-Term Average Price
- All calculated in logarithmic space for data consistency.


### Why logarithmic space?
All calculations are performed in logarithmic space for consistency and mathematical correctness:

Returns are additive: log(St / S(t-1))

- This allows modeling price dynamics as cumulative sums of increments, instead of multiplicative growth.
- Models like GBM are naturally defined in log-space. So it was decided to equal other processes for competent analysis.
- Volatility scales correctly with time
- Prevents distortion when comparing different processes


Prices are recovered by exponentiating the log-process.
- RW / GBM: St = S0 * exp(Xt)
- OU: St = exp(Xt), since log-price is modeled directly
 

### Simulation setup
- Number of simulations: 200
- Time step:dt = 1 / 252

All models use the same:
- starting price
- time horizon


**Random component** - Wt is a Wiener process such that: dWt ~ N(0, dt)
- The Wiener process can be seen as a random walk in continuous time. 
- It serves as the common source of randomness across all simulated processes.


## Discretization Approach
- Continuous-time stochastic differential equations (SDEs) cannot be implemented directly in code.
- Therefore, all models were transformed into discrete-time form using **Euler** discretization.


**Euler** discretization approximates continuous dynamics by replacing infinitesimal changes with small finite steps:

- dt represents a small time increment
- differential terms (dX, dWt) are replaced with discrete changes

As a result:
- deterministic components scale with dt
- stochastic components scale with √dt

This allows simulation of continuous stochastic processes using iterative updates.


## Processes

---

### Random Walk
Pure stochastic process - only basic external variables.

Theoretical Linear foundation:

![formula](Data/Pictures/random_walk_theory.png)


To ensure that process in logarithmic space I needed to reformulate It. 

Let Et ~ N(0,1) be independent standard normal variables. Then:

![formula](Data/Pictures/random_walk_calculations.png)

Meaning that:

![formula](Data/Pictures/random_walk.png)

In log-space, the process evolves as a linear random walk with increments Et · √dt.

The price itself is obtained via exponentiation, making it non-linear.

**Jensen's Inequality:** 
- Geometric version is used to stay consistent with log-returns
- Due to that showed up Jensen's inequality effect (bias after exponentiation):
    - E[exp(X)] > exp(E[X])
    - Even if log-returns have zero mean, expected price grows over time.
    - This creates an upward bias in simulated paths, which is a known artifact of geometric formulation.
- In this project:
  - the effect is preserved intentionally
  - no martingale correction is applied
  - since it does not distort return-based statistics

**Note:** "Why √dt?" is gonna be explained on Geometric Brownian Motion example and is applied to every model in my project.

---

### Geometric Brownian Motion

Adds deterministic drift to random walk

Theoretical foundation:

![formula](Data/Pictures/Brownian_motion.png)

Let Et ~ N(0,1) be independent standard normal variables. Then discrete version looks like:

![formula](Data/Pictures/brownian_motion_calculations.png)

Where:
- μ = Mean Annual Return
- σ = Annual Volatility

In the increment formula, the deterministic part scales with dt (linear drift over time), while the stochastic part scales with √dt.

**Why √dt?**
- In Brownian Motion applied Wiener Process as a base for stochastic part.
- In the continuous-time model, the Wiener process increment dWt has variance dt

![formula](Data/Pictures/gbm_var.png)

In discrete simulation, is used Et ~ N(0,1) which has variance 1.

To transform Et ~ N(0,1) into dWt ~ N(0, dt), multiply Et by √dt (the standard deviation of dWt).

![formula](Data/Pictures/gbm_stoch.png)

This scaling ensures that the stochastic part has the correct variance dt

**Conclusion**
- The model combines:
  - deterministic exponential growth (drift)
  - stochastic fluctuations (volatility)
- Unlike Random Walk:
  - GBM has a built-in trend
  - growth is controlled by μ

---

### Ornstein-Uhlenbeck process

Mean-reverting process.

Theoretical foundation:

![formula](Data/Pictures/OU.png)

Let Et ~ N(0,1) be independent standard normal variables. Then discrete version looks like:

![formula](Data/Pictures/ou_used.png)

- Et was also transformed to get Wiener's Process variance as it was in previous model.
- New variable **theta** - measures the speed of getting back to μ. (Mean Reversion part)

Where:
- μ = Long-term Mean (log price)
- θ = Speed of Mean Reversion (theta)
- σ = Annual Volatility

Notes:
- While the classical Ornstein-Uhlenbeck process is defined in linear space, I reformulated it in log-space to maintain consistency with other processes.
- Model assumes a constant long-term mean, which may not reflect real market dynamics.

**Conclusion**
- Unlike GBM, the OU process does not accumulate drift over time.
- Instead - deviations from the mean are continuously corrected and growth is suppressed.
- This explains why OU paths are gonna appear “flat” and fail to reproduce trending behavior of stocks
- The process is stationary in log-space (under constant μ)

---

## Stock 

**Random walk**
**Geometric Brownian Motion**
**Ornstein-Uhlenbeck process**

![plot](Data/Pictures/stock_data.png)
![plot](Data/Pictures/stock_prices.png)
![plot](Data/Pictures/stock_mean.png)
![plot](Data/Pictures/stock_dist.png)
![plot](Data/Pictures/stock_autocorrelation.png)



## Index

**Random walk**
**Geometric Brownian Motion**
**Ornstein-Uhlenbeck process**

![plot](Data/Pictures/index_data.png)
![plot](Data/Pictures/index_prices.png)
![plot](Data/Pictures/index_mean.png)
![plot](Data/Pictures/index_dist.png)
![plot](Data/Pictures/index_autocorrelation.png)





## Limitations
- OU does not fit to simulate single stock. shows strong attraction to the average

NOTES
- Most of the calculations were made using vectorization and class.











