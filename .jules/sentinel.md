## 2026-01-28 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function accepted an arbitrary `filename` argument and passed it directly to `plt.savefig()`, allowing potential path traversal attacks (e.g., `../file.png`) if user input controlled the filename.
**Learning:** Even in internal tools or simulations, utility functions can be exposed to user input. Implicitly trusting file paths allows writing to arbitrary locations, which can lead to overwriting critical files.
**Prevention:** Always validate file paths when they are derived from input. Use `os.path.basename()` to enforce writing only to the current directory, or `os.path.abspath()` with a common path check to enforce a specific subdirectory.
