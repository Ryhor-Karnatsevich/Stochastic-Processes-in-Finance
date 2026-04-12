# Stochastic Processes in Finance
 
The goal of this research is to explore how different stochastic processes can be applied to simulate the behavior of financial assets.
Four Hypothesis were questioned and explored on different assets.

## Hypothesis

1. Market has a weak form of efficiency
2. Market is a random walk
3. Market is lognormal
4. Market is being attracted to some average 






## Methodology

- It can be chosen index or stock ticker. 
- Based on preferred option, will be extracted data as:
  - Starting price
  - Average Return (Annualized)
  - Average Volatility (Annualized)
  - Long-Term Average Price

- Analysis has 200 iterations.
- Every Process has the same starting price.
- All calculations made in logarithmic form.
- **Normal distribution** was used as default for stochastic variable, Wt ~ N(0,1).
- Most of the calculations were made using vectorization and class.
- csv files date = 12.04.2026

### Random walk
- Does not require external variables.
- Was used geometrical formula to extend logarithmic return in further analysis. 
- Due to that showed up Jensen's inequality. Decided not to change model, but to keep in mind that fact.


Theoretical Linear foundation:

![formula](Data/Pictures/random.png)

---

### Geometric Brownian Motion




Theoretical foundation:

![formula](Data/Pictures/Brownian_motion.png)

---

### Ornstein-Uhlenbeck process
- While the classical Ornstein-Uhlenbeck process is defined in linear space, I reformulated it in log-space to maintain consistency with other processes.
- Model assumes a constant long-term mean, which may not reflect real market dynamics.


Theoretical foundation:

![formula](Data/Pictures/OU.png)

---



## Limitations
- OU does not fit to simulate single stock. shows strong attraction to the average




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