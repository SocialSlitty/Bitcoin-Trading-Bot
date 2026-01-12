## 2026-01-12 - Prevent Arbitrary File Write via Path Traversal
**Vulnerability:** The `plot_results` function blindly accepted a `filename` argument and passed it to `matplotlib.pyplot.savefig`. This allowed writing files to arbitrary locations on the filesystem (e.g., `/etc/cron.d/evil`, though constrained by the file content being an image).
**Learning:** Even internal utility functions like plotting helpers can be exposed or misused. Input validation (sanitizing filenames to ensure they are just names, not paths) is crucial for any function performing file I/O.
**Prevention:** In `plot_results`, added a check using `os.path.dirname(filename)` to reject any filename containing path components.
