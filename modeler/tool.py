import numpy as np
import pandas as pd

def df_sub(df1, df2, cols):
    intsct_df = df_intersection(df1, df2, cols)
    diff_df = pd.concat([df1, intsct_df]).drop_duplicates(keep=False).reset_index(drop=True)
    return diff_df

def df_union(df1, df2):
    union_df = pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)
    return union_df

def df_filter(df, colns, vals):
    num = len(colns)
    if (num != len(vals)):
        print("Error: len(colns) = %d, len(vals) = %d" % (num, len(vals)))
    for i in range(num):
        mask = (df[colns[i]].values == vals[i])
        df = df.loc[mask]
    rem_colns = [i for i in df.columns.tolist() if i not in colns]
    return df[rem_colns]

def df_ext(df, colns, vals):
    cols = np.asarray([np.asarray(vals) for i in range(df.shape[0])])
    new_df = pd.DataFrame(np.c_[cols, df.values], columns=colns + df.columns.tolist())
    return new_df

