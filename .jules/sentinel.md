## 2026-01-06 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function accepted a raw filename string and passed it directly to `matplotlib.pyplot.savefig`. This allowed path traversal (e.g., `../sensitive_file`) or arbitrary file write to any location the process had access to.
**Learning:** Even utility functions intended for local output needs input validation. Libraries like `matplotlib` do not enforce path restrictions by default.
**Prevention:** Always validate file paths. Using `pathlib.Path(filename).name == filename` is a robust way to ensure a string is a simple filename without directory components.
