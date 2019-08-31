#!/usr/bin/env python3

import numpy as np
import pandas as pd
import string

letters = [c for c in string.ascii_lowercase]

df = pd.DataFrame(
    {
        "alpha": letters,
        "c1": range(1 * 26),
        "c2": range(1 * 26, 2 * 26),
        "c3": range(2 * 26, 3 * 26),
        "c4": range(3 * 26, 4 * 26),
    }
)
df.set_index("alpha", inplace=True)


print(df)
print()

print(df.loc[["a", "c"]])
print()

print(df.loc[["a", "c"], df.columns])
print()

print(df.loc[["a", "c"], ["c1", "c3"]])
print()

print(df.loc["a", "c1"])
print()


rows = ["c", "e", "g"]
cols = ["c2", "c4"]
df.loc["a", cols] = np.sum(df.loc[rows, cols])
print(df)
print()


print(df.loc[letters, ["c2", "c3", "c4"]] > 5.0)
