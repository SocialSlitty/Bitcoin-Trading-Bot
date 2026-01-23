## 2026-01-23 - [Implicit Trust in Filename Arguments]
**Vulnerability:** The `plot_results` function accepted a `filename` argument and passed it directly to `plt.savefig`, allowing path traversal (arbitrary file overwrite) via inputs like `../evil.png`.
**Learning:** Utility functions in scripts are often written with the assumption of "friendly" inputs (e.g., hardcoded calls), but become vulnerable when exposed or reused in broader contexts where inputs might be user-controlled.
**Prevention:** Always sanitize file path arguments in utility functions using `os.path.basename` or explicit path validation, even if the current usage seems safe.
