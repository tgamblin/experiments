#!/usr/bin/env python3

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


print(df)
print()
print(df.loc[["a", "c"], ["c1", "c3"]])
