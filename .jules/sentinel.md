## 2026-01-04 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function allowed writing to any file path provided by the caller, including paths outside the current working directory (e.g., `../hacked.png`).
**Learning:** Even internal helper functions (or functions intended for CLI use) can be vulnerable to path traversal if they accept file paths as input. Assumptions about "trusted input" should be verified.
**Prevention:** Always validate file paths using `pathlib`'s `resolve()` and `is_relative_to()` (or checking `startswith` with resolved paths) to ensure they are contained within the intended directory.
