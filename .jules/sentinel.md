## 2026-01-30 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function accepted any filename string, allowing path traversal (e.g., `../file`).
**Learning:** File output functions exposed to user input must validate paths to prevent arbitrary file writes.
**Prevention:** Use `os.path.basename` to strip directory components or strictly validate filenames against an allowlist.
