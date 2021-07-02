import numpy as np
import pandas as pd
import glob
import modeler as mdlr
import sample as sp

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

def gen_unmeas_smpl(filens_smpl, filens_meas, filen_unmeas, paramns):
    df_smpl = sp.csv2df(glob.glob(filens_smpl), paramns)
    df_meas_perf = sp.csv2df(glob.glob(filens_meas), paramns)
    df_meas = mdlr.df_intersection(df_smpl, df_meas_perf, paramns)
    df_unmeas = pd.concat([df_smpl, df_meas]).drop_duplicates(keep=False).astype(int)
    sp.df2csv(df_unmeas, filen_unmeas)

#lmp_paramns = ['lmp_nproc', 'lmp_ppn', 'lmp_tpp', 'lmp_nstep_out', 'lmp_l2s', 'lmp_sld']
#gen_unmeas_smpl('smpl_lmp.csv', 'rslt_lmp.csv', 'smpl_lmp_unmeas.csv', lmp_paramns)

#vr_paramns = ['vr_nproc', 'vr_ppn', 'vr_tpp', 'lmp_nstep_out', 'lmp_l2s', 'lmp_sld']
#gen_unmeas_smpl('smpl_vr.csv', 'rslt_vr.csv', 'smpl_vr_unmeas.csv', vr_paramns)

hs_paramns = ['ht_x_nproc', 'ht_y_nproc', 'ht_ppn', 'ht_bufsize', 'sw_nproc', 'sw_ppn', 'ht_nout', 'ht_x', 'ht_y', 'ht_iter']
gen_unmeas_smpl('smpl_hs.csv', 'rslt_hs.csv', 'smpl_hs_unmeas.csv', hs_paramns)

#df_hs = sp.csv2df(glob.glob('../data/hs/hs.csv'), hs_paramns).drop_duplicates().reset_index(drop=True)
#print(df_hs.shape)
