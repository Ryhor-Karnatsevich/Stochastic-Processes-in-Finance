import numpy as np

class Simulations:
    def __init__(self, iterations = 1, s = 100, dt = 1/252):
        self.iterations = iterations
        self.s = s
        self.dt = dt


    # Random Walk
    # St = S(t-1) * exp(Et * √dt)
    # used geometric version to ensure data integrity in further logarithmic data comparison
    def geometric_random_walk(self, walk_length=504):
        Et = np.random.normal(0, 1, (self.iterations, walk_length))
        increments = Et * np.sqrt(self.dt)

        cumulative_sum = np.cumsum(increments, axis=1)

        zeros_column = np.zeros((self.iterations, 1))
        paths_with_changes = np.column_stack([zeros_column, cumulative_sum])
        results = self.s * np.exp(paths_with_changes)
        return results


    #==================================================================================================================================
    # Geometric Brownian Motion
    # St = S(t-1) * e^(( μ - σ^2/2)*dt + σ*Wt*dt)
    # μ = mean annual return(the percentage drift) | σ = volatility
    # Wt is a Wiener process of Brownian Motion
    def geometric_brownian_motion(self, walk_length=504, volatility=0.2, mean_annual_return=0.1):
        # vectorization
        # used normal distribution as default setup for GB motion (basic for Black-Scholes modeling)
        Wt = np.random.normal(0, 1, (self.iterations, walk_length))

        calculations = (mean_annual_return - volatility ** 2 / 2) * self.dt + volatility * Wt * np.sqrt(self.dt)

        log_paths = np.cumsum(calculations, axis=1)
        log_paths = np.hstack([np.zeros((self.iterations, 1)), log_paths])

        results = self.s * np.exp(log_paths)

        return results


    #==================================================================================================================================
    # Ornstein-Uhlenbeck process
    # μ is a constant called the (long-term) mean
    # St = S(t-1) + θ*(μ - S(t-1))*dt + σ*Wt*dt
    # θ = theta
    def ornstein_uhlenbeck_process(self, walk_length=504, volatility=0.2, long_term_mean=None, theta=0.5):
        St = np.zeros((self.iterations, walk_length + 1))
        St[:, 0] = np.log(self.s)
        Wt = np.random.normal(0, 1, (self.iterations, walk_length))
        mean = long_term_mean
        for t in range(1, walk_length + 1):
            St[:, t] = (
                    St[:, t - 1]
                    + theta * (mean - St[:, t - 1]) * self.dt
                    + volatility * np.sqrt(self.dt) * Wt[:, t - 1]
            )

        return np.exp(St)
