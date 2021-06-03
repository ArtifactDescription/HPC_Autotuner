import numpy as np
import pandas as pd
import xgboost as xgb

import data
import tool

def train_mdl(train_df, conf_colns, perf_coln):
    train_X = train_df[conf_colns].values
    train_y = train_df[perf_coln].values
    mdl = xgb.XGBRegressor(max_depth=10, n_estimators=200).fit(train_X, train_y)
    return mdl

def train_mdl_chk(train_df, conf_colns, perf_coln):
    mdl_chk = train_mdl(train_df, conf_colns, 'runnable')
    train_df_vld = data.get_vld_df(train_df)
    mdl = train_mdl(train_df_vld, conf_colns, perf_coln)
    return mdl_chk, mdl

def sprt_cmb_pred_vld(pred_y1, pred_y2):
    pred_y = np.concatenate(([pred_y1], [pred_y2]), axis=0).min(axis=0)
    return pred_y

def sprt_cmb_pred_val(pred_y1, pred_y2, perf_coln):
    if (perf_coln == 'run_time'):
        pred_y = 0.5 * (pred_y1 + pred_y2) \
                 + 0.5 * np.concatenate(([pred_y1], [pred_y2]), axis=0).max(axis=0)
    elif (perf_coln == 'mach_time'):
        pred_y = pred_y1 + pred_y2
    else:
        pred_y = np.concatenate(([pred_y1], [pred_y2]), axis=0).max(axis=0)
    return pred_y

def sprt_pred_chk(mdl1_chk, mdl2_chk, conf_df, conf1_colns, conf2_colns, conf_colns):
    test_X1_chk = conf_df[conf1_colns].values
    test_X2_chk = conf_df[conf2_colns].values
    pred_y1_chk = mdl1_chk.predict(test_X1_chk)
    pred_y2_chk = mdl2_chk.predict(test_X2_chk)
    pred_y_chk = sprt_cmb_pred_vld(pred_y1_chk, pred_y2_chk)
    for i in range(conf_df.shape[0]):
        if (pred_y_chk[i] > 0.0005):
            pred_y_chk[i] = 1.0
        else:
            pred_y_chk[i] = 0.0
    pred_df_chk = pd.DataFrame(np.c_[conf_df[conf_colns].values, pred_y_chk], \
                               columns=conf_colns + ['runnable'])
    return pred_df_chk
    
def sprt_pred_val(pred_df_chk, mdl1, mdl2, conf1_colns, conf2_colns, conf_colns, perf_coln):
    pred_df = pred_df_chk[(pred_df_chk.runnable == 1.0)]
    test_X1 = pred_df[conf1_colns].values
    test_X2 = pred_df[conf2_colns].values
    pred_y1 = mdl1.predict(test_X1)
    pred_y2 = mdl2.predict(test_X2)
    pred_y = sprt_cmb_pred_val(pred_y1, pred_y2, perf_coln)
    pred_df = pd.DataFrame(np.c_[pred_df[conf_colns].values, pred_y], \
                           columns=conf_colns + [perf_coln])
    pred_df_invld = pred_df_chk[(pred_df_chk.runnable == 0.0)]
    pred_y = np.ones(pred_df_invld.shape[0]) * float('inf')
    pred_df_invld = pd.DataFrame(np.c_[pred_df_invld[conf_colns].values, pred_y], \
                                 columns=conf_colns + [perf_coln])
    pred_df = pred_df.append(pred_df_invld).reset_index(drop=True)
    return pred_df
    
def sprt_pred_vld_val(mdl1, mdl2, test_df, conf1_colns, conf2_colns, conf_colns, perf_coln):
    test_df_vld = data.get_vld_df(test_df)
    test_X1_vld = test_df_vld[conf1_colns].values
    test_X2_vld = test_df_vld[conf2_colns].values
    pred_y1_vld = mdl1.predict(test_X1_vld)
    pred_y2_vld = mdl2.predict(test_X2_vld)
    pred_y_vld = sprt_cmb_pred_val(pred_y1_vld, pred_y2_vld, perf_coln)
    pred_df_vld = pd.DataFrame(np.c_[test_df_vld[conf_colns].values, pred_y_vld], \
                               columns=conf_colns + [perf_coln])
    
    return pred_df_vld

def sprt_pred_top_eval(train1_df, train2_df, test_df, \
                       conf1_colns, conf2_colns, conf_colns, perf_coln, topn=1, eval_flag=1):
    mdl1_chk, mdl1 = train_mdl_chk(train1_df, conf1_colns, perf_coln)
    mdl2_chk, mdl2 = train_mdl_chk(train2_df, conf2_colns, perf_coln)
    
    pred_df_chk = sprt_pred_chk(mdl1_chk, mdl2_chk, test_df, conf1_colns, conf2_colns, conf_colns)
    pred_df = sprt_pred_val(pred_df_chk, mdl1, mdl2, conf1_colns, conf2_colns, conf_colns, perf_coln)
    
    top_smpl = tool.gen_top_df(pred_df, perf_coln, topn)
    if (eval_flag != 0):
        # recall, precision = tool.eval_fail(pred_df_chk, test_df)

        pred_df_vld = sprt_pred_vld_val(mdl1, mdl2, test_df, \
                                        conf1_colns, conf2_colns, conf_colns, perf_coln)
        test_df_vld = data.get_vld_df(test_df)
        err_prcntl_df = tool.eval_err(pred_df_vld, test_df_vld, perf_coln)

        # tool.eval_top_match(pred_df_vld, test_df_vld, conf_colns, perf_coln)
        top_rs_df = tool.eval_top_match(pred_df, test_df, conf_colns, perf_coln)
        return top_smpl, err_prcntl_df, top_rs_df
    else:
        return top_smpl

def whl_pred_top_eval(train_df, test_df, conf_colns, perf_coln, topn=1, eval_flag=1, fn=''):
    mdl_chk, mdl = train_mdl_chk(train_df, conf_colns, perf_coln)
    
    test_X_chk = test_df[conf_colns].values
    pred_y_chk = mdl_chk.predict(test_X_chk)
    for i in range(test_df.shape[0]):
        if (pred_y_chk[i] > 0.0005):
            pred_y_chk[i] = 1.0
        else:
            pred_y_chk[i] = 0.0
    pred_df_chk = pd.DataFrame(np.c_[test_X_chk, pred_y_chk], columns=conf_colns + ['runnable'])
        
    pred_df = pred_df_chk[(pred_df_chk.runnable == 1.0)]
    test_X = pred_df[conf_colns].values
    pred_y = mdl.predict(test_X)
    pred_df = pd.DataFrame(np.c_[test_X, pred_y], columns=conf_colns + [perf_coln])
    pred_df_invld = pred_df_chk[(pred_df_chk.runnable == 0.0)]
    pred_y = np.ones(pred_df_invld.shape[0]) * float('inf')
    pred_df_invld = pd.DataFrame(np.c_[pred_df_invld[conf_colns].values, pred_y], \
                                 columns=conf_colns + [perf_coln])
    pred_df = pred_df.append(pred_df_invld).reset_index(drop=True)
    
    top_smpl = tool.gen_top_df(pred_df, perf_coln, topn)
    if (eval_flag != 0):
        # recall, precision = tool.eval_fail(pred_df_chk, test_df)

        test_df_vld = data.get_vld_df(test_df)
        test_X_vld = test_df_vld[conf_colns].values
        pred_y_vld = mdl.predict(test_X_vld)
        pred_df_vld = pd.DataFrame(np.c_[test_X_vld, pred_y_vld], columns=conf_colns + [perf_coln])
        err_prcntl_df = tool.eval_err(pred_df_vld, test_df_vld, perf_coln)

        # tool.eval_top_match(pred_df_vld, test_df_vld, conf_colns, perf_coln)
        top_rs_df = tool.eval_top_match(pred_df, test_df, conf_colns, perf_coln)
        
        if (fn != ''):
            perf_df = pd.DataFrame(np.c_[test_df.sort_values(conf_colns)[perf_coln].values, \
                                         pred_df.sort_values(conf_colns)[perf_coln].values], \
                                   columns=['real_'+perf_coln, 'pred_'+perf_coln])
            df2csv(perf_df, fn)
        return top_smpl, err_prcntl_df, top_rs_df
    else:
        return top_smpl
    
def whl_in_pred_top_eval(train_df, test_df, in_params, in_conf_colns, conf_colns, perf_coln, \
                         topn=1, eval_flag=1):
    mdl_chk, mdl = train_mdl_chk(train_df, in_conf_colns, perf_coln)
    
    test_num_chk = test_df.shape[0]
    in_X_chk = np.asarray([np.asarray(in_params) for i in range(test_num_chk)])
    test_X_chk = np.concatenate((in_X_chk, test_df[conf_colns].values), axis=1)
    pred_y_chk = mdl_chk.predict(test_X_chk)
    for i in range(test_num_chk):
        if (pred_y_chk[i] > 0.0005):
            pred_y_chk[i] = 1.0
        else:
            pred_y_chk[i] = 0.0
    pred_df_chk = pd.DataFrame(np.c_[test_df[conf_colns].values, pred_y_chk], \
                               columns=conf_colns + ['runnable'])
    
    pred_df = pred_df_chk[(pred_df_chk.runnable == 1.0)]
    test_num = pred_df.shape[0]
    in_X = np.asarray([np.asarray(in_params) for i in range(test_num)])
    test_X = np.concatenate((in_X, pred_df[conf_colns].values), axis=1)
    pred_y = mdl.predict(test_X)
    pred_df = pd.DataFrame(np.c_[pred_df[conf_colns].values, pred_y], \
                           columns=conf_colns + [perf_coln])
    pred_df_invld = pred_df_chk[(pred_df_chk.runnable == 0.0)]
    pred_y = pred_df_invld['runnable'].values + np.ones(pred_df_invld.shape[0]) * float('inf')
    pred_df_invld = pd.DataFrame(np.c_[pred_df_invld[conf_colns].values, pred_y], \
                                 columns=conf_colns + [perf_coln])
    pred_df = pred_df.append(pred_df_invld).reset_index(drop=True)
    
    top_smpl = tool.gen_top_df(pred_df, perf_coln, topn)
    if (eval_flag != 0):
        # recall, precision = tool.eval_fail(pred_df_chk, test_df)

        test_df_vld = data.get_vld_df(test_df)
        test_num_vld = test_df_vld.shape[0]
        in_X_vld = np.asarray([np.asarray(in_params) for i in range(test_num_vld)])
        test_X_vld = np.concatenate((in_X_vld, test_df_vld[conf_colns].values), axis=1)
        pred_y_vld = mdl.predict(test_X_vld)
        pred_df_vld = pd.DataFrame(np.c_[test_df_vld[conf_colns].values, pred_y_vld], \
                                   columns=conf_colns + [perf_coln])
        err_prcntl_df = tool.eval_err(pred_df_vld, test_df_vld, perf_coln)

        # tool.eval_top_match(pred_df_vld, test_df_vld, conf_colns, perf_coln)
        top_rs_df = tool.eval_top_match(pred_df, test_df, conf_colns, perf_coln)
        return top_smpl, err_prcntl_df, top_rs_df
    else:
        return top_smpl

def pred_perf_chk(X_arr, mdl_chk, mdl):
    pred_y_chk = mdl_chk.predict(X_arr)
    pred_y = mdl.predict(X_arr)
    for i in range(len(pred_y_chk)):
        if (pred_y_chk[i] < 0.0005):
            pred_y[i] = float('inf')
    return pred_y

def add_layer_sprt_pred(df, conf1_colns, conf2_colns, conf_colns, perf_coln, \
                        mdl1_chk, mdl1, mdl2_chk, mdl2): 
    X1 = df[conf1_colns].values
    pred_y1 = pred_perf_chk(X1, mdl1_chk, mdl1)

    X2 = df[conf2_colns].values
    pred_y2 = pred_perf_chk(X2, mdl2_chk, mdl2)

    pred_df = pd.DataFrame(np.c_[df[conf_colns].values, pred_y1, pred_y2, \
                                 df['runnable'].values, df[perf_coln].values], \
                           columns=conf_colns + [perf_coln+'1', perf_coln+'2', 'runnable', perf_coln])
    return pred_df

def add_layer_shrt_pred(df, in_params, conf_colns, perf_coln, mdl_chk, mdl):
    in_X = np.asarray([np.asarray(in_params) for i in range(df.shape[0])])
    X = np.concatenate((in_X, df[conf_colns].values), axis=1)
    pred_y = pred_perf_chk(X, mdl_chk, mdl)
    pred_df = pd.DataFrame(np.c_[df[conf_colns].values, pred_y, df['runnable'].values, \
                                 df[perf_coln].values], \
                           columns=conf_colns + [perf_coln+'0', 'runnable', perf_coln])
    return pred_df

