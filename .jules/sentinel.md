# Sentinel's Journal

## 2024-01-01 - [Sentinel Init]
**Vulnerability:** N/A
**Learning:** Initialized security journal.
**Prevention:** N/A

## 2026-01-20 - [Path Traversal and DoS Protection]
**Vulnerability:** The `plot_results` function allowed writing files to arbitrary paths via directory traversal, and `SimConfig` lacked an upper limit on simulation duration, posing a DoS risk.
**Learning:** File system operations and resource-intensive loops must always have strict input validation to prevent unauthorized file access and resource exhaustion.
**Prevention:** Implemented `os.path.basename` validation for filenames and enforced a hard limit of 36,500 days (100 years) for simulations.
