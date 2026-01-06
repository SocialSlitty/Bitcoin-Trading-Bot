## 2024-12-31 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function in `src/bitcoin_sim.py` accepted a `filename` argument directly passed to `matplotlib.pyplot.savefig` without validation.
**Learning:** Even internal helper functions can become attack vectors if they process user-controlled input (e.g., via CLI or future API). Python's `pathlib` offers a robust way to validate paths.
**Prevention:** Always validate file paths against a whitelist (e.g., current directory) using `Path.resolve().is_relative_to(base_dir)`.