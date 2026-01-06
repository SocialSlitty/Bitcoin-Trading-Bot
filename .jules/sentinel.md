## 2024-12-30 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function allowed arbitrary file paths for output, potentially enabling path traversal if the filename argument was user-controlled.
**Learning:** Even internal utility functions like plotting helpers should validate file paths to prevent accidental or malicious overwrites outside the project scope.
**Prevention:** Use `pathlib.Path.resolve()` and check `.is_relative_to(cwd)` for any function that writes files based on input arguments.
