## 2024-03-23 - Date Formatting Anti-Pattern
**Learning:** `pd.Timestamp.strftime` inside a loop is extremely slow. Using `np.datetime_as_string` vectorized outside the loop is ~9-15x faster. However, if the loop processes only a slice of the data, the vectorization must also be sliced to avoid O(N) overhead for unused data.
**Action:** Always slice the source array before applying expensive vector operations if only a subset is needed.

## 2024-03-23 - Optimization Scope Alignment
**Learning:** Optimizing a full dataset operation (O(N)) when the consuming loop is fixed-window (O(1)) can introduce a regression if not sliced correctly.
**Action:** Verify the loop range and slice the pre-calculated arrays to match `range(start_idx, end_idx)`.
