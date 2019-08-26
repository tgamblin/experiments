#!/usr/bin/env python3

import pandas as pd
import string


# Dataframe with a number column and a letter column
df = pd.DataFrame({"num": range(26), "alpha": [c for c in string.ascii_lowercase]})
print(df)
print()

# make the indexes letters
df.set_index("alpha", drop=True, inplace=True, verify_integrity=True)
print(df)
print()

# introduce some abbiguity
df["alpha"] = df.index.map(lambda c: "c" if c == "b" else c)
print(df)
print()

# this gives a ValueError:
# ValueError: 'alpha' is both an index level and a column label, which is ambiguous.
try:
    df.groupby("alpha").agg("sum")
    assert False
except ValueError as e:
    print("ValueError:", e)
    print()

# need to drop the index first
index_names = df.index.names
df.reset_index(inplace=True, drop=True)
print(df)
print()

# then do the groupby/agg, but this excludes alpha b/c it's now the
# index.  we preserve the column by using as_index=False, then setting
# the index later with drop=False.
#
# Would be nice to find cleaner ways to do this.
df = df.groupby("alpha", as_index=False).agg("sum")
df.set_index(index_names, drop=False, inplace=True)
print(df)
print()
