# This program is to test the performance differences between standard loop, .apply() and vectorization method
# It compares three ways to calculate the same value (the Euclidean distance from the origin) for 1 million rows of data.


import pandas as pd
import numpy as np
import time

# 1. Create a sample dataset with 1,000,000 rows
n = 1_000_000
df = pd.DataFrame({
    'a': np.random.rand(n),
    'b': np.random.rand(n)
})

# A simple math function to apply to each row
def calculate_distance(row):
    return np.sqrt(row['a']**2 + row['b']**2)

print(f"--- Benchmarking {n:,} rows ---")

# --- Method 1: The Standard Loop (iterrows) ---
# This is usually the slowest way as it iterates row-by-row in Python.
start = time.time()
result_loop = []
for index, row in df.iterrows():
    result_loop.append(calculate_distance(row))
loop_time = time.time() - start
print(f"Standard Loop:  {loop_time:.4f} seconds")

# --- Method 2: Pandas .apply() ---
# Often mistaken for vectorization, but it's still a loop under the hood.
start = time.time()
result_apply = df.apply(calculate_distance, axis=1)
apply_time = time.time() - start
print(f"Pandas .apply:  {apply_time:.4f} seconds")

# --- Method 3: Vectorization (NumPy/Pandas) ---
# Operates on the entire array at once using optimized C code.
start = time.time()
result_vec = np.sqrt(df['a']**2 + df['b']**2)
vec_time = time.time() - start
print(f"Vectorization:  {vec_time:.4f} seconds")

# --- Results ---
print(f"\nVectorization is {loop_time / vec_time:.1f}x faster than a loop!")
