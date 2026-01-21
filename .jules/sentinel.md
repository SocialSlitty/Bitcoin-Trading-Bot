# Sentinel's Security Journal

## 2024-01-01 - [Initial Setup]
**Vulnerability:** N/A
**Learning:** Initializing the security journal.
**Prevention:** N/A

## 2024-01-21 - [DoS Prevention and Path Traversal Fix]
**Vulnerability:** The simulation configuration allowed an unbounded `days` parameter, which could lead to Denial of Service (DoS) via memory exhaustion when allocating large NumPy arrays. Additionally, the plotting function lacked input validation for the filename, posing a path traversal risk if exposed to user input.
**Learning:** Even internal simulation tools can be vulnerable to resource exhaustion if input limits are not enforced. Cross-platform path traversal protection requires handling both forward and backward slashes explicitly, especially when running tests in a Linux environment that treats backslashes as valid filename characters.
**Prevention:** Implemented a strict upper limit (36,500 days / 100 years) for the simulation duration and added comprehensive filename validation to reject path separators (`/`, `\`, `..`).
