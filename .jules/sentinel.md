## 2026-01-31 - Path Traversal in File Output
**Vulnerability:** The `plot_results` function allowed arbitrary filenames, enabling potential path traversal (e.g., `../../etc/passwd`) if the filename input was controlled by a user.
**Learning:** Even in internal simulation tools, public functions can be misused if they don't validate inputs. Assuming "safe usage" by the caller is a security anti-pattern.
**Prevention:** Always validate file paths when writing to disk. Use `os.path.basename` to restrict writes to the current directory, or strictly validate against an allowed directory list.
