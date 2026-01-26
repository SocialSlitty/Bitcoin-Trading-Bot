## 2024-12-23 - [Pandas Loop Optimization]
**Learning:** Iterating through a Pandas DataFrame using `.iloc` inside a loop is a significant performance bottleneck because it creates a new Series object for each row.
**Action:** Always pre-extract columns to NumPy arrays (`df['col'].values`) before iterating if row-by-row processing is required (e.g., for stateful simulations). This simple change can yield 4x-100x speedups.

## 2025-12-30 - [Vectorized Simulation]
**Learning:** Replacing iterative `for` loops with NumPy vectorization (e.g., `np.cumsum`, `np.exp`) for stochastic processes like Geometric Brownian Motion is dramatically faster but alters the random number generation sequence compared to iterative calls, even with the same seed.
**Action:** When vectorizing simulations, verify that strict deterministic reproduction of the *exact same* path isn't required by downstream tests, or accept that the "same seed" will produce a statistically equivalent but numerically different path.

## 2026-01-26 - [In-place Vectorization & Buffer Reuse]
**Learning:** Reusing a single NumPy array as a buffer for multiple independent stochastic calculations (prices, volumes, high/low) reduces peak memory usage by ~50% and yields ~5x speedup by eliminating intermediate allocations.
**Action:** When generating multiple synthetic datasets (e.g., OHLCV), identify independent steps and chain in-place operations (`out=buffer`) to reuse the largest allocated array.
