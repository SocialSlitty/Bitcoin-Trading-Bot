## 2026-02-06 - [Path Traversal in File Output]
**Vulnerability:** The `plot_results` function allowed arbitrary file paths (including `../` or `/tmp/`) as input for the output filename, enabling path traversal and arbitrary file write vulnerabilities.
**Learning:** Functions that accept filenames as arguments must always validate that they are strictly filenames and do not contain path components, especially if they might be exposed to user input.
**Prevention:** Use `os.path.basename(filename) != filename` to ensure the argument is a filename only, or use strict allow-lists for output directories.
