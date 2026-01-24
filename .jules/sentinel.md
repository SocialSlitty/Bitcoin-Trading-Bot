# Sentinel's Journal

## 2026-01-24 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function accepted any `filename` string and passed it directly to `plt.savefig()`, allowing attackers (if the library is exposed) to write files to arbitrary locations via path traversal (e.g., `../etc/passwd`).
**Learning:** Library functions that perform file I/O often default to trusting the caller, but this creates security debts when those libraries are later wrapped in web services or CLI tools with user input.
**Prevention:** Enforce strict filename validation by ensuring `filename == os.path.basename(filename)` to restrict writes to the current working directory, or use a dedicated output directory with sanitized paths.
