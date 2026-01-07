## 2026-01-07 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function accepted a filename argument and passed it directly to `plt.savefig()` without validation, allowing path traversal (e.g., `../malicious_file.png`).
**Learning:** Functions that write to files based on input parameters (even internally supplied ones that might become user-controlled later) must validate the path to prevent arbitrary file writes.
**Prevention:** Use `pathlib.Path(filename).name == filename` to ensure only a filename is provided and no directory traversal is attempted. Alternatively, resolve the path and ensure it starts with a trusted root directory.
