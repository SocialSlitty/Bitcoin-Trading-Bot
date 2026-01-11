## 2026-01-11 - Path Traversal Vulnerability in File Output

**Vulnerability:** The `plot_results` function in `src/bitcoin_sim.py` accepted a `filename` argument directly from callers without validation, allowing path traversal (e.g., `../evil.png`) or absolute path overwrites.
**Learning:** Even internal library functions should validate file paths if they accept filenames, as they might be exposed later or used in contexts where input is user-controlled.
**Prevention:** Validate that filenames do not contain path components using `os.path.dirname(filename)` or force them to specific directories. In this case, I enforced that `filename` must be a simple filename without directory separators.
