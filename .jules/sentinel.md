## 2026-01-26 - Prevent Path Traversal in File Output
**Vulnerability:** The `plot_results` function in `src/bitcoin_sim.py` accepted a `filename` argument without validation, allowing path traversal (e.g., `../file.png`).
**Learning:** Utility functions that write to files often trust the caller implicitly. When these functions are exposed or used with user input, they become vectors for arbitrary file overwrite.
**Prevention:** Always validate filenames in file-writing functions. Ensure they contain no path separators (`os.path.dirname(filename)` check) or resolve to a safe canonical path.
