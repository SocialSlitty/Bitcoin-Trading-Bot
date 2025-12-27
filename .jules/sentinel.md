## 2024-12-27 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function allowed writing to arbitrary file paths via the `filename` argument, enabling potential path traversal (e.g., `../../etc/passwd` or `/tmp/malicious`).
**Learning:** Python's `open()` or library functions like `plt.savefig()` do not validate paths by default. Simply checking for `..` is insufficient due to symbolic links and absolute paths.
**Prevention:** Use `pathlib.Path.resolve()` to obtain the canonical path and verify that the target path starts with the expected parent directory (`base_dir in target_path.parents`). This "jails" the file operations to the intended directory.
