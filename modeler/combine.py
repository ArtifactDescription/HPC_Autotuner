import numpy as np
import pandas as pd
import sample as sp
import modeler as mdlr
import sys

if (len(sys.argv) != 2):
    print("gen_smpl.py workflow")
    print("\tworkflow: lv, hs, gvpv")
    exit()

wf = sys.argv[1]

dir_name = "../plot/combine/"

if (wf == 'lv'):
    confn_cpnt1 = sp.lmp_confn
    confn_cpnt2 = sp.vr_confn
    confn = sp.lv_confn
    df_lmp = sp.df_lmp.copy()
    df_vr = sp.df_vr.copy()
    df_lv = sp.df_lv.copy()

    df_cpnt1 = df_lmp
    df_cpnt2 = df_vr
    df_wf = df_lv
    cpnt1 = 'lmp'
    cpnt2 = 'vr'
elif (wf == 'hs'):
    confn_cpnt1 = sp.ht_confn
    confn_cpnt2 = sp.sw_confn
    confn = sp.hs_confn
    df_ht = sp.df_ht.copy()
    df_sw = sp.df_sw.copy()
    df_hs = sp.df_hs.copy()

    df_cpnt1 = df_ht
    df_cpnt2 = df_sw
    df_wf = df_hs
    cpnt1 = 'ht'
    cpnt2 = 'sw'
elif (wf == 'gvpv'):
    confn_cpnt1 = sp.gs_confn
    confn_cpnt2 = sp.pdf_confn
    confn = sp.gvpv_confn
    df_gs = sp.df_gs.copy()
    df_pdf = sp.df_pdf.copy()
    df_gvpv = sp.df_gvpv.copy()

    df_cpnt1 = df_gs
    df_cpnt2 = df_pdf
    df_wf = df_gvpv
    cpnt1 = 'gs'
    cpnt2 = 'pdf'
else:
    exit()

df_wf = mdlr.df_intersection(df_wf, df_cpnt1, confn_cpnt1)
df_wf = mdlr.df_intersection(df_wf, df_cpnt2, confn_cpnt2)
df_cpnt1 = mdlr.df_intersection(df_cpnt1, df_wf, confn_cpnt1)
df_cpnt2 = mdlr.df_intersection(df_cpnt2, df_wf, confn_cpnt2)

df_wf = df_wf.merge(df_cpnt1[confn_cpnt1 + ['exec_time', 'comp_time']], \
        on=confn_cpnt1, suffixes=('', '_' + cpnt1))
df_wf = df_wf.merge(df_cpnt2[confn_cpnt2 + ['exec_time', 'comp_time']], \
        on=confn_cpnt2, suffixes=('', '_' + cpnt2))

exec_time_max = np.concatenate(([df_wf['exec_time_' + cpnt1].values], \
        [df_wf['exec_time_' + cpnt2].values]), axis=0).max(axis=0)
df_wf_exec = pd.DataFrame(np.c_[df_wf[confn].values, exec_time_max], \
        columns=confn + ['exec_time'])
df_recall = mdlr.eval_recall(df_wf_exec, df_wf, confn, 'exec_time', 25)
print("Recall score for max of execution times:")
print(df_recall)
sp.df2csv(df_recall, dir_name + "recall_" + wf + "_exec_max.csv")

comp_time_sum = df_wf['comp_time_' + cpnt1].values + df_wf['comp_time_' + cpnt2].values
df_wf_comp = pd.DataFrame(np.c_[df_wf[confn].values, comp_time_sum], \
        columns=confn + ['comp_time'])
df_recall = mdlr.eval_recall(df_wf_comp, df_wf, confn, 'comp_time', 25)
print("Recall score for sum of computer times:")
print(df_recall)
sp.df2csv(df_recall, dir_name + "recall_" + wf + "_comp_sum.csv")

for perfn in ['exec', 'comp']:
    for rand_seed in range(1, 101):
        df_wf = df_wf.sort_values(confn).reset_index(drop=True)
        df_wf = df_wf.sample(frac=1, random_state=rand_seed).reset_index(drop=True)
        df_wf = df_wf.sample(frac=1, random_state=rand_seed).reset_index(drop=True)
        df_wf = df_wf.sample(frac=1, random_state=rand_seed).reset_index(drop=True)
        
        df_recall = mdlr.eval_recall_rand(df_wf, confn, perfn+'_time')
        if (rand_seed == 1):
            recall_rnd = np.array([df_recall.values])
        else:
            recall_rnd = np.append(recall_rnd, [df_recall.values], axis=0)

    top_rs_df = pd.DataFrame(np.c_[np.mean(recall_rnd, axis=0)], \
            columns=['num_top', 'recall_score'])
    print("Recall score of random sampling for " + perfn + " time:")
    print(df_recall)
    sp.df2csv(df_recall, dir_name + 'recall_' + wf + "_" + perfn + '_rnd.csv')

