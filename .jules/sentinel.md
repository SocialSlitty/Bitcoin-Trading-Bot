## 2026-02-03 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function in `src/bitcoin_sim.py` accepted a `filename` argument without validation, allowing a potential attacker to write the output plot to arbitrary locations on the file system (Path Traversal) if the filename was user-controlled.
**Learning:** Functions that perform file I/O using parameters that *could* be user-controlled (even if currently hardcoded in main) must always validate inputs to prevent security risks if the function is reused in a different context (e.g., an API).
**Prevention:** Validate all file paths before use. Use `os.path.basename(filename) == filename` to ensure files are written only to the intended directory, or strictly validate against an allowlist of directories.
