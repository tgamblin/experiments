#!/usr/bin/env python3

import pandas as pd
import numpy as np

df1 = pd.DataFrame(np.array([1, 2, 3]))
print(df1.dtypes[0])
print(dir(df1.dtypes[0]))
print()

df2 = pd.DataFrame(np.array([object(), 2, 3]))
print(df2.dtypes[0])
print(dir(df2.dtypes[0]))
print(df2.dtypes[0].kind)
