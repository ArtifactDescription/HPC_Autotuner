import numpy as np
import pandas as pd
import xgboost as xgb
import sample as sp

def df_intersection(df1, df2, cols):
    df_intsct = df1.merge(df2[cols].drop_duplicates(), on=cols, suffixes=('', ''))
    return df_intsct


def df_sub(df1, df2, cols):
    df_intsct = df_intersection(df1, df2, cols)
    df_diff = pd.concat([df1, df_intsct]).drop_duplicates(keep=False).reset_index(drop=True)
    return df_diff


def df_union(df1, df2):
    df_union = pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)
    return df_union


def get_top_idx(df_smpl, perfn, num_top=1):
    num_top = int(num_top)
    if (num_top <= 0):
        print("Error: in get_top_idx(), num_top <= 0!")
    num_top = max(1, min(num_top, df_smpl.shape[0]))
    col_idx = df_smpl.columns.tolist().index(perfn)
    top_idx = np.argsort(df_smpl.values[:, col_idx])[:num_top]
    return top_idx


def gen_top_df(df_smpl, perfn, num_top=1):
    top_idx = get_top_idx(df_smpl, perfn, max(1, num_top))
    df_top = pd.DataFrame(np.c_[df_smpl.values[top_idx, :]], columns=df_smpl.columns.tolist())
    return df_top


def eval_recall(df_pred, df_test, confn, perfn, num_top=10):
    if (df_pred.shape[0] != df_test.shape[0]):
        print("Error: df_pred.shape[0] = %d, df_test.shape[0] = %d" % (df_pred.shape[0], df_test.shape[0]))
    recalls = []
    for idx_top in range(1, num_top + 1, 1):
        df_pred_top = gen_top_df(df_pred, perfn, idx_top)
        df_test_top = gen_top_df(df_test, perfn, idx_top)
        recall = float(df_intersection(df_pred_top, df_test_top, confn).shape[0]) / idx_top * 100
        pct_top = float(idx_top) / df_test.shape[0]
        recalls.append([pct_top * 100, idx_top, recall])
    df_recall = pd.DataFrame(recalls, columns=['pct_top', 'num_top', 'recall_score'])
    return df_recall


def eval_recall_rand(df_rand, confn, perfn, num_top=25):
    recalls = []
    for idx_top in range(1, num_top + 1, 1):
        df_rank = gen_top_df(df_rand, perfn, idx_top)
        recall = float(df_intersection(df_rand.head(idx_top), df_rank, confn).shape[0]) / idx_top * 100
        recalls.append([idx_top, recall])
    df_recall = pd.DataFrame(recalls, columns=['num_top', 'recall_score'])
    return df_recall


def eval_mape(df_pred, df_test, perfn, pcts_top=[0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]):
    y_pred = df_pred[perfn].values
    y_test = df_test[perfn].values

    s_mape = set([])
    for pct_top in pcts_top:
        top_idx = get_top_idx(df_test, perfn, max(1, df_test.shape[0] * pct_top))
        ape_top = 100. * np.abs(y_pred[top_idx] - y_test[top_idx]) / y_test[top_idx]
        s_mape.add((pct_top * 100, np.percentile(ape_top, 50)))
    ape_all = 100. * np.abs(y_pred - y_test) / y_test
    s_mape.add((100, np.percentile(ape_all, 50)))
    df_mape = pd.DataFrame(data=list(s_mape), columns=['pct_top', 'MAPE'])
    df_mape = df_mape.sort_values(['pct_top']).reset_index(drop=True)
    return df_mape


def train_mdl(df_train, confn, perfn, mdl=None):
    X_train = df_train[confn].values
    y_train = df_train[perfn].values
    mdl = xgb.XGBRegressor(max_depth=10, n_estimators=200).fit(X_train, y_train, xgb_model=mdl)
    return mdl


def pred_top(df_train, df_test, confn, perfn, num_top=1, stats=True):
    mdl = train_mdl(df_train, confn, perfn)
    X_test = df_test[confn].values
    y_pred = mdl.predict(X_test)
    df_pred = pd.DataFrame(np.c_[X_test, y_pred], columns=confn + [perfn])

    df_top_pred = gen_top_df(df_pred, perfn, num_top)
    if (stats):
        df_recall = eval_recall(df_pred, df_test, confn, perfn)
        df_mape = eval_mape(df_pred, df_test, perfn)
        return df_top_pred, df_recall, df_mape
    else:
        return df_top_pred


def sum_comp_time(df_vld, exec_alias='exec_time', comp_alias='comp_time'):
    if (df_vld.shape[0] == 0):
        return 0.0
    if (all([x not in df_vld.columns.tolist() for x in [exec_alias, comp_alias]])):
        return -1.0

    name = sp.get_name(df_vld)
    if (name != 'lmp' and name != 'vr' and name != 'lv' \
        and name != 'ht' and name != 'sw' and name != 'hs' \
        and name != 'gs' and name != 'pdf' and name != 'gp' \
        and name != 'gvpv' and name != 'gplot' and name != 'pplot' \
       ):
        print("Error: in sum_comp_time(), unknown dataframe!")
        return -1.0

    if (comp_alias in df_vld.columns.tolist()):
        vld_time = df_vld[comp_alias].values.sum()
    else:
        df_comp = exec2comp_df(df_vld, exec_alias, comp_alias)
        vld_time = df_comp[comp_alias].values.sum()
    return vld_time

################################################################################
# Random sampling
################################################################################

def rs(df_smpl, confn, perfn, num_smpl):
    df_train = df_smpl.head(num_smpl)
    df_top_pred, df_recall, df_mape = pred_top(df_train, df_smpl, confn, perfn)
    top_perf = df_intersection(df_smpl, df_top_pred, confn)[perfn].values[0]
    comp_time = sum_comp_time(df_smpl.head(num_smpl))
    return top_perf, df_recall, df_mape, comp_time


################################################################################
# Active learning
################################################################################

def al(df_smpl, confn, perfn, num_smpl, pct_rand, num_iter):
    num_rand = int(num_smpl * pct_rand)
    df_train = df_smpl.head(num_rand)
    df_top_pred = pred_top(df_train, df_smpl, confn, perfn, num_smpl, False)

    nspi = int((num_smpl - num_rand) / num_iter)
    for iter_idx in range(num_iter):
        curr_ns = num_smpl - nspi * (num_iter - 1 - iter_idx)

        df_top_pred = df_top_pred.sort_values([perfn]).reset_index(drop=True)
        df_train_incr = df_intersection(df_smpl, df_top_pred.head(nspi), confn)
        df_train = df_union(df_train, df_train_incr)

        last_num = nspi
        while (df_train.shape[0] < curr_ns):
            last_num = last_num + 1
            df_train_incr = df_intersection(df_smpl, df_top_pred.head(last_num).tail(1), confn)
            df_train = df_union(df_train, df_train_incr)

        if (iter_idx < num_iter - 1):
            df_top_pred = pred_top(df_train, df_smpl, confn, perfn, num_smpl, False)
        else:
            df_top_pred, df_recall, df_mape = pred_top(df_train, df_smpl, confn, perfn)

    top_perf = df_intersection(df_smpl, df_top_pred, confn)[perfn].values[0]
    comp_time = sum_comp_time(df_train)
    return top_perf, df_recall, df_mape, comp_time


################################################################################
# GEIST
################################################################################

def ctgr_label(df_bs, perfn, perc_opt):
    threshold = np.percentile(df_bs[perfn].values, perc_opt * 100)
    opt_mask = (df_bs[perfn].values < threshold)
    opt_idx = df_bs.loc[opt_mask].index
    df_bs['opt'].values[opt_idx] = 1
    no_mask = (df_bs[perfn].values >= threshold)
    no_idx = df_bs.loc[no_mask].index
    df_bs['opt'].values[no_idx] = 0
    return df_bs


def get_strength(df_smpl1, df_smpl2):
    df_name = sp.get_name(df_smpl1)
    if (df_name == 'lv'):
        strength = abs(df_smpl1['lmp_nproc'].values[0] - df_smpl2['lmp_nproc'].values[0]) \
                 / max(df_smpl1['lmp_nproc'].values[0], df_smpl2['lmp_nproc'].values[0]) \
                 + abs(df_smpl1['vr_nproc'].values[0] - df_smpl2['vr_nproc'].values[0]) \
                 / max(df_smpl1['vr_nproc'].values[0], df_smpl2['vr_nproc'].values[0])
    elif (df_name == 'hs'):
        ht_nproc1 = df_smpl1['ht_x_nproc'].values[0] * df_smpl1['ht_y_nproc'].values[0]
        ht_nproc2 = df_smpl2['ht_x_nproc'].values[0] * df_smpl2['ht_y_nproc'].values[0]
        strength = abs(ht_nproc1 - ht_nproc2) \
                 / max(ht_nproc1, ht_nproc2) \
                 + abs(df_smpl1['sw_nproc'].values[0] - df_smpl2['sw_nproc'].values[0]) \
                 / max(df_smpl1['sw_nproc'].values[0], df_smpl2['sw_nproc'].values[0])
    elif (df_name == 'gp' or df_name == 'gpv' or df_name == 'gvpv'):
        strength = abs(df_smpl1['gs_nproc'].values[0] - df_smpl2['gs_nproc'].values[0]) \
                 / max(df_smpl1['gs_nproc'].values[0], df_smpl2['gs_nproc'].values[0]) \
                 + abs(df_smpl1['pdf_nproc'].values[0] - df_smpl2['pdf_nproc'].values[0]) \
                 / max(df_smpl1['pdf_nproc'].values[0], df_smpl2['pdf_nproc'].values[0])
    else:
        strength = 0
    strength = strength / 2.0
    return strength


def pred_label(df_un, df_bs, perc_opt):
    for i in range(df_un.shape[0]):
        prob_opt = 0
        for j in range(df_bs.shape[0]):
            smpl = df_bs.head(j+1).tail(1)
            prob_opt = prob_opt + smpl['opt'].values[0] * get_strength(df_un.head(i+1).tail(1), smpl)
        prob_opt = perc_opt + prob_opt
        prob_no = 1 - perc_opt
        df_un['opt'].values[i] = prob_opt / (prob_opt + prob_no)
    threshold = np.percentile(df_un['opt'].values, 1 - perc_opt)
    return df_un[df_un.opt >= threshold]


def geist(df_smpl, confn, perfn, num_smpl, pct_rand, num_iter):
    rand_seed = 2019
    perc_opt = 0.05

    num_rand = int(num_smpl * pct_rand)
    df_bs = df_smpl.head(num_rand).copy()
    df_bs = pd.DataFrame(np.c_[df_bs.values, np.zeros(df_bs.shape[0])], \
            columns=df_bs.columns.tolist() + ['opt'])
    df_un = df_smpl.tail(df_smpl.shape[0] - num_rand).copy()
    df_un = pd.DataFrame(np.c_[df_un.values, np.zeros(df_un.shape[0])], \
            columns=df_un.columns.tolist() + ['opt'])

    nspi = int((num_smpl - num_rand) / num_iter)
    for iter_idx in range(num_iter):
        df_bs = ctgr_label(df_bs, perfn, perc_opt)
        df_un = pred_label(df_un, df_bs, perc_opt)
        df_un = df_un.sort_values(confn).reset_index(drop=True)
        df_un = df_un.sample(frac=1, random_state=rand_seed).reset_index(drop=True)
        df_bs = df_bs.append(df_un.head(nspi))
        df_un = df_un.tail(df_un.shape[0] - nspi)

    df_top_pred, df_recall, df_mape = pred_top(df_bs, df_smpl, confn, perfn)
    top_perf = df_intersection(df_smpl, df_top_pred, confn)[perfn].values[0]
    comp_time = sum_comp_time(df_bs)
    return top_perf, df_recall, df_mape, comp_time


################################################################################
# ALpH 
################################################################################

def preproc_cpnt_pred(cpnt_mdls, cpnt_confns, cpnt_perfns, df_smpl, confn, perfn):
    num_cpnt = len(cpnt_mdls)
    if (len(cpnt_confns) != num_cpnt):
        print("Error: len(cpnt_mdls) != len(cpnt_confns)")

    for i in range(num_cpnt):
        if isinstance(cpnt_mdls[i], xgb.sklearn.XGBRegressor):
            X_cpnt = df_smpl[cpnt_confns[i]].values
            y_cpnt_pred = cpnt_mdls[i].predict(X_cpnt)
            if (i == 0):
                y_cpnts_pred = np.array([y_cpnt_pred])
            else:
                y_cpnts_pred = np.append(y_cpnts_pred, [y_cpnt_pred], axis=0)
    df_cpnt_pred = pd.DataFrame(np.c_[df_smpl[confn].values, np.transpose(y_cpnts_pred), \
            df_smpl[perfn].values], columns=confn + cpnt_perfns + [perfn])
    return df_cpnt_pred


def pred_top_learn_cmbn(cpnt_mdls, cpnt_confns, df_train, df_test, confn, perfn, \
        num_top=1, stats=True):
    num_cpnt = len(cpnt_mdls)
    cpnt_perfns = []
    for i in range(num_cpnt):
        if isinstance(cpnt_mdls[i], xgb.sklearn.XGBRegressor):
            cpnt_perfns = cpnt_perfns + [perfn + str(i)]
    df_train_cmbn = preproc_cpnt_pred(cpnt_mdls, cpnt_confns, cpnt_perfns, \
                                           df_train, confn, perfn)
    df_test_cmbn = preproc_cpnt_pred(cpnt_mdls, cpnt_confns, cpnt_perfns, \
                                          df_test, confn, perfn)
    return pred_top(df_train_cmbn, df_test_cmbn, confn + cpnt_perfns, perfn, \
                         num_top, stats)


def alph(cpnt_mdls, df_smpl, cpnt_confns, confn, perfn, num_smpl, pct_rand, num_iter):
    num_rand = int(num_smpl * pct_rand)
    df_train = df_smpl.head(num_rand)
    df_top_pred = pred_top_learn_cmbn(cpnt_mdls, cpnt_confns, df_train, df_smpl, confn, 
            perfn, num_smpl, False)

    nspi = int((num_smpl - num_rand) / num_iter)
    for iter_idx in range(num_iter):
        curr_ns = num_smpl - nspi * (num_iter - 1 - iter_idx)

        df_top_pred = df_top_pred.sort_values([perfn]).reset_index(drop=True)
        df_train_incr = df_intersection(df_smpl, df_top_pred.head(nspi), confn)
        df_train = df_union(df_train, df_train_incr)

        last_num = nspi
        while (df_train.shape[0] < curr_ns):
            last_num = last_num + 1
            df_train_incr = df_intersection(df_smpl, df_top_pred.head(last_num).tail(1), confn)
            df_train = df_union(df_train, df_train_incr)

        if (iter_idx < num_iter - 1):
            df_top_pred = pred_top_learn_cmbn(cpnt_mdls, cpnt_confns, df_train, df_smpl, 
                    confn, perfn, num_smpl, False)
        else:
            df_top_pred, df_recall, df_mape = pred_top_learn_cmbn(cpnt_mdls, \
                    cpnt_confns, df_train, df_smpl, confn, perfn)

    top_perf = df_intersection(df_smpl, df_top_pred, confn)[perfn].values[0]
    comp_time = sum_comp_time(df_train)
    return top_perf, df_recall, df_mape, comp_time


################################################################################
# ALIC 
################################################################################

def cmbn_cpnt_pred(y_cpnts_pred, perfn):
    if (perfn == 'exec_time'):
        y_pred = np.concatenate(y_cpnts_pred, axis=0).max(axis=0)
    elif (perfn == 'comp_time'):
        y_pred = np.concatenate(y_cpnts_pred, axis=0).sum(axis=0)
    else:
        print("Error: Unknown performance metrics!")
    return y_pred


def pred_top_anal_cmbn(cpnt_mdls, df_test, cpnt_confns, confn, perfn, num_top=1, \
        stats=True):
    num_cpnt = len(cpnt_mdls)
    if (len(cpnt_confns) != num_cpnt):
        print("Error: len(cpnt_mdls) != len(cpnt_confns)")

    y_cpnts_pred = ()
    for i in range(num_cpnt):
        X_cpnt_test = df_test[cpnt_confns[i]].values
        if isinstance(cpnt_mdls[i], xgb.sklearn.XGBRegressor):
            y_cpnt_pred = cpnt_mdls[i].predict(X_cpnt_test)
        elif isinstance(cpnt_mdls[i], float):
            y_cpnt_pred = cpnt_mdls[i] * np.ones(X_cpnt_test.shape[0])
        else:
            print(f"Unknown type of cpnt_mdls[{i}]")
        y_cpnt_pred = np.concatenate(([y_cpnt_pred], \
                [np.zeros(np.size(y_cpnt_pred))]), axis=0).max(axis=0)
        y_cpnts_pred = y_cpnts_pred + ([y_cpnt_pred], )
    y_pred = cmbn_cpnt_pred(y_cpnts_pred, perfn)
    df_pred = pd.DataFrame(np.c_[df_test[confn].values, y_pred], \
            columns=confn + [perfn])

    df_top_pred = gen_top_df(df_pred, perfn, num_top)
    if (stats):
        df_recall = eval_recall(df_pred, df_test, confn, perfn)
        df_mape = eval_mape(df_pred, df_test, perfn)
        return df_top_pred, df_recall, df_mape
    else:
        return df_top_pred


def alic(cpnt_mdls, df_smpl, cpnt_confns, confn, perfn, num_smpl, pct_rand, \
        num_iter, pct_repl=0.0, dfs_cpnt=None):
    num_rand = int(num_smpl * pct_rand)
    num_repl = min(int(num_smpl * pct_repl), num_smpl - num_rand)
    if (num_repl >= 1):
        for i in range(len(dfs_cpnt)):
            if isinstance(dfs_cpnt[i], pd.core.frame.DataFrame):
                cpnt_mdls[i] = train_mdl(dfs_cpnt[i].head(num_repl), \
                        cpnt_confns[i], perfn, cpnt_mdls[i])
            elif isinstance(dfs_cpnt[i], float):
                cpnt_mdls[i] = dfs_cpnt[i]
            else:
                print(f"Unknown type of dfs_cpnt[{i}]")

    df_top_pred = pred_top_anal_cmbn(cpnt_mdls, df_smpl, cpnt_confns, confn, \
            perfn, num_smpl, False)
    df_train = df_smpl.head(num_rand)
    nspi = int((num_smpl - num_rand - num_repl) / num_iter)
    for iter_idx in range(num_iter):
        curr_ns = num_smpl - nspi * (num_iter - 1 - iter_idx)
        
        df_top_pred = df_top_pred.sort_values([perfn]).reset_index(drop=True)
        df_train_incr = df_intersection(df_smpl, df_top_pred.head(nspi), confn)
        df_train = df_union(df_train, df_train_incr)
        
        last_num = nspi
        while (df_train.shape[0] < curr_ns):
            last_num = last_num + 1
            df_train_incr = df_intersection(df_smpl, \
                    df_top_pred.head(last_num).tail(1), confn)
            df_train = df_union(df_train, df_train_incr)

        if (iter_idx < num_iter - 1):
            df_top_pred = pred_top(df_train, df_smpl, confn, perfn, num_smpl, \
                    False)
        else:
            df_top_pred, df_recall, df_mape = pred_top(df_train, df_smpl, \
                    confn, perfn)

    top_perf = df_intersection(df_smpl, df_top_pred, confn)[perfn].values[0]
    comp_time = sum_comp_time(df_train)
    return top_perf, df_recall, df_mape, comp_time


################################################################################
# CEAL 
################################################################################

def ceal(cpnt_mdls, df_smpl, cpnt_confns, confn, perfn, num_smpl, pct_rand, \
        num_iter, pct_repl=0.0, dfs_cpnt=None):
    num_rand_upper = int(num_smpl * pct_rand)
    num_rand = int(max(1, num_smpl * pct_rand / 2))
    df_train = df_smpl.head(num_rand)
    df_top_pred_high = pred_top(df_train, df_smpl, confn, perfn, \
            df_smpl.shape[0], False)
    df_rmn = df_sub(df_smpl, df_train, confn) 

    num_repl = min(int(num_smpl * pct_repl), num_smpl - num_rand_upper)
    if (num_repl >= 1):
        for i in range(len(dfs_cpnt)):
            if isinstance(dfs_cpnt[i], pd.core.frame.DataFrame):
                cpnt_mdls[i] = train_mdl(dfs_cpnt[i].head(num_repl), \
                        cpnt_confns[i], perfn, cpnt_mdls[i])
            elif isinstance(dfs_cpnt[i], float):
                cpnt_mdls[i] = dfs_cpnt[i]
            else:
                print(f"Unknown type of dfs_cpnt[{i}]")
    df_top_pred_low = pred_top_anal_cmbn(cpnt_mdls, df_rmn, cpnt_confns, \
            confn, perfn, df_rmn.shape[0], False)
    df_top_pred = df_top_pred_low
    low = True

    num_iter = min(num_iter, max(1, num_smpl - num_rand_upper - num_repl))
    nspi = int((num_smpl - num_rand_upper - num_repl) / num_iter)
    for iter_idx in range(num_iter):
        curr_ns = num_smpl - (num_rand_upper - num_rand) \
                - nspi * (num_iter - 1 - iter_idx)
        
        df_top_pred = df_top_pred.sort_values([perfn]).reset_index(drop=True)
        df_test = df_intersection(df_rmn, df_top_pred.head(nspi), confn)
        last_num = nspi
        while (df_train.shape[0] + df_test.shape[0] < curr_ns):
            last_num = last_num + 1
            df_test = df_intersection(df_rmn, df_top_pred.head(last_num), confn)
        df_rmn = df_sub(df_rmn, df_test, confn)

        if (df_test.shape[0] >= 2):
            df_pred_high = df_intersection(df_top_pred_high, df_test, confn)
            robust = df_intersection(df_pred_high.head(1), \
                    gen_top_df(df_test, perfn, int(df_test.shape[0] / 2)), confn).shape[0]
            if (robust < 1):
                if (iter_idx < num_iter - 1):
                    num_rand_incr = int((num_rand_upper - num_rand) / 2)
                else:
                    num_rand_incr = num_rand_upper - num_rand
                df_train = df_union(df_train, df_rmn.head(num_rand_incr))
                num_rand = num_rand + num_rand_incr
                df_rmn = df_rmn.tail(df_rmn.shape[0] - num_rand_incr)

        if (low):
            df_pred_low = df_intersection(df_top_pred_low, df_test, confn)
            df_recall_low = eval_recall(df_pred_low, df_test, confn, perfn, \
                    min(3, df_test.shape[0]))
            recall_low = df_recall_low['recall_score'].values.mean()

            df_pred_high = pred_top(df_train, df_test, confn, perfn, \
                    df_test.shape[0], False)
            df_recall_high = eval_recall(df_pred_high, df_test, confn, perfn, \
                    min(3, df_test.shape[0]))
            recall_high = df_recall_high['recall_score'].values.mean()

            if (recall_high >= recall_low):
                low = False

        df_train = df_union(df_train, df_test)
        if (iter_idx < num_iter - 1):
            df_top_pred_high = pred_top(df_train, df_rmn, confn, perfn, \
                    df_rmn.shape[0], False)
            if (low):
                df_top_pred = df_intersection(df_top_pred_low, df_rmn, confn)
            else:
                df_top_pred = df_top_pred_high
        else:
            if (num_rand_upper > num_rand):
                df_top_pred = pred_top(df_train, df_rmn, confn, perfn, \
                        num_rand_upper - num_rand, False)
                df_test = df_intersection(df_rmn, df_top_pred, confn)
                df_train = df_union(df_train, df_test)
            df_top_pred, df_recall, df_mape = pred_top(df_train, df_smpl, \
                    confn, perfn)

    top_perf = df_intersection(df_smpl, df_top_pred, confn)[perfn].values[0]
    comp_time = sum_comp_time(df_train)
    return top_perf, df_recall, df_mape, comp_time

print("Best execution time of LV:")
print(gen_top_df(sp.df_lv, 'exec_time'))
print("Best computer time of LV:")
print(gen_top_df(sp.df_lv, 'comp_time'))
'''
perfn = 'comp_time'
gs_mdl = train_mdl(sp.df_gs, sp.gs_confn, perfn)
pdf_mdl = train_mdl(sp.df_pdf, sp.pdf_confn, perfn)
gplot_perf = sp.df_gplot[perfn].values[0]
pplot_perf = sp.df_pplot[perfn].values[0]
num_smpl = 100
pct_rand = 0.3
num_iter = 3
pct_repl = 0.3
rslt = rs(sp.df_gvpv, sp.gvpv_confn, perfn, num_smpl)
rslt = al(sp.df_gvpv, sp.gvpv_confn, perfn, num_smpl, pct_rand, num_iter)
rslt = geist(sp.df_gvpv, sp.gvpv_confn, perfn, num_smpl, pct_rand, num_iter)
rslt = alph((gs_mdl, pdf_mdl), sp.df_gvpv, (sp.gs_confn, sp.pdf_confn), \
        sp.gvpv_confn, perfn, num_smpl, pct_rand, num_iter)
rslt = alic([gs_mdl, pdf_mdl, gplot_perf, pplot_perf], sp.df_gvpv, \
        (sp.gs_confn, sp.pdf_confn, sp.gplot_confn, sp.pplot_confn), \
        sp.gvpv_confn, perfn, num_smpl, pct_rand, num_iter)
rslt = alic([None, None, None, None], sp.df_gvpv, \
        (sp.gs_confn, sp.pdf_confn, sp.gplot_confn, sp.pplot_confn), \
        sp.gvpv_confn, perfn, num_smpl, pct_rand, num_iter, pct_repl, \
        (sp.df_gs, sp.df_pdf, gplot_perf, pplot_perf))
rslt = ceal([gs_mdl, pdf_mdl, gplot_perf, pplot_perf], sp.df_gvpv, \
        (sp.gs_confn, sp.pdf_confn, sp.gplot_confn, sp.pplot_confn), \
        sp.gvpv_confn, perfn, num_smpl, pct_rand, num_iter)
rslt = ceal([None, None, None, None], sp.df_gvpv, \
        (sp.gs_confn, sp.pdf_confn, sp.gplot_confn, sp.pplot_confn), \
        sp.gvpv_confn, perfn, num_smpl, pct_rand, num_iter, pct_repl, \
        (sp.df_gs, sp.df_pdf, gplot_perf, pplot_perf))
for i in range(len(rslt)):
    print(rslt[i])
'''
