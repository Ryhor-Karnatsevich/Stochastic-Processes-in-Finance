import numpy as np
import matplotlib.pyplot as plt


class Simulations:
    def __init__(self, iterations = 1, s = 100, dt = 1/252):
        self.iterations = iterations
        self.s = s
        self.dt = dt



    # Random Walk
    # St = S(t-1) + Et
    def random_walk(self,walk_length = 504):
        results = []
        for number in range(self.iterations):
            start = [self.s]
            for i in range(walk_length):
                change = np.random.normal(0, 1)
                start.append(start[-1] + change)
            results.append(start)
        return results



    #==================================================================================================================================
    # Geometric Brownian Motion
    # St = S(t-1) * e^(( μ - σ^2/2)*dt + σ*Wt*dt)
    # μ = mean annual return(the percentage drift) | σ = volatility
    # Wt is a Wiener process of Brownian Motion
    def geometric_brownian_motion(self, walk_length = 504 , volatility = 0.2,mean_annual_return = 0.1):
        results = []
        for number in range(self.iterations):
            start = [self.s]
            for i in range(walk_length):
                Wt = np.random.normal(0, 1)
                start.append(start[-1] *np.exp((mean_annual_return - volatility**2 / 2) * self.dt + volatility * Wt * np.sqrt(self.dt)))
            results.append(start)
        return results




    #==================================================================================================================================
    # Ornstein-Uhlenbeck process
    # μ is a constant called the (long-term) mean
    # St = S(t-1) + θ*(μ - S(t-1))*dt + σ*Wt*dt

    def ornstein_uhlenbeck_process(self, walk_length = 504 , volatility = 0.2,Long_term_mean = 110, theta = 0.02):
        results = []
        for number in range(self.iterations):
            start = [self.s]
            for i in range(walk_length):
                Wt = np.random.normal(0, 1)
                start.append(start[-1] + theta * (Long_term_mean - start[-1]) * self.dt + volatility * Wt * np.sqrt(self.dt))
            results.append(start)
        return results

    def plot_one_path(self, process='gbm', **kwargs):
        if process == 'rw':
            paths = self.random_walk(**kwargs)
        elif process == 'gbm':
            paths = self.geometric_brownian_motion(**kwargs)
        elif process == 'ou':
            paths = self.ornstein_uhlenbeck_process(**kwargs)
        else:
            raise ValueError("process must be 'rw', 'gbm', or 'ou'")

        plt.figure(figsize=(12, 6))
        plt.plot(paths[0])
        plt.title(f"{process.upper()}")
        plt.xlabel("time step")
        plt.ylabel("price")
        plt.show()