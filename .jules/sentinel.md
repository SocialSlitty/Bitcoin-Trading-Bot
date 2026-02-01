## 2026-02-01 - [Path Traversal in Plotting Function]
**Vulnerability:** The `plot_results` function in `src/bitcoin_sim.py` accepted a `filename` argument that was used directly in `plt.savefig()` without validation, allowing for path traversal (e.g., writing to `/tmp` or overwriting system files if running with elevated privileges).
**Learning:** Even auxiliary functions used for outputting results can be attack vectors if they accept filenames from potential user input (simulations or web wrappers).
**Prevention:** Validate all file paths. For simple output files, ensure the filename contains no path separators (`/` or `\`) using `os.path.basename(f) == f` or similar checks.
