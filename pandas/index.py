#!/usr/bin/env python3

import numpy as np
import pandas as pd
import string

df = pd.DataFrame(
    {
        "alpha": [c for c in string.ascii_lowercase],
        "c1": range(1 * 26),
        "c2": range(1 * 26, 2 * 26),
        "c3": range(2 * 26, 3 * 26),
        "c4": range(3 * 26, 4 * 26),
    }
)
df.set_index("alpha", inplace=True)

print("INDEX: ", df.index.names)
print(df)
print()

new_df = df.copy()
print("INDEX: ", new_df.index.names)
print(new_df)
assert new_df.index.names == ["alpha"]
