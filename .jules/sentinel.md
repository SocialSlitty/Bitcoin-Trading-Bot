## 2024-05-22 - Unbounded Simulation Parameters DoS
**Vulnerability:** The `SimConfig` class allowed an unbounded `days` parameter. A malicious or accidental input (e.g., `10^9` days) would cause `generate_synthetic_data` to attempt allocating terabytes of memory for `numpy` arrays, leading to a crash (DoS). Additionally, `plot_results` accepted arbitrary file paths, allowing file overwrites outside the working directory.
**Learning:** Simulation parameters that directly control array sizes must have explicit upper bounds to prevent resource exhaustion. Input validation must extend beyond "is positive" to "is within safe operational limits". File paths provided to output functions must be sanitized to prevent traversal attacks.
**Prevention:**
1. Always enforce maximum limits on configuration parameters that drive memory allocation (`SimConfig` `days` cap).
2. Validate and sanitize file paths using `os.path.basename` to confine outputs to the intended directory.
