## 2024-12-23 - [Pandas Loop Optimization]
**Learning:** Iterating through a Pandas DataFrame using `.iloc` inside a loop is a significant performance bottleneck because it creates a new Series object for each row.
**Action:** Always pre-extract columns to NumPy arrays (`df['col'].values`) before iterating if row-by-row processing is required (e.g., for stateful simulations). This simple change can yield 4x-100x speedups.

## 2025-12-30 - [Vectorized Simulation]
**Learning:** Replacing iterative `for` loops with NumPy vectorization (e.g., `np.cumsum`, `np.exp`) for stochastic processes like Geometric Brownian Motion is dramatically faster but alters the random number generation sequence compared to iterative calls, even with the same seed.
**Action:** When vectorizing simulations, verify that strict deterministic reproduction of the *exact same* path isn't required by downstream tests, or accept that the "same seed" will produce a statistically equivalent but numerically different path.

## 2026-01-23 - [Date Formatting in Loops]
**Learning:** Formatting dates inside a loop using `pd.Timestamp.strftime` is a major performance bottleneck (approx 0.8ms per call). Using `np.datetime_as_string` vectorized on the array outside the loop is orders of magnitude faster (15x-20x speedup).
**Action:** Pre-calculate date strings using `np.datetime_as_string(dates, unit='D').astype(object)` before entering any loop that requires string representations of dates. Use `.astype(object)` to ensure compatibility with Python string operations.
