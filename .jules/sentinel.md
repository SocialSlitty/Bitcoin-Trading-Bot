## 2024-05-23 - Path Traversal Prevention in File Outputs
**Vulnerability:** The `plot_results` function allowed arbitrary file paths via the `filename` argument, potentially enabling path traversal attacks if the filename was user-controlled.
**Learning:** Even in internal simulation scripts, file output functions should validate filenames to ensure they only write to intended directories (e.g., current working directory).
**Prevention:** Enforce that `os.path.basename(filename) == filename` to reject any path separators or directory components.
