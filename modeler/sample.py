import numpy as np
import pandas as pd
import glob

num_core = 36

lmp_confn = ['lmp_nproc', 'lmp_ppn', 'lmp_tpp']
vr_confn = ['vr_nproc', 'vr_ppn', 'vr_tpp']
lmp_inn = ['lmp_nstep_out', 'lmp_l2s', 'lmp_sld']
lv_confn = lmp_confn + vr_confn
lmp_paramns = lmp_confn + lmp_inn
vr_paramns = vr_confn + lmp_inn
lv_paramns = lv_confn + lmp_inn

ht_confn = ['ht_x_nproc', 'ht_y_nproc', 'ht_ppn', 'ht_bufsize', 'ht_nout']
sw_confn = ['sw_nproc', 'sw_ppn', 'ht_nout']
ht_inn = ['ht_x', 'ht_y', 'ht_iter']
hs_confn = ['ht_x_nproc', 'ht_y_nproc', 'ht_ppn', 'ht_bufsize', 'sw_nproc', 'sw_ppn', 'ht_nout']
#ht_confn = ['ht_x_nproc', 'ht_y_nproc', 'ht_ppn', 'ht_bufsize']
#sw_confn = ['sw_nproc', 'sw_ppn']
#ht_inn = ['ht_nout', 'ht_x', 'ht_y', 'ht_iter']
#hs_confn = ht_confn + sw_confn
ht_paramns = ht_confn + ht_inn
sw_paramns = sw_confn + ht_inn
hs_paramns = hs_confn + ht_inn

gs_confn = ['gs_nproc', 'gs_ppn']
pdf_confn = ['pdf_nproc', 'pdf_ppn']
gplot_confn = ['gplot_nproc']
pplot_confn = ['pplot_nproc']
gs_inn = ['gs_cs', 'gs_step']
gp_confn = gs_confn + pdf_confn
gvpv_confn = gp_confn + pplot_confn + gplot_confn
gs_paramns = gs_confn + gs_inn
pdf_paramns = pdf_confn + gs_inn
gplot_paramns = gplot_confn + gs_inn
pplot_paramns = pplot_confn + gs_inn
gp_paramns = gp_confn + gs_inn
gvpv_paramns = gvpv_confn + gs_inn


def df2csv(df, filename):
    f = open(filename, "w")
    f.write(df.to_csv(sep='\t', header=False, index=False))
    f.close()


def csv2df(filenames, paramns, perfn='', cols=[], vals=[]):
    if (perfn == ''):
        colns = paramns
    else:
        colns = paramns + [perfn]
    data = []
    for filename in filenames:
        for line in open(filename):
            data.append([float(s) for s in line.split()[:len(colns)]] + vals)
    return pd.DataFrame(data, columns=colns+cols)


def lbl_df_runnable(df_smpl, colns, perfn='exec_time'):
    runnable = np.ones(df_smpl.shape[0]).astype(int)
    for i in range(df_smpl.shape[0]):
        if (df_smpl[perfn].values[i] == float('inf')):
            runnable[i] = 0
    rem_colns = [coln for coln in df_smpl.columns.tolist() if coln not in colns]
    df_lbl = pd.DataFrame(np.c_[df_smpl[colns].values, runnable, df_smpl[rem_colns].values], \
                          columns=colns + ['runnable'] + rem_colns)
    return df_lbl


def get_vld_df(df_smpl):
    return df_smpl[df_smpl.runnable == 1]


def get_name(df_smpl):
    if (all([x in df_smpl.columns.tolist() for x in lv_confn])):
        return 'lv'
    elif (all([x in df_smpl.columns.tolist() for x in lmp_confn])):
        return 'lmp'
    elif (all([x in df_smpl.columns.tolist() for x in vr_confn])):
        return 'vr'
    elif (all([x in df_smpl.columns.tolist() for x in hs_confn])):
        return 'hs'
    elif (all([x in df_smpl.columns.tolist() for x in ht_confn])):
        return 'ht'
    elif (all([x in df_smpl.columns.tolist() for x in sw_confn])):
        return 'sw'
    elif (all([x in df_smpl.columns.tolist() for x in gvpv_confn])):
        return 'gvpv'
    elif (all([x in df_smpl.columns.tolist() for x in gp_confn])):
        return 'gp'
    elif (all([x in df_smpl.columns.tolist() for x in gs_confn])):
        return 'gs'
    elif (all([x in df_smpl.columns.tolist() for x in pdf_confn])):
        return 'pdf'
    elif (all([x in df_smpl.columns.tolist() for x in gplot_confn])):
        return 'gplot'
    elif (all([x in df_smpl.columns.tolist() for x in pplot_confn])):
        return 'pplot'
    else:
        return 'unknown'


def get_comp_time(nproc, ppn, runtime):
    nnode = np.ceil(np.divide(nproc, ppn))
    return np.multiply(nnode, runtime) * num_core / 3600


def exec2comp_df(df_exec, exec_alias='exec_time', comp_alias='comp_time'):
    if (comp_alias in df_exec.columns.tolist()):
        return df_exec

    if (exec_alias not in df_exec.columns.tolist()):
        print("There is not exec_time!")
        return df_exec

    name = get_name(df_exec)
    if (name != 'lmp' and name != 'vr' and name != 'lv' \
        and name != 'ht' and name != 'sw' and name != 'hs' \
        and name != 'gs' and name != 'pdf' and name != 'gp' \
        and name != 'gvpv' and name != 'gplot' and name != 'pplot' \
       ):
        print("Error: unknown dataframe!")
        return df_exec

    runtime = df_exec[exec_alias].values
    if (name == 'lmp' or name == 'vr' or name == 'ht' or name == 'sw' \
        or name == 'gs' or name == 'pdf' \
       ):
        if (name == 'ht'):
            nproc = df_exec['ht_x_nproc'].values * df_exec['ht_y_nproc'].values
        else:
            nproc = df_exec[name + '_nproc'].values
        ppn = df_exec[name + '_ppn'].values
        comp_time = get_comp_time(nproc, ppn, runtime)
    elif (name == 'gplot' or name == 'pplot'):
        comp_time = runtime * num_core / 3600
    else:
        if (name == 'lv'):
            nproc1 = df_exec['lmp_nproc'].values
            ppn1 = df_exec['lmp_ppn'].values
            nproc2 = df_exec['vr_nproc'].values
            ppn2 = df_exec['vr_ppn'].values
            comp_time = get_comp_time(nproc1, ppn1, runtime) + get_comp_time(nproc2, ppn2, runtime)
        elif (name == 'hs'):
            nproc1 = df_exec['ht_x_nproc'].values * df_exec['ht_y_nproc'].values
            ppn1 = df_exec['ht_ppn'].values
            nproc2 = df_exec['sw_nproc'].values
            ppn2 = df_exec['sw_ppn'].values
            comp_time = get_comp_time(nproc1, ppn1, runtime) + get_comp_time(nproc2, ppn2, runtime)
        elif (name == 'gp' or name == 'gvpv'):
            nproc1 = df_exec['gs_nproc'].values
            ppn1 = df_exec['gs_ppn'].values
            nproc2 = df_exec['pdf_nproc'].values
            ppn2 = df_exec['pdf_ppn'].values
            comp_time = get_comp_time(nproc1, ppn1, runtime) + get_comp_time(nproc2, ppn2, runtime)
            if (name == 'gvpv'):
                comp_time = comp_time + 2 * runtime * num_core / 3600

    df_comp = pd.DataFrame(np.c_[df_exec.values, comp_time], columns=df_exec.columns.tolist() + [comp_alias])
    return df_comp


df_lmp = csv2df(glob.glob('../data/lv/lmp*.csv'), lmp_paramns, 'exec_time')
df_lmp = get_vld_df(exec2comp_df(lbl_df_runnable(df_lmp, lmp_paramns)))
df_lmp = df_lmp[lmp_paramns + ['exec_time', 'comp_time']]
df_lmp = df_lmp.sort_values(lmp_inn + lmp_confn).reset_index(drop=True)

df_vr = csv2df(glob.glob('../data/lv/vr*.csv'), vr_paramns, 'exec_time')
df_vr = get_vld_df(exec2comp_df(lbl_df_runnable(df_vr, vr_paramns)))
df_vr = df_vr[vr_paramns + ['exec_time', 'comp_time']]
df_vr = df_vr.sort_values(lmp_inn + vr_confn).reset_index(drop=True)

df_lv = csv2df(glob.glob('../data/lv/lv*.csv'), lv_paramns, 'exec_time')
df_lv = get_vld_df(exec2comp_df(lbl_df_runnable(df_lv, lv_paramns)))
df_lv = df_lv[lv_paramns + ['exec_time', 'comp_time']]
df_lv = df_lv.sort_values(lmp_inn + lv_confn).reset_index(drop=True)


df_ht = csv2df(glob.glob('../data/hs/ht*.csv'), ht_paramns, 'exec_time')
df_ht = get_vld_df(exec2comp_df(lbl_df_runnable(df_ht, ht_paramns)))
df_ht = df_ht[ht_paramns + ['exec_time', 'comp_time']]
df_ht = df_ht.sort_values(ht_inn + ht_confn).reset_index(drop=True)

df_sw = csv2df(glob.glob('../data/hs/sw*.csv'), sw_paramns, 'exec_time')
df_sw = get_vld_df(exec2comp_df(lbl_df_runnable(df_sw, sw_paramns)))
df_sw = df_sw[sw_paramns + ['exec_time', 'comp_time']]
df_sw = df_sw.sort_values(ht_inn + sw_confn).reset_index(drop=True)

df_hs = csv2df(glob.glob('../data/hs/hs*.csv'), hs_paramns, 'exec_time')
df_hs = get_vld_df(exec2comp_df(lbl_df_runnable(df_hs, hs_paramns)))
df_hs = df_hs[hs_paramns + ['exec_time', 'comp_time']]
df_hs = df_hs.sort_values(ht_inn + hs_confn).reset_index(drop=True)


df_gs = csv2df(glob.glob('../data/gp/gs*.csv'), gs_paramns, 'exec_time')
df_gs = get_vld_df(exec2comp_df(lbl_df_runnable(df_gs, gs_paramns)))
df_gs = df_gs[gs_paramns + ['exec_time', 'comp_time']]
df_gs = df_gs.sort_values(gs_inn + gs_confn).reset_index(drop=True)

df_pdf = csv2df(glob.glob('../data/gp/pdf*.csv'), pdf_paramns, 'exec_time')
df_pdf = get_vld_df(exec2comp_df(lbl_df_runnable(df_pdf, pdf_paramns)))
df_pdf = df_pdf[pdf_paramns + ['exec_time', 'comp_time']]
df_pdf = df_pdf.sort_values(gs_inn + pdf_confn).reset_index(drop=True)

df_gplot = csv2df(glob.glob('../data/gp/gplot*.csv'), gs_inn, 'exec_time', \
        gplot_confn, [1])
df_gplot = get_vld_df(exec2comp_df(lbl_df_runnable(df_gplot, gplot_paramns)))
df_gplot = df_gplot[gplot_paramns + ['exec_time', 'comp_time']]
df_gplot = df_gplot.sort_values(gs_inn + gplot_confn).reset_index(drop=True)

df_pplot = csv2df(glob.glob('../data/gp/pplot*.csv'), gs_inn, 'exec_time', \
        pplot_confn, [1])
df_pplot = get_vld_df(exec2comp_df(lbl_df_runnable(df_pplot, pplot_paramns)))
df_pplot = df_pplot[pplot_paramns + ['exec_time', 'comp_time']]
df_pplot = df_pplot.sort_values(gs_inn + pplot_confn).reset_index(drop=True)

df_gp = csv2df(glob.glob('../data/gp/gp*.csv'), gp_paramns, 'exec_time')
df_gp = get_vld_df(exec2comp_df(lbl_df_runnable(df_gp, gp_paramns)))
df_gp = df_gp[gp_paramns + ['exec_time', 'comp_time']]
df_gp = df_gp.sort_values(gs_inn + gp_confn).reset_index(drop=True)

df_gvpv = csv2df(glob.glob('../data/gp/gvpv*.csv'), gp_paramns, 'exec_time', \
        ['pplot_nproc', 'gplot_nproc'], [1, 1])
df_gvpv = get_vld_df(exec2comp_df(lbl_df_runnable(df_gvpv, gvpv_paramns)))
df_gvpv = df_gvpv[gvpv_paramns + ['exec_time', 'comp_time']]
df_gvpv = df_gvpv.sort_values(gs_inn + gvpv_confn).reset_index(drop=True)

