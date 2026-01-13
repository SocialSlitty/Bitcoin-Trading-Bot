## 2026-01-13 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function accepted an arbitrary `filename` argument and passed it directly to `plt.savefig`, allowing path traversal (e.g., `../evil.png`) and potential arbitrary file overwrite.
**Learning:** Even internal simulation tools can be vulnerable if they expose file write operations without validation. Relying on default values isn't enough; explicit validation is needed.
**Prevention:** Validate all file paths before writing. In this case, we enforced that the filename has no directory components using `os.path.dirname(filename)`.
