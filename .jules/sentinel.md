## 2026-02-04 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function in `bitcoin_sim.py` accepted a `filename` argument without validation, allowing potential path traversal (e.g., writing to `../../file`) if the input were user-controlled.
**Learning:** Even internal utility functions like plotting should validate file paths, as they might be exposed later or used in contexts where inputs are not trusted.
**Prevention:** Always validate filenames using `os.path.basename(filename) == filename` or checks for `..` and path separators before writing files.
