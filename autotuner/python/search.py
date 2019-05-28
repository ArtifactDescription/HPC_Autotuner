import math
import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution

import data

def obj_func_lv(x, *params):
    lmp_nproc = round(x[0])
    lmp_ppw = round(x[1])
    lmp_nthread = round(x[2])
    lmp_io_step = round(x[3]) * 50
    vr_nproc = round(x[4])
    vr_ppw = round(x[5])
    vr_nthread = round(x[6])
    x_chk = np.array([lmp_nproc, lmp_ppw, lmp_nthread, lmp_io_step, vr_nproc, vr_ppw, vr_nthread])
    y = float('inf')
    if (lmp_nproc >= lmp_ppw and vr_nproc >= vr_ppw):
        if (lmp_nproc % lmp_ppw == 0 and vr_nproc % vr_ppw == 0):
            nodes = lmp_nproc // lmp_ppw + vr_nproc // vr_ppw
        elif (lmp_nproc % lmp_ppw == 0 or vr_nproc % vr_ppw == 0):
            nodes = lmp_nproc // lmp_ppw + vr_nproc // vr_ppw + 1
        else:
            nodes = lmp_nproc // lmp_ppw + vr_nproc // vr_ppw + 2
        if (nodes <= data.num_node):
            algo = params[0]
            mdls = params[1:]
            if (algo == 'cmtl_ch'):
                mdl1_chk, mdl1, mdl2_chk, mdl2 = mdls[0], mdls[1], mdls[2], mdls[3]
                mdl_chk, mdl = mdls[4], mdls[5]
                y1, y2 = float('inf'), float('inf')
                x1 = x_chk[:4]
                y1_chk = mdl1_chk.predict([x1])[0]
                if (y1_chk >= 0.0005):
                    y1 = mdl1.predict([x1])[0]
                x2 = np.hstack((x_chk[4:7], [x_chk[3]]))
                y2_chk = mdl2_chk.predict([x2])[0]
                if (y2_chk >= 0.0005):
                    y2 = mdl2.predict([x2])[0]
                x_p = np.concatenate((x_chk, np.array([y1, y2])), axis=0)
                y_chk = mdl_chk.predict([x_p])[0]
                if (y_chk >= 0.0005):
                    y = mdl.predict([x_p])[0]
            elif (algo == 'cmtl_wh'):
                in_mdl_chk, in_mdl = mdls[0], mdls[1]
                mdl_chk, mdl = mdls[2], mdls[3]
                y_in = float('inf')
                x_in = np.concatenate((np.array(data.lmp_in_params), x_chk), axis=0)
                y_in_chk = in_mdl_chk.predict([x_in])[0]
                if (y_in_chk >= 0.0005):
                    y_in = in_mdl.predict([x_in])[0]
                x_p = np.concatenate((x_chk, np.array([y_in])), axis=0)
                y_chk = mdl_chk.predict([x_p])[0]
                if (y_chk >= 0.0005):
                    y = mdl.predict([x_p])[0]
            else:
                mdl_chk = mdls[0]
                mdl = mdls[1]
                y_chk = mdl_chk.predict([x_chk])[0]
                if (y_chk >= 0.0005):
                    y = mdl.predict([x_chk])[0]
    return y

def pred_top_lv(algo, mdls):
    bounds = [(2.0 - 0.1, (data.num_core - 1.0) * (data.num_node - 1.0) + 0.1), \
              (1.0 - 0.1, data.num_core - 1 + 0.1), \
              (1.0 - 0.1, 4.0 + 0.1), \
              (1.0 - 0.1, 8.0 + 0.1), \
              (2.0 - 0.1, (data.num_core - 1.0) * (data.num_node - 1.0) + 0.1), \
              (1.0 - 0.1, data.num_core - 1 + 0.1), \
              (1.0 - 0.1, 4.0 + 0.1)]
    params = (algo, ) + mdls
    result = differential_evolution(obj_func_lv, bounds, args=params)
    x = np.rint(result.x)
    if (algo == 'cmtl_ch'):
        y = obj_func_lv(x, algo, mdls[0], mdls[1], mdls[2], mdls[3], mdls[4], mdls[5])
    elif (algo == 'cmtl_wh'):
        y = obj_func_lv(x, algo, mdls[0], mdls[1], mdls[2], mdls[3])
    else:
        y = obj_func_lv(x, algo, mdls[0], mdls[1])
    x[3] *= 50
    smpl_arr = np.hstack((x, [y]))
    return smpl_arr

def obj_func_hs(x, *params):
    ht_x_nproc = round(x[0])
    ht_y_nproc = round(x[1])
    ht_ppw = round(x[2])
    ht_io_step = round(x[3]) * 4
    ht_io_buf = round(x[4])
    sw_nproc = round(x[5])
    sw_ppw = round(x[6])
    x_chk = np.array([ht_x_nproc, ht_y_nproc, ht_ppw, ht_io_step, ht_io_buf, sw_nproc, sw_ppw])
    y = float('inf')
    ht_nproc = ht_x_nproc * ht_y_nproc
    if (ht_nproc >= ht_ppw and sw_nproc >= sw_ppw):
        if (ht_nproc % ht_ppw == 0 and sw_nproc % sw_ppw == 0):
            nodes = ht_nproc // ht_ppw + sw_nproc // sw_ppw
        elif (ht_nproc % ht_ppw == 0 or sw_nproc % sw_ppw == 0):
            nodes = ht_nproc // ht_ppw + sw_nproc // sw_ppw + 1
        else:
            nodes = ht_nproc // ht_ppw + sw_nproc // sw_ppw + 2
        if (nodes <= data.num_node):
            algo = params[0]
            mdls = params[1:]

            if (algo == 'cmtl_ch'):
                mdl1_chk, mdl1, mdl2_chk, mdl2 = mdls[0], mdls[1], mdls[2], mdls[3]
                mdl_chk, mdl = mdls[4], mdls[5]
                y1, y2 = float('inf'), float('inf')
                x1 = x_chk[:5]
                y1_chk = mdl1_chk.predict([x1])[0]
                if (y1_chk >= 0.0005):
                    y1 = mdl1.predict([x1])[0]
                x2 = np.hstack((x_chk[5:7], [x_chk[3]]))
                y2_chk = mdl2_chk.predict([x2])[0]
                if (y2_chk >= 0.0005):
                    y2 = mdl2.predict([x2])[0]
                x_p = np.concatenate((x_chk, np.array([y1, y2])), axis=0)
                y_chk = mdl_chk.predict([x_p])[0]
                if (y_chk >= 0.0005):
                    y = mdl.predict([x_p])[0]
            elif (algo == 'cmtl_wh'):
                in_mdl_chk, in_mdl = mdls[0], mdls[1]
                mdl_chk, mdl = mdls[2], mdls[3]
                y_in = float('inf')
                x_in = np.concatenate((np.array(data.ht_in_params), x_chk), axis=0)
                y_in_chk = in_mdl_chk.predict([x_in])[0]
                if (y_in_chk >= 0.0005):
                    y_in = in_mdl.predict([x_in])[0]
                x_p = np.concatenate((x_chk, np.array([y_in])), axis=0)
                y_chk = mdl_chk.predict([x_p])[0]
                if (y_chk >= 0.0005):
                    y = mdl.predict([x_p])[0]
            else:
                mdl_chk = mdls[0]
                mdl = mdls[1]
                y_chk = mdl_chk.predict([x_chk])[0]
                if (y_chk >= 0.0005):
                    y = mdl.predict([x_chk])[0]
    return y

def pred_top_hs(algo, mdls):
    max_nproc = (data.num_core - 1.0) * (data.num_node - 1.0)
    bounds = [(2.0 - 0.1, math.floor(math.sqrt(max_nproc)) + 0.1), \
              (2.0 - 0.1, math.floor(math.sqrt(max_nproc)) + 0.1), \
              (1.0 - 0.1, data.num_core - 1 + 0.1), \
              (1.0 - 0.1, 8.0 + 0.1), \
              (1.0 - 0.1, 40.0 + 0.1), \
              (2.0 - 0.1, max_nproc + 0.1), \
              (1.0 - 0.1, data.num_core - 1 + 0.1)]
    params = (algo, ) + mdls
    result = differential_evolution(obj_func_hs, bounds, args=params)
    x = np.rint(result.x)
    if (algo == 'cmtl_ch'):
        y = obj_func_hs(x, algo, mdls[0], mdls[1], mdls[2], mdls[3], mdls[4], mdls[5])
    elif (algo == 'cmtl_wh'):
        y = obj_func_hs(x, algo, mdls[0], mdls[1], mdls[2], mdls[3])
    else:
        y = obj_func_hs(x, algo, mdls[0], mdls[1])
    x[3] *= 4
    smpl_arr = np.hstack((x, [y]))
    return smpl_arr

def get_pred_top_smpl(algo, mdls, conf_colns, perf_coln, topn=10):
    slctR = 0.5
    cnddtn = int(float(topn) / slctR)
    app_name = data.get_name(conf_colns)
    for i in range(cnddtn):
        if (app_name == 'lv'):
            smpl_arr = pred_top_lv(algo, mdls)
        elif (app_name == 'hs'):
            smpl_arr = pred_top_hs(algo, mdls)

        if (i == 0):
            smpls_arr = smpl_arr
        else:
            smpls_arr = np.vstack((smpls_arr, smpl_arr))
    smpl_df = pd.DataFrame(np.c_[smpls_arr], columns=conf_colns + [perf_coln])
    top_smpl_df = smpl_df.drop_duplicates().sort_values([perf_coln]).reset_index(drop=True).head(topn)
    return top_smpl_df

