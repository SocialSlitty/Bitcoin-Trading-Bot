## 2026-01-29 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function accepted an arbitrary `filename` string and passed it directly to `matplotlib.pyplot.savefig`, allowing an attacker to overwrite files outside the intended directory using path traversal sequences (e.g., `../../etc/passwd`).
**Learning:** Functions that write to disk using user-provided filenames must explicitly validate that the filename contains no directory components unless specifically intended and sanitized.
**Prevention:** Use `os.path.basename(filename) == filename` to enforce that only a filename (and not a path) is provided, locking output to the current working directory.
