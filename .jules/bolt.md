## 2024-12-23 - [Pandas Loop Optimization]
**Learning:** Iterating through a Pandas DataFrame using `.iloc` inside a loop is a significant performance bottleneck because it creates a new Series object for each row.
**Action:** Always pre-extract columns to NumPy arrays (`df['col'].values`) before iterating if row-by-row processing is required (e.g., for stateful simulations). This simple change can yield 4x-100x speedups.

## 2025-12-30 - [Vectorized Simulation]
**Learning:** Replacing iterative `for` loops with NumPy vectorization (e.g., `np.cumsum`, `np.exp`) for stochastic processes like Geometric Brownian Motion is dramatically faster but alters the random number generation sequence compared to iterative calls, even with the same seed.
**Action:** When vectorizing simulations, verify that strict deterministic reproduction of the *exact same* path isn't required by downstream tests, or accept that the "same seed" will produce a statistically equivalent but numerically different path.

## 2026-02-04 - [Vectorized Date Formatting]
**Learning:** `np.datetime_as_string(arr, unit='D')` correctly handles `datetime64[s]` input (standard from Pandas DataFrame creation) by truncating to Day precision, confirming it as a robust replacement for `strftime` inside loops.
**Action:** Use `np.datetime_as_string(..., unit='D').astype(object)` to pre-calculate date strings outside of loops involving large datasets, as it avoids the massive overhead of creating `pd.Timestamp` objects per iteration.
