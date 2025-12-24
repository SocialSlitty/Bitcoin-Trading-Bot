## 2024-12-23 - [Pandas Loop Optimization]
**Learning:** Iterating through a Pandas DataFrame using `.iloc` inside a loop is a significant performance bottleneck because it creates a new Series object for each row.
**Action:** Always pre-extract columns to NumPy arrays (`df['col'].values`) before iterating if row-by-row processing is required (e.g., for stateful simulations). This simple change can yield 4x-100x speedups.
