## 2026-02-02 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function allowed arbitrary filenames, enabling users to write files to any directory the process had access to (Path Traversal).
**Learning:** Functions that write to disk using user-provided filenames must always validate the path to prevent writing outside the intended directory.
**Prevention:** Use `os.path.basename` to strip directory components or explicitly validate that the path is within the allowed directory before writing.
