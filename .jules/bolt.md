## 2024-12-23 - [Pandas Loop Optimization]
**Learning:** Iterating through a Pandas DataFrame using `.iloc` inside a loop is a significant performance bottleneck because it creates a new Series object for each row.
**Action:** Always pre-extract columns to NumPy arrays (`df['col'].values`) before iterating if row-by-row processing is required (e.g., for stateful simulations). This simple change can yield 4x-100x speedups.

## 2025-12-30 - [Vectorized Simulation]
**Learning:** Replacing iterative `for` loops with NumPy vectorization (e.g., `np.cumsum`, `np.exp`) for stochastic processes like Geometric Brownian Motion is dramatically faster but alters the random number generation sequence compared to iterative calls, even with the same seed.
**Action:** When vectorizing simulations, verify that strict deterministic reproduction of the *exact same* path isn't required by downstream tests, or accept that the "same seed" will produce a statistically equivalent but numerically different path.

## 2025-01-08 - [Date Formatting Vectorization]
**Learning:** Repeatedly calling `pd.Timestamp(dt).strftime('%Y-%m-%d')` inside a loop is extremely slow (~0.1ms per call) due to object creation and method overhead.
**Action:** Use `np.datetime_as_string(dates, unit='D').astype(object)` to pre-calculate all date strings in a single vectorized operation, which can be 15-20x faster. Ensure to slice the input array to only what is needed to avoid unnecessary computation.
