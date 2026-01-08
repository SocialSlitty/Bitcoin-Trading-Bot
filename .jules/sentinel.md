## 2026-01-08 - Path Traversal in Simulation Plotting
**Vulnerability:** The `plot_results` function allowed arbitrary filenames, enabling directory traversal (e.g., `../evil.png`) to write files outside the intended directory.
**Learning:** Even internal simulation tools can be vulnerable to path traversal if they process user-provided filenames, which could be exploited if wrapped in a service or used with untrusted inputs.
**Prevention:** Always validate filenames using `pathlib.Path(f).name == f` to ensure they do not contain path separators, or strictly sanitize inputs against a whitelist of allowed characters.
