## 2026-01-05 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function accepted an arbitrary filename and passed it directly to `plt.savefig()`, allowing writing to arbitrary paths (Path Traversal).
**Learning:** Utility functions that take filenames as input often assume trusted input, but in a library or reusable context, they can become vulnerabilities.
**Prevention:** Always validate filenames using `pathlib` to ensure they do not contain directory components (`parts > 1`) unless writing to subdirectories is explicitly supported and validated against a whitelist.
