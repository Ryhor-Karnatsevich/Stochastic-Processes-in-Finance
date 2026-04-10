# Setup for Class
sim = Simulations(iterations=10000, s=100, dt=1/252)

# Calculating
print("Random Walk calculation")
rw_paths = sim.random_walk(walk_length=252)
print(f"Iterations: {len(rw_paths)}, walk length: {len(rw_paths[0])} steps")

print("GBM calculation")
gbm_paths = sim.geometric_brownian_motion(walk_length=252, volatility=0.2)
print(f"Iterations: {len(gbm_paths)}")

print("OU calculation")
ou_paths = sim.ornstein_uhlenbeck_process(walk_length=252)
print(f"Iterations: {len(ou_paths)}")


# First gbm plot visualization
sim.plot_one_path(process='gbm', walk_length=252)





final_rw = [path[-1] for path in rw_paths]
final_gbm = [path[-1] for path in gbm_paths]
final_ou = [path[-1] for path in ou_paths]

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].hist(final_rw, bins=50, alpha=0.7, color='blue', edgecolor='black')
axes[0].set_title("Random Walk")
axes[0].set_xlabel("End Price")
axes[0].axvline(np.mean(final_rw), color='red', linestyle='--', label=f'Mean: {np.mean(final_rw):.1f}')
axes[0].legend()

axes[1].hist(final_gbm, bins=50, alpha=0.7, color='green', edgecolor='black')
axes[1].set_title("GBM")
axes[1].set_xlabel("End Price")
axes[1].axvline(np.mean(final_gbm), color='red', linestyle='--', label=f'Mean: {np.mean(final_gbm):.1f}')
axes[1].legend()

axes[2].hist(final_ou, bins=50, alpha=0.7, color='red', edgecolor='black')
axes[2].set_title("Ornstein-Uhlenbeck")
axes[2].set_xlabel("End Price")
axes[2].axvline(np.mean(final_ou), color='red', linestyle='--', label=f'Mean: {np.mean(final_ou):.1f}')
axes[2].legend()

plt.tight_layout()
plt.show()

# Final results
print("\n")
print(f"{'Process':<20} {'Mean':<12} {'standard deviation':<18} {'Median':<12}")
print(f"{'Random Walk':<20} {np.mean(final_rw):<12.2f} {np.std(final_rw):<18.2f} {np.median(final_rw):<12.2f}")
print(f"{'GBM':<20} {np.mean(final_gbm):<12.2f} {np.std(final_gbm):<18.2f} {np.median(final_gbm):<12.2f}")
print(f"{'OU':<20} {np.mean(final_ou):<12.2f} {np.std(final_ou):<18.2f} {np.median(final_ou):<12.2f}")