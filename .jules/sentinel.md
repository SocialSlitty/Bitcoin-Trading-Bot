## 2026-01-25 - Path Traversal in File Output Functions
**Vulnerability:** The `plot_results` function allowed arbitrary file paths, enabling path traversal (e.g., `../evil.png`) which could overwrite sensitive files.
**Learning:** Utility functions that accept output filenames are often overlooked as injection vectors. Even in simulation scripts, these can be exposed or reused in larger systems.
**Prevention:** Always validate filenames in functions that write to disk. Ensure they contain no path separators (`os.path.basename(f) == f`) to restrict writes to the current working directory, or validate against a strict allowlist of directories.
