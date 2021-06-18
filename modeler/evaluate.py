import numpy as np
import pandas as pd
import sample as sp
import modeler as mdlr
import sys

if (len(sys.argv) != 5):
    print("evaluate.py workflow performance #sample #runs")
    print("\tworkflow: lv, hs, gvpv")
    print("\tperformance: exec_time, comp_time")
    print("\tnumber of samples: 25, 50, 100")
    print("\t#runs: 10, 100")
    exit()

wf = sys.argv[1]
perfn = sys.argv[2]
num_smpl = int(sys.argv[3])
num_runs = int(sys.argv[4])

dir_name = '../plot/' + wf + '/' + perfn + '/'

if (wf == 'lv'):
    mdl_cnpt1 = mdlr.train_mdl(sp.df_lmp, sp.lmp_confn, perfn)
    mdl_cnpt2 = mdlr.train_mdl(sp.df_vr, sp.vr_confn, perfn)
    cpnt_mdls = [mdl_cnpt1, mdl_cnpt2]
    cpnt_confns = (sp.lmp_confn, sp.vr_confn)
    confn = sp.lv_confn
    if (perfn == 'exec_time'):
        if (num_smpl == 50):
            geist_num_iter = 7
            geist_pct_rand = 0.25
            al_num_iter = 7
            al_pct_rand = 0.3
            alic_num_iter = 6
            alic_pct_rand = 0.05
            alic_pct_repl = 0.45
            ceal_num_iter = 6
            ceal_pct_rand = 0.05
            ceal_pct_repl = 0.45
            alph_num_iter = 7
            alph_pct_rand = 0.15
            alich_num_iter = 1
            alich_pct_rand = 0.15
            cealh_num_iter = 1
            cealh_pct_rand = 0.15
        else:    # 100 samples
            geist_num_iter = 6
            geist_pct_rand = 0.4
            al_num_iter = 7
            al_pct_rand = 0.4
            alic_num_iter = 7
            alic_pct_rand = 0.05
            alic_pct_repl = 0.8
            ceal_num_iter = 7
            ceal_pct_rand = 0.05
            ceal_pct_repl = 0.8
            alph_num_iter = 4
            alph_pct_rand = 0.25
            alich_num_iter = 2
            alich_pct_rand = 0.45
            cealh_num_iter = 2
            cealh_pct_rand = 0.45
    elif (perfn == 'comp_time'):
        if (num_smpl == 50):
            geist_num_iter = 9
            geist_pct_rand = 0.25
            al_num_iter = 5
            al_pct_rand = 0.55
            alic_num_iter = 6
            alic_pct_rand = 0.05
            alic_pct_repl = 0.5
            ceal_num_iter = 6
            ceal_pct_rand = 0.05
            ceal_pct_repl = 0.5
            alph_num_iter = 8
            alph_pct_rand = 0.5
            alich_num_iter = 9
            alich_pct_rand = 0.3
            cealh_num_iter = 9
            cealh_pct_rand = 0.3
        else:    # 25 samples
            geist_num_iter = 2
            geist_pct_rand = 0.05
            al_num_iter = 9
            al_pct_rand = 0.1
            alic_num_iter = 7
            alic_pct_rand = 0.1
            alic_pct_repl = 0.5
            ceal_num_iter = 7
            ceal_pct_rand = 0.1
            ceal_pct_repl = 0.5
            alph_num_iter = 9
            alph_pct_rand = 0.1
            alich_num_iter = 8
            alich_pct_rand = 0.15
            cealh_num_iter = 8
            cealh_pct_rand = 0.15
    else:
        print("Error: unknown performance metrics!")
        exit()
elif (wf == 'hs'):
    mdl_cnpt1 = mdlr.train_mdl(sp.df_ht, sp.ht_confn, perfn)
    mdl_cnpt2 = mdlr.train_mdl(sp.df_sw, sp.sw_confn, perfn)
    cpnt_mdls = [mdl_cnpt1, mdl_cnpt2]
    cpnt_confns = (sp.ht_confn, sp.sw_confn)
    confn = sp.hs_confn
    if (perfn == 'exec_time'):
        if (num_smpl == 50):
            geist_num_iter = 2
            geist_pct_rand = 0.25
            al_num_iter = 9
            al_pct_rand = 0.45
            alic_num_iter = 8
            alic_pct_rand = 0.15
            alic_pct_repl = 0.7
            ceal_num_iter = 8
            ceal_pct_rand = 0.15
            ceal_pct_repl = 0.7
            alph_num_iter = 8
            alph_pct_rand = 0.25
            alich_num_iter = 2
            alich_pct_rand = 0.3
            cealh_num_iter = 2
            cealh_pct_rand = 0.3
        else:    # 100 samples
            geist_num_iter = 5
            geist_pct_rand = 0.4
            al_num_iter = 5
            al_pct_rand = 0.35
            alic_num_iter = 10
            alic_pct_rand = 0.3
            alic_pct_repl = 0.25
            ceal_num_iter = 10
            ceal_pct_rand = 0.3
            ceal_pct_repl = 0.25
            alph_num_iter = 8
            alph_pct_rand = 0.3
            alich_num_iter = 3
            alich_pct_rand = 0.15
            cealh_num_iter = 3
            cealh_pct_rand = 0.15
    elif (perfn == 'comp_time'):
        if (num_smpl == 50):
            geist_num_iter = 4
            geist_pct_rand = 0.4
            al_num_iter = 9
            al_pct_rand = 0.35
            alic_num_iter = 10
            alic_pct_rand = 0.2
            alic_pct_repl = 0.55
            ceal_num_iter = 10
            ceal_pct_rand = 0.2
            ceal_pct_repl = 0.55
            alph_num_iter = 9
            alph_pct_rand = 0.35
            alich_num_iter = 1
            alich_pct_rand = 0.05
            cealh_num_iter = 1
            cealh_pct_rand = 0.05
        else:    # 25 samples
            geist_num_iter = 6
            geist_pct_rand = 0.05
            al_num_iter = 8
            al_pct_rand = 0.35
            alic_num_iter = 5
            alic_pct_rand = 0.2
            alic_pct_repl = 0.35
            ceal_num_iter = 5
            ceal_pct_rand = 0.2
            ceal_pct_repl = 0.35
            alph_num_iter = 5
            alph_pct_rand = 0.45
            alich_num_iter = 2
            alich_pct_rand = 0.05
            cealh_num_iter = 2
            cealh_pct_rand = 0.05
    else:
        print("Error: unknown performance metrics!")
        exit()
elif (wf == 'gvpv'):
    mdl_cnpt1 = mdlr.train_mdl(sp.df_gs, sp.gs_confn, perfn)
    mdl_cnpt2 = mdlr.train_mdl(sp.df_pdf, sp.pdf_confn, perfn)
    cpnt_mdls = [mdl_cnpt1, mdl_cnpt2]
    cpnt_confns = (sp.gs_confn, sp.pdf_confn)
    confn = sp.gvpv_confn
    if (perfn == 'comp_time'):
        if (num_smpl == 50):
            geist_num_iter = 6
            geist_pct_rand = 0.05
            al_num_iter = 7
            al_pct_rand = 0.15
            alic_num_iter = 7
            alic_pct_rand = 0.1
            alic_pct_repl = 0.1
            ceal_num_iter = 7
            ceal_pct_rand = 0.1
            ceal_pct_repl = 0.1
            alph_num_iter = 8
            alph_pct_rand = 0.4
            alich_num_iter = 9
            alich_pct_rand = 0.15
            cealh_num_iter = 9
            cealh_pct_rand = 0.15
        else:    # 25 samples
            geist_num_iter = 3
            geist_pct_rand = 0.1
            al_num_iter = 8
            al_pct_rand = 0.35
            alic_num_iter = 7
            alic_pct_rand = 0.15
            alic_pct_repl = 0.6
            ceal_num_iter = 7
            ceal_pct_rand = 0.15
            ceal_pct_repl = 0.6
            alph_num_iter = 7
            alph_pct_rand = 0.35
            alich_num_iter = 6
            alich_pct_rand = 0.1
            cealh_num_iter = 6
            cealh_pct_rand = 0.1
    else:
        print("Error: unknown performance metrics!")
        exit()
else:
    print("Error: unknown workflow!")
    exit()

for rand_seed in range(1, num_runs + 1):
    if (wf == 'lv'):
        df_cnpt1 = sp.df_lmp.sample(frac=1, random_state=rand_seed).reset_index(drop=True)
        df_cnpt2 = sp.df_vr.sample(frac=1, random_state=rand_seed).reset_index(drop=True)
        dfs_cpnt = (df_cnpt1, df_cnpt2)
        df_wf = sp.df_lv.sample(frac=1, random_state=rand_seed).reset_index(drop=True)
    elif (wf == 'hs'):
        df_cnpt1 = sp.df_ht.sample(frac=1, random_state=rand_seed).reset_index(drop=True)
        df_cnpt2 = sp.df_sw.sample(frac=1, random_state=rand_seed).reset_index(drop=True)
        dfs_cpnt = (df_cnpt1, df_cnpt2)
        df_wf = sp.df_hs.sample(frac=1, random_state=rand_seed).reset_index(drop=True)
    elif (wf == 'gvpv'):
        df_cnpt1 = sp.df_gs.sample(frac=1, random_state=rand_seed).reset_index(drop=True)
        df_cnpt2 = sp.df_pdf.sample(frac=1, random_state=rand_seed).reset_index(drop=True)
        dfs_cpnt = (df_cnpt1, df_cnpt2)
        df_wf = sp.df_gvpv.sample(frac=1, random_state=rand_seed).reset_index(drop=True)
    else:
        print("Error: unknown workflow!")
        exit()

    # Random sampling
    rslt = mdlr.rs(df_wf, confn, perfn, num_smpl)
    top_perf, df_recall, df_mape, comp_time = rslt[0], rslt[1], rslt[2], rslt[3]
    if (rand_seed == 1):
        rs_top_perf = np.array([top_perf])
        rs_recall = np.array([df_recall.values])
        rs_mape = np.array([df_mape.values])
        rs_comp_time = np.array([comp_time])
    else:
        rs_top_perf = np.append(rs_top_perf, [top_perf], axis=0)
        rs_recall = np.append(rs_recall, [df_recall.values], axis=0)
        rs_mape = np.append(rs_mape, [df_mape.values], axis=0)
        rs_comp_time = np.append(rs_comp_time, [comp_time], axis=0)

    # Active learning
    rslt = mdlr.al(df_wf, confn, perfn, num_smpl, al_pct_rand, al_num_iter)
    top_perf, df_recall, df_mape, comp_time = rslt[0], rslt[1], rslt[2], rslt[3]
    if (rand_seed == 1):
        al_top_perf = np.array([top_perf])
        al_recall = np.array([df_recall.values])
        al_mape = np.array([df_mape.values])
        al_comp_time = np.array([comp_time])
    else:
        al_top_perf = np.append(al_top_perf, [top_perf], axis=0)
        al_recall = np.append(al_recall, [df_recall.values], axis=0)
        al_mape = np.append(al_mape, [df_mape.values], axis=0)
        al_comp_time = np.append(al_comp_time, [comp_time], axis=0)
    
    # ALIC
    rslt = mdlr.alic([None, None], df_wf, cpnt_confns, confn, perfn, num_smpl, \
            alic_pct_rand, alic_num_iter, alic_pct_repl, dfs_cpnt)
    top_perf, df_recall, df_mape, comp_time = rslt[0], rslt[1], rslt[2], rslt[3]
    if (rand_seed == 1):
        alic_top_perf = np.array([top_perf])
        alic_recall = np.array([df_recall.values])
        alic_mape = np.array([df_mape.values])
        alic_comp_time = np.array([comp_time])
    else:
        alic_top_perf = np.append(alic_top_perf, [top_perf], axis=0)
        alic_recall = np.append(alic_recall, [df_recall.values], axis=0)
        alic_mape = np.append(alic_mape, [df_mape.values], axis=0)
        alic_comp_time = np.append(alic_comp_time, [comp_time], axis=0)

    # CEAL
    rslt = mdlr.ceal([None, None], df_wf, cpnt_confns, confn, perfn, num_smpl, \
            ceal_pct_rand, ceal_num_iter, ceal_pct_repl, dfs_cpnt)
    top_perf, df_recall, df_mape, comp_time = rslt[0], rslt[1], rslt[2], rslt[3]
    if (rand_seed == 1):
        ceal_top_perf = np.array([top_perf])
        ceal_recall = np.array([df_recall.values])
        ceal_mape = np.array([df_mape.values])
        ceal_comp_time = np.array([comp_time])
    else:
        ceal_top_perf = np.append(ceal_top_perf, [top_perf], axis=0)
        ceal_recall = np.append(ceal_recall, [df_recall.values], axis=0)
        ceal_mape = np.append(ceal_mape, [df_mape.values], axis=0)
        ceal_comp_time = np.append(ceal_comp_time, [comp_time], axis=0)

    # ALpH
    rslt = mdlr.alph(cpnt_mdls, df_wf, cpnt_confns, confn, perfn, num_smpl, \
            alph_pct_rand, alph_num_iter)
    top_perf, df_recall, df_mape, comp_time = rslt[0], rslt[1], rslt[2], rslt[3]
    if (rand_seed == 1):
        alph_top_perf = np.array([top_perf])
        alph_recall = np.array([df_recall.values])
        alph_mape = np.array([df_mape.values])
        alph_comp_time = np.array([comp_time])
    else:
        alph_top_perf = np.append(alph_top_perf, [top_perf], axis=0)
        alph_recall = np.append(alph_recall, [df_recall.values], axis=0)
        alph_mape = np.append(alph_mape, [df_mape.values], axis=0)
        alph_comp_time = np.append(alph_comp_time, [comp_time], axis=0)

    # ALIC-H
    rslt = mdlr.alic(cpnt_mdls, df_wf, cpnt_confns, confn, perfn, num_smpl, \
            alich_pct_rand, alich_num_iter)
    top_perf, df_recall, df_mape, comp_time = rslt[0], rslt[1], rslt[2], rslt[3]
    if (rand_seed == 1):
        alich_top_perf = np.array([top_perf])
        alich_recall = np.array([df_recall.values])
        alich_mape = np.array([df_mape.values])
        alich_comp_time = np.array([comp_time])
    else:
        alich_top_perf = np.append(alich_top_perf, [top_perf], axis=0)
        alich_recall = np.append(alich_recall, [df_recall.values], axis=0)
        alich_mape = np.append(alich_mape, [df_mape.values], axis=0)
        alich_comp_time = np.append(alich_comp_time, [comp_time], axis=0)
   
    # CEAL-H
    rslt = mdlr.ceal(cpnt_mdls, df_wf, cpnt_confns, confn, perfn, num_smpl, \
            cealh_pct_rand, cealh_num_iter)
    top_perf, df_recall, df_mape, comp_time = rslt[0], rslt[1], rslt[2], rslt[3]
    if (rand_seed == 1):
        cealh_top_perf = np.array([top_perf])
        cealh_recall = np.array([df_recall.values])
        cealh_mape = np.array([df_mape.values])
        cealh_comp_time = np.array([comp_time])
    else:
        cealh_top_perf = np.append(cealh_top_perf, [top_perf], axis=0)
        cealh_recall = np.append(cealh_recall, [df_recall.values], axis=0)
        cealh_mape = np.append(cealh_mape, [df_mape.values], axis=0)
        cealh_comp_time = np.append(cealh_comp_time, [comp_time], axis=0)

    '''
    # GEIST
    rslt = mdlr.geist(df_wf, confn, perfn, num_smpl, geist_pct_rand, geist_num_iter)
    top_perf, df_recall, df_mape, comp_time = rslt[0], rslt[1], rslt[2], rslt[3]
    if (rand_seed == 1):
        geist_top_perf = np.array([top_perf])
        geist_recall = np.array([df_recall.values])
        geist_mape = np.array([df_mape.values])
        geist_comp_time = np.array([comp_time])
    else:
        geist_top_perf = np.append(geist_top_perf, [top_perf], axis=0)
        geist_recall = np.append(geist_recall, [df_recall.values], axis=0)
        geist_mape = np.append(geist_mape, [df_mape.values], axis=0)
        geist_comp_time = np.append(geist_comp_time, [comp_time], axis=0)
    '''

colns = ['RS', 'AL', 'ALIC', 'CEAL', 'ALpH', 'ALICH', 'CEALH']#, 'GEIST']
print("Top performance ({perfn}):")
top_perf = np.c_[np.mean(rs_top_perf, axis=0), \
                 np.mean(al_top_perf, axis=0), \
                 np.mean(alic_top_perf, axis=0), \
                 np.mean(ceal_top_perf, axis=0), \
                 np.mean(alph_top_perf, axis=0), \
                 np.mean(alich_top_perf, axis=0), \
                 np.mean(cealh_top_perf, axis=0) \
#                 np.mean(geist_top_perf, axis=0) \
                ]
df_top_perf = pd.DataFrame(top_perf, columns=colns).round(4)
print(df_top_perf)
sp.df2csv(df_top_perf, dir_name + 'top_perf_' + str(num_smpl) + '.csv')

print("MAPE (%):")
mape_avg = np.c_[np.mean(rs_mape, axis=0), \
                 np.mean(al_mape, axis=0)[:, -1], \
                 np.mean(alic_mape, axis=0)[:, -1], \
                 np.mean(ceal_mape, axis=0)[:, -1], \
                 np.mean(alph_mape, axis=0)[:, -1], \
                 np.mean(alich_mape, axis=0)[:, -1], \
                 np.mean(cealh_mape, axis=0)[:, -1] \
#                 np.mean(geist_mape, axis=0)[:, -1] \
                ]
df_mapes = pd.DataFrame(mape_avg, columns=['pct_top']+colns).round(4)
print(df_mapes)
sp.df2csv(df_mapes, dir_name + 'mape_' + str(num_smpl) + '.csv')

print("Recall Score (%):")
recall_avg = np.c_[np.mean(rs_recall, axis=0), \
                   np.mean(al_recall, axis=0)[:, -1], \
                   np.mean(alic_recall, axis=0)[:, -1], \
                   np.mean(ceal_recall, axis=0)[:, -1], \
                   np.mean(alph_recall, axis=0)[:, -1], \
                   np.mean(alich_recall, axis=0)[:, -1], \
                   np.mean(cealh_recall, axis=0)[:, -1] \
#                   np.mean(geist_recall, axis=0)[:, -1] \
                  ]
df_recall = pd.DataFrame(recall_avg, columns=['pct_top', 'num_top']+colns).round(4)
print(df_recall)
sp.df2csv(df_recall, dir_name + 'recall_' + str(num_smpl) + '.csv')


print("Cost [Computer Time (core-hours)]:")
comp_time = np.c_[np.mean(rs_comp_time, axis=0), \
                  np.mean(al_comp_time, axis=0), \
                  np.mean(alic_comp_time, axis=0), \
                  np.mean(ceal_comp_time, axis=0), \
                  np.mean(alph_comp_time, axis=0), \
                  np.mean(alich_comp_time, axis=0), \
                  np.mean(cealh_comp_time, axis=0) \
#                  np.mean(geist_comp_time, axis=0) \
                 ]
df_comp_time = pd.DataFrame(comp_time, columns=colns).round(4)
print(df_comp_time)
sp.df2csv(df_comp_time, dir_name + 'comp_time_' + str(num_smpl) + '.csv')

