import numpy as np
import pandas as pd
import sample as sp
import modeler as mdlr
import sys

if (len(sys.argv) != 6):
    print("pct_rand.py workflow performance #sample #runs algorithm")
    print("\tworkflow: lv, hs, gvpv")
    print("\tperformance: exec_time, comp_time")
    print("\tnumber of samples: 25, 50, 100")
    print("\t#runs: 10, 100")
    print("\talgorithm: al, geist, alic, alph, alich")
    exit()

wf = sys.argv[1]
perfn = sys.argv[2]
num_smpl = int(sys.argv[3])
num_run = int(sys.argv[4])
algo = sys.argv[5]

dir_name = 'plot/pct_rand/' + wf + '_' + perfn + '/'

pct_repl = 0.0

if (wf == 'lv'):
    mdl_cnpt1 = mdlr.train_mdl(sp.df_lmp, sp.lmp_confn, perfn)
    mdl_cnpt2 = mdlr.train_mdl(sp.df_vr, sp.vr_confn, perfn)
    cpnt_mdls = [mdl_cnpt1, mdl_cnpt2]
    cpnt_confns = (sp.lmp_confn, sp.vr_confn)
    confn = sp.lv_confn
    if (perfn == 'exec_time'):
        if (num_smpl == 50):
            if (algo == 'geist'):
                num_iter = 7
            elif (algo == 'al'):
                num_iter = 7
            elif (algo == 'alic'):
                num_iter = 6
                pct_repl = 0.45
            elif (algo == 'alph'):
                num_iter = 7
            elif (algo == 'alich'):
                num_iter = 1
            else:
                print("Error: unknown algorithm!")
                exit()
        else:    # 100 samples
            if (algo == 'geist'):
                num_iter = 6
            elif (algo == 'al'):
                num_iter = 7
            elif (algo == 'alic'):
                num_iter = 7
                pct_repl = 0.8
            elif (algo == 'alph'):
                num_iter = 4
            elif (algo == 'alich'):
                num_iter = 2
            else:
                print("Error: unknown algorithm!")
                exit()
    elif (perfn == 'comp_time'):
        if (num_smpl == 50):
            if (algo == 'geist'):
                num_iter = 9
            elif (algo == 'al'):
                num_iter = 5
            elif (algo == 'alic'):
                num_iter = 6
                pct_repl = 0.5
            elif (algo == 'alph'):
                num_iter = 8
            elif (algo == 'alich'):
                num_iter = 9
            else:
                print("Error: unknown algorithm!")
                exit()
        else:    # 25 samples
            if (algo == 'geist'):
                num_iter = 2
            elif (algo == 'al'):
                num_iter = 9
            elif (algo == 'alic'):
                num_iter = 7
                pct_repl = 0.5
            elif (algo == 'alph'):
                num_iter = 9
            elif (algo == 'alich'):
                num_iter = 8
            else:
                print("Error: unknown algorithm!")
                exit()
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
            if (algo == 'geist'):
                num_iter = 2
            elif (algo == 'al'):
                num_iter = 9
            elif (algo == 'alic'):
                num_iter = 8
                pct_repl = 0.7
            elif (algo == 'alph'):
                num_iter = 8
            elif (algo == 'alich'):
                num_iter = 2
            else:
                print("Error: unknown algorithm!")
                exit()
        else:    # 100 samples
            if (algo == 'geist'):
                num_iter = 5
            elif (algo == 'al'):
                num_iter = 5
            elif (algo == 'alic'):
                num_iter = 10
                pct_repl = 0.25
            elif (algo == 'alph'):
                num_iter = 8
            elif (algo == 'alich'):
                num_iter = 3
            else:
                print("Error: unknown algorithm!")
                exit()
    elif (perfn == 'comp_time'):
        if (num_smpl == 50):
            if (algo == 'geist'):
                num_iter = 4
            elif (algo == 'al'):
                num_iter = 9
            elif (algo == 'alic'):
                num_iter = 10
                pct_repl = 0.55
            elif (algo == 'alph'):
                num_iter = 9
            elif (algo == 'alich'):
                num_iter = 1
            else:
                print("Error: unknown algorithm!")
                exit()
        else:    # 25 samples
            if (algo == 'geist'):
                num_iter = 6
            elif (algo == 'al'):
                num_iter = 8
            elif (algo == 'alic'):
                num_iter = 5
                pct_repl = 0.35
            elif (algo == 'alph'):
                num_iter = 5
            elif (algo == 'alich'):
                num_iter = 2
            else:
                print("Error: unknown algorithm!")
                exit()
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
            if (algo == 'geist'):
                num_iter = 6
            elif (algo == 'al'):
                num_iter = 7
            elif (algo == 'alic'):
                num_iter = 7
                pct_repl = 0.1
            elif (algo == 'alph'):
                num_iter = 8
            elif (algo == 'alich'):
                num_iter = 9
            else:
                print("Error: unknown algorithm!")
                exit()
        else:    # 25 samples
            if (algo == 'geist'):
                num_iter = 3
            elif (algo == 'al'):
                num_iter = 8
            elif (algo == 'alic'):
                num_iter = 7
                pct_repl = 0.6
            elif (algo == 'alph'):
                num_iter = 7
            elif (algo == 'alich'):
                num_iter = 6
            else:
                print("Error: unknown algorithm!")
                exit()
    else:
        print("Error: unknown performance metrics!")
        exit()
else:
    print("Error: unknown workflow!")
    exit()

pct_rand_start = 0.05
pct_rand_end = 0.95 - pct_repl
pct_rand_step = 0.05

rand_seed_start = 1
rand_seed_end = num_run + 1
rand_seed_step = 1
for rand_seed in range(rand_seed_start, rand_seed_end, rand_seed_step):
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

    for pct_rand in np.arange(pct_rand_start, pct_rand_end, pct_rand_step):
        if (algo == 'geist'):
            rslt = mdlr.geist(df_wf, confn, perfn, num_smpl, pct_rand, num_iter)
        elif (algo == 'al'):
            rslt = mdlr.al(df_wf, confn, perfn, num_smpl, pct_rand, num_iter)
        elif (algo == 'alic'):
            rslt = mdlr.alic([None, None], df_wf, cpnt_confns, confn, perfn, num_smpl, \
                    pct_rand, num_iter, pct_repl, dfs_cpnt)
        elif (algo == 'alich'):
            rslt = mdlr.alic(cpnt_mdls, df_wf, cpnt_confns, confn, perfn, num_smpl, \
                    pct_rand, num_iter)
        elif (algo == 'alph'):
            rslt = mdlr.alph(cpnt_mdls, df_wf, cpnt_confns, confn, perfn, num_smpl, \
                    pct_rand, num_iter)
        else:
            print("Error: unknown algorithms!")
            exit()

        top_perf, df_recall, df_mape = rslt[0], rslt[1], rslt[2]
        if (pct_rand == pct_rand_start):
            top_perfs = np.array([top_perf])
            recalls = np.array([df_recall['recall_score'].values])
            mapes = np.array([df_mape['MAPE'].values])
        else:
            top_perfs = np.append(top_perfs, [top_perf], axis=0)
            recalls = np.append(recalls, [df_recall['recall_score'].values], axis=0)
            mapes = np.append(mapes, [df_mape['MAPE'].values], axis=0)

    if (rand_seed == rand_seed_start):
        top_perfs_all = np.array([top_perfs])
        recalls_all = np.array([recalls])
        mapes_all = np.array([mapes])
    else:
        top_perfs_all = np.append(top_perfs_all, [top_perfs], axis=0)
        recalls_all = np.append(recalls_all, [recalls], axis=0)
        mapes_all = np.append(mapes_all, [mapes], axis=0)


print("For different percentages of random samples:")
colns = list(map(str, np.arange(pct_rand_start, pct_rand_end, pct_rand_step).round(4)))

print(f"Top performance ({perfn}):")
top_perfs_avg = np.sum(top_perfs_all, axis=0) / len(top_perfs_all)
df_top_perf = pd.DataFrame([top_perfs_avg], columns=colns)
df_top_perf = df_top_perf.round(4)
print(df_top_perf)
sp.df2csv(df_top_perf, dir_name + algo + '_top_perf_' + str(num_smpl) + '.csv')

print("Recall score:")
recalls_avg = np.sum(recalls_all, axis=0) / len(recalls_all)
df_recall = pd.DataFrame(np.c_[df_recall[['pct_top', 'num_top']].values, \
        np.transpose(recalls_avg)], columns=['pct_top', 'num_top']+colns)
df_recall = df_recall.round(4)
print(df_recall)
sp.df2csv(df_recall, dir_name + algo + '_recall_' + str(num_smpl) + '.csv')

print("MAPE:")
mapes_avg = np.sum(mapes_all, axis=0) / len(mapes_all)
df_mape = pd.DataFrame(np.c_[df_mape['pct_top'].values, \
        np.transpose(mapes_avg)], columns=['pct_top']+colns)
df_mape = df_mape.round(4)
print(df_mape)
sp.df2csv(df_mape, dir_name + algo + '_mape_' + str(num_smpl) + '.csv')
