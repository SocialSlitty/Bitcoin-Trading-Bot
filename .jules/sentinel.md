## 2026-02-05 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function allowed writing files to arbitrary paths via the `filename` argument, enabling potential overwriting of sensitive files or writing outside the intended directory.
**Learning:** Implicit trust in function arguments, even for internal tools like simulations, can lead to vulnerabilities if those arguments can potentially be controlled by external inputs or reused in unsafe contexts.
**Prevention:** Always validate file paths when writing to disk. Use `os.path.basename` to enforce writing to the current directory or a specific safe directory, and explicitly reject path separators.
