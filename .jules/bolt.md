## 2024-12-23 - [Pandas Loop Optimization]
**Learning:** Iterating through a Pandas DataFrame using `.iloc` inside a loop is a significant performance bottleneck because it creates a new Series object for each row.
**Action:** Always pre-extract columns to NumPy arrays (`df['col'].values`) before iterating if row-by-row processing is required (e.g., for stateful simulations). This simple change can yield 4x-100x speedups.

## 2025-12-30 - [Vectorized Simulation]
**Learning:** Replacing iterative `for` loops with NumPy vectorization (e.g., `np.cumsum`, `np.exp`) for stochastic processes like Geometric Brownian Motion is dramatically faster but alters the random number generation sequence compared to iterative calls, even with the same seed.
**Action:** When vectorizing simulations, verify that strict deterministic reproduction of the *exact same* path isn't required by downstream tests, or accept that the "same seed" will produce a statistically equivalent but numerically different path.

## 2026-02-02 - [Date Formatting in Loops]
**Learning:** Formatting dates inside a loop using `pd.Timestamp.strftime` is a major performance bottleneck; pre-calculating date strings using `np.datetime_as_string` outside the loop yields significant speedups (observed ~16x for the formatting operation).
**Action:** When iterating over dates for logging or output, pre-calculate the formatted strings using NumPy's `datetime_as_string` (with `.astype(object)` for native strings) instead of converting each timestamp individually inside the loop.
