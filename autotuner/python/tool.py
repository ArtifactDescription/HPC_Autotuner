import numpy as np
import pandas as pd

def df_intersection(df1, df2, cols):
    df1_idx = df1.set_index(cols).index
    df2_idx = df2.set_index(cols).index
    df1_mask = df1_idx.isin(df2_idx)
    df2_mask = df2_idx.isin(df1_idx)
    df1 = df1.loc[df1_mask]
    df2 = df2.loc[df2_mask]
    intsct_df = df1.reset_index(drop=True)
    return intsct_df

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
        print "Error: len(colns) = %d, len(vals) = %d" % (num, len(vals))
    for i in range(num):
        mask = (df[colns[i]].values == vals[i])
        df = df.loc[mask]
    rem_colns = [i for i in df.columns.tolist() if i not in colns]
    return df[rem_colns]

def df_ext(df, colns, vals):
    cols = np.asarray([np.asarray(vals) for i in range(df.shape[0])])
    new_df = pd.DataFrame(np.c_[cols, df.values], columns=colns + df.columns.tolist())
    return new_df

# The index of df should be 0, 1, 2, 3, ... in advance by df = df.reset_index(drop=True)
def get_top_idx(df, coln, topn):
    topn = int(topn)
    if (topn <= 0):
        print "Error: in get_top_idx(), topn <= 0!"
    topn = max(1, min(topn, df.shape[0]))
    col_idx = df.columns.tolist().index(coln)
    top_idx = np.argsort(df.values[:, col_idx])[:topn]
    return top_idx

def gen_top_df(df, coln, topn=1):
    top_idx = get_top_idx(df, coln, max(1, topn))
    top_df = pd.DataFrame(np.c_[df.values[top_idx, :]], columns=df.columns.tolist())
    return top_df

def eval_top_match(pred_df, test_df, conf_colns, perf_coln, fn=''):
    if (pred_df.shape[0] != test_df.shape[0]):
        print "Error: pred_df.shape[0] = %d, test_df.shape[0] = %d" % (pred_df.shape[0], test_df.shape[0])
    top_rs_s = set([])
    for topn in range(1, 11, 1):
        pred_df_top = gen_top_df(pred_df, perf_coln, topn)
        test_df_top = gen_top_df(test_df, perf_coln, topn)
        rs = float(df_intersection(pred_df_top, test_df_top, conf_colns).shape[0]) / topn * 100
        topp = float(topn) / test_df.shape[0]
        top_rs_s.add((topp * 100, topn, rs))
    top_rs_df = pd.DataFrame(data=list(top_rs_s), columns=['top_prec', 'top_num', 'recall_score'])
    top_rs_df = top_rs_df.sort_values(top_rs_df.columns.tolist()[0]).reset_index(drop=True)
    if (fn != ''):
        df2csv(top_rs_df, fn)
    return top_rs_df

def get_rank(df, coln, val):
    sort_df = gen_top_df(df, coln, df.shape[0]).reset_index(drop=True)
    return sort_df[coln].values.tolist().index(val)

def find_top_rank(top_smpl, df, conf_colns, perf_coln):
    top_cnddt = df_intersection(df, top_smpl, conf_colns)
    top = gen_top_df(top_cnddt, perf_coln)
    print top[perf_coln].values[0]
    print get_rank(df, perf_coln, top[perf_coln].values[0])

def eval_fail(pred_df, test_df, coln='runnable'):
    pred_y = pred_df[coln].values
    test_y = test_df[coln].values
    test_vld_num = np.array(filter(lambda x: x == 1.0, test_y)).sum()
    pred_vld_num = np.array(filter(lambda x: x == 1.0, pred_y)).sum()
    vld2invld_num = np.array(filter(lambda x: x == 1.0, test_y - pred_y)).sum()
    invld2vld_num = np.array(filter(lambda x: x == 1.0, pred_y - test_y)).sum()
    recall = 100. * (test_vld_num - vld2invld_num) / test_vld_num
    precision = 100. * (pred_vld_num - invld2vld_num) / pred_vld_num
    #print "recall = %3.1f%%, precision = %3.1f%%" % (recall, precision)
    return recall, precision
    
def eval_err(pred_df, test_df, perf_coln):
    pred_y = pred_df[perf_coln].values
    test_y = test_df[perf_coln].values
    
    abs_rerr = 100. * np.abs(pred_y - test_y) / test_y
    err_prcntl = np.array([])
    for i in range(0, 101, 10):
        err_prcntl = np.append(err_prcntl, np.percentile(abs_rerr, i))
    err_prcntl_2d = [err_prcntl]
    
    for topp in (0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5):
        top_idx = get_top_idx(test_df, perf_coln, max(1, test_df.shape[0] * topp))
        abs_rerr_top = 100. * np.abs(pred_y[top_idx] - test_y[top_idx]) / test_y[top_idx]
        
        err_prcntl = np.array([])
        for i in range(0, 101, 10):
            err_prcntl = np.append(err_prcntl, np.percentile(abs_rerr_top, i))
        err_prcntl_2d = np.append(err_prcntl_2d, [err_prcntl], axis=0)
    
    err_prcntl_2d = np.append(err_prcntl_2d, [err_prcntl_2d[0, :]], axis=0)
    err_prcntl_2d = np.delete(err_prcntl_2d, (0), axis=0)
    top = 100. * np.array([0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0])
    err_prcntl_2d = np.append(np.transpose([top]), err_prcntl_2d, axis=1)
    err_prcntl_df = pd.DataFrame(np.c_[err_prcntl_2d], columns=['top_perc'] + range(0, 101, 10))
    return err_prcntl_df

