import numpy as np
import pandas as pd
import sample as sp
import modeler as mdlr

dir_name = "../plot/combine/"

df_lmp = sp.df_lmp.copy()
df_vr = sp.df_vr.copy()
df_lv = sp.df_lv.copy()

df_lmp = df_lmp[df_lmp.lmp_nstep_out == 200]
df_lmp = df_lmp[df_lmp.lmp_l2s == 16000]
df_lmp = df_lmp[df_lmp.lmp_sld == 20000]
df_vr = df_vr[df_vr.lmp_nstep_out == 200]
df_vr = df_vr[df_vr.lmp_l2s == 16000]
df_vr = df_vr[df_vr.lmp_sld == 20000]
df_lv = df_lv[df_lv.lmp_nstep_out == 200]
df_lv = df_lv[df_lv.lmp_l2s == 16000]
df_lv = df_lv[df_lv.lmp_sld == 20000]

df_lv = mdlr.df_intersection(df_lv, df_lmp, sp.lmp_confn)
df_lv = mdlr.df_intersection(df_lv, df_vr, sp.vr_confn)
df_lmp = mdlr.df_intersection(df_lmp, df_lv, sp.lmp_confn)
df_vr = mdlr.df_intersection(df_vr, df_lv, sp.vr_confn)

df_lv = df_lv.merge(df_lmp[sp.lmp_confn + ['exec_time', 'comp_time']], \
        on=sp.lmp_confn, suffixes=('', '_lmp'))
df_lv = df_lv.merge(df_vr[sp.vr_confn + ['exec_time', 'comp_time']], \
        on=sp.vr_confn, suffixes=('', '_vr'))

exec_time_max = np.concatenate(([df_lv['exec_time_lmp'].values], \
        [df_lv['exec_time_vr'].values]), axis=0).max(axis=0)
df_lv_exec = pd.DataFrame(np.c_[df_lv[sp.lv_confn].values, exec_time_max], \
        columns=sp.lv_confn + ['exec_time'])
df_recall = mdlr.eval_recall(df_lv_exec, df_lv, sp.lv_confn, 'exec_time', 25)
print("Recall score for max of execution times:")
print(df_recall)
df2csv(df_recall, dir_name + "recall_exec_max.csv")

comp_time_sum = df_lv['comp_time_lmp'].values + df_lv['comp_time_vr'].values
df_lv_comp = pd.DataFrame(np.c_[df_lv[sp.lv_confn].values, comp_time_sum], \
        columns=sp.lv_confn + ['comp_time'])
df_recall = mdlr.eval_recall(df_lv_comp, df_lv, sp.lv_confn, 'comp_time', 25)
print("Recall score for sum of computer times:")
print(df_recall)
df2csv(df_recall, dir_name + "recall_comp_sum.csv")

for perfn in ['exec', 'comp']:
    for rand_seed in range(1, 101):
        df_lv = df_lv.sort_values(sp.lv_confn).reset_index(drop=True)
        df_lv = df_lv.sample(frac=1, random_state=rand_seed).reset_index(drop=True)
        df_lv = df_lv.sample(frac=1, random_state=rand_seed).reset_index(drop=True)
        df_lv = df_lv.sample(frac=1, random_state=rand_seed).reset_index(drop=True)
        
        df_recall = mdlr.eval_recall2(df_lv, sp.lv_confn, perfn+'_time')
        if (rand_seed == 1):
            recall_rand = np.array([df_recall.values])
        else:
            recall_rand = np.append(recall_rand, [df_recall.values], axis=0)

    top_rs_df = pd.DataFrame(np.c_[np.mean(recall_rand, axis=0)], \
            columns=['num_top', 'recall_score'])
    print("Recall score of random sampling for " + perfn + " time:")
    print(df_recall)
    df2csv(df_recall, dir_name + 'recall_' + perfn + '_rand.csv')

