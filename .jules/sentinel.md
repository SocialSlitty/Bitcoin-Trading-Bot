## 2024-01-15 - Prevented Path Traversal in File Output
**Vulnerability:** The `plot_results` function accepted any string as a filename, allowing path traversal (e.g., `../evil.png` or `/etc/passwd`) which could overwrite arbitrary files on the system if running with sufficient privileges.
**Learning:** Even internal helper functions like `plot_results` should validate file paths if there's any chance user input (or configuration) could influence them. Relying on "it's just a simulation script" is insecure by default.
**Prevention:** Validate that output filenames do not contain path separators or directory components using `os.path.basename(filename) == filename` to enforce writing only to the intended directory.
