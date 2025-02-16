import numpy as np
import pandas as pd

s = pd.Series([1, 3, 5, np.nan, 6, 8])
s.replace(np.nan, 0, inplace=True)
s.astype(int)
print(s)