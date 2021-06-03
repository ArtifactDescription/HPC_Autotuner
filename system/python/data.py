import glob
import math
import random
import numpy as np
import pandas as pd

rand_seed = 1983
num_core = 36
num_node = 32

lmp_in_params = [16000, 20000]
lmp_conf_colns = ['lmp_nproc', 'lmp_ppw', 'lmp_nthread', 'lmp_io_step']
vr_conf_colns = ['vr_nproc', 'vr_ppw', 'vr_nthread', 'lmp_io_step']
lv_conf_colns = ['lmp_nproc', 'lmp_ppw', 'lmp_nthread', 'lmp_io_step', 'vr_nproc', 'vr_ppw', 'vr_nthread']
lv_in_conf_colns = ['lmp_l2s', 'lmp_sld', 'lmp_nproc', 'lmp_ppw', 'lmp_nthread', 'lmp_io_step', \
                    'vr_nproc', 'vr_ppw', 'vr_nthread']

ht_in_params = [2048, 2048, 1024]
ht_conf_colns = ['ht_x_nproc', 'ht_y_nproc', 'ht_ppw', 'ht_io_step', 'ht_io_buf']
sw_conf_colns = ['sw_nproc', 'sw_ppw', 'ht_io_step']
hs_conf_colns = ['ht_x_nproc', 'ht_y_nproc', 'ht_ppw', 'ht_io_step', 'ht_io_buf', 'sw_nproc', 'sw_ppw']
hs_in_conf_colns = ['ht_x', 'ht_y', 'ht_iter', 'ht_x_nproc', 'ht_y_nproc', 'ht_ppw', 'ht_io_step', 'ht_io_buf', \
                    'sw_nproc', 'sw_ppw']

# colns = df.columns.tolist()
def get_name(colns):
    if (all([x in colns for x in lv_in_conf_colns])):
        return 'lvi'
    elif (all([x in colns for x in lv_conf_colns])):
        return 'lv'
    elif (all([x in colns for x in lmp_conf_colns])):
        return 'lmp'
    elif (all([x in colns for x in vr_conf_colns])):
        return 'vr'
    elif (all([x in colns for x in hs_in_conf_colns])):
        return 'hsi'
    elif (all([x in colns for x in hs_conf_colns])):
        return 'hs'
    elif (all([x in colns for x in ht_conf_colns])):
        return 'ht'
    elif (all([x in colns for x in sw_conf_colns])):
        return 'sw'
    else:
        return 'unknown'

def df2string(df2D, super_delim=";", sub_delim=","):
    # super list elements separated by ;
    if (df2D.shape[0] <= 0):
        return ""
    L = []
    for index, data in df2D.iterrows():
        L.append(sub_delim.join(str(n) for n in data.tolist()))
    result = super_delim.join(L)
    return result

def string2df(string, colns, super_delim=';', sub_delim=','):
    list_str = string.split(super_delim)
    arr2d = []
    for row in list_str:
        list_item = row.split(sub_delim)
        arr_item = np.array([float(i) for i in list_item])
        if (len(arr2d) == 0):
            arr2d = np.array([np.append(arr2d, arr_item)])
        else:
            arr2d = np.append(arr2d, [arr_item], axis=0)
    df = pd.DataFrame(arr2d, columns=colns)
    return df

def df2csv(df, csv_file_name):
    fp = open(csv_file_name, "a")
    fp.write(df.to_csv(sep='\t', header=False, index=False))
    fp.close()

def csv2df(csv_file_name, conf_colns):
    app_name = get_name(conf_colns)
    if (app_name == 'lv'):
        df = lv_load(glob.glob(csv_file_name), conf_colns)
    elif (app_name == 'lvi'):
        df = lv_in_load(glob.glob(csv_file_name), conf_colns)
    elif (app_name == 'lmp'):
        df = lmp_load(glob.glob(csv_file_name), conf_colns)
    elif (app_name == 'vr'):
        df = vr_load(glob.glob(csv_file_name), conf_colns)
    elif (app_name == 'hs'):
        df = hs_load(glob.glob(csv_file_name), conf_colns)
    elif (app_name == 'hsi'):
        df = hs_in_load(glob.glob(csv_file_name), conf_colns)
    elif (app_name == 'ht'):
        df = ht_load(glob.glob(csv_file_name), conf_colns)
    elif (app_name == 'sw'):
        df = sw_load(glob.glob(csv_file_name), conf_colns)
    df = df.sort_values(conf_colns).reset_index(drop=True)
    return df

def gen_smpl(app_name, num_smpl, smpl_filename=''):
    if (app_name == 'lv'):
        smpls_df = gen_lv_smpl(num_smpl, smpl_filename)
    elif (app_name == 'lvi'):
        smpls_df = gen_lv_in_smpl(num_smpl, smpl_filename)
    elif (app_name == 'lmp'):
        smpls_df = gen_lmp_smpl(num_smpl, smpl_filename)
    elif (app_name == 'vr'):
        smpls_df = gen_vr_smpl(num_smpl, smpl_filename)
    elif (app_name == 'hs'):
        smpls_df = gen_hs_smpl(num_smpl, smpl_filename)
    elif (app_name == 'hsi'):
        smpls_df = gen_hs_in_smpl(num_smpl, smpl_filename)
    elif (app_name == 'ht'):
        smpls_df = gen_ht_smpl(num_smpl, smpl_filename)
    elif (app_name == 'sw'):
        smpls_df = gen_sw_smpl(num_smpl, smpl_filename)
    return smpls_df

def incr_rand_seed():
    global rand_seed
    rand_seed = rand_seed + 1
    random.seed(rand_seed)

def gen_lv_smpl(num_smpl, smpl_filename=''):
    # incr_rand_seed()
    random.seed(2019)
    lv_smpls = set([])
    while (len(lv_smpls) < num_smpl):
        lmp_nproc = random.randint(2, (num_core - 1) * (num_node - 1))
        lmp_ppw = random.randint(1, num_core - 1)
        lmp_nthread = random.randint(1, 4)
        lmp_io_step = random.randint(1, 8) * 50
        vr_nproc = random.randint(2, (num_core - 1) * (num_node - 1))
        vr_ppw = random.randint(1, num_core - 1)
        vr_nthread = random.randint(1, 4)
        
        if (lmp_nproc >= lmp_ppw and vr_nproc >= vr_ppw):
            if (lmp_nproc % lmp_ppw == 0 and vr_nproc % vr_ppw == 0):
                nodes = lmp_nproc // lmp_ppw + vr_nproc // vr_ppw
            elif (lmp_nproc % lmp_ppw == 0 or vr_nproc % vr_ppw == 0):
                nodes = lmp_nproc // lmp_ppw + vr_nproc // vr_ppw + 1
            else:
                nodes = lmp_nproc // lmp_ppw + vr_nproc // vr_ppw + 2
            if (nodes <= num_node):
                lv_smpls.add((lmp_nproc, lmp_ppw, lmp_nthread, lmp_io_step, vr_nproc, vr_ppw, vr_nthread))

    lv_smpls_df = pd.DataFrame(data = list(lv_smpls), columns=lv_conf_colns)
    if (smpl_filename != ''):
        df2csv(lv_smpls_df, smpl_filename)
    return lv_smpls_df

def gen_lv_in_smpl(num_smpl, smpl_filename=''):
    random.seed(2020)
    lv_smpls = set([])
    while (len(lv_smpls) < num_smpl):
        lmp_l2s = lmp_in_params[0] / (2 ** random.randint(0, 5))
        lmp_sld = lmp_in_params[1] / (2 ** random.randint(0, 5))
        lmp_nproc = random.randint(2, (num_core - 1) * (num_node - 1))
        lmp_ppw = random.randint(1, num_core - 1)
        lmp_nthread = random.randint(1, 4)
        lmp_io_step = random.randint(1, 8) * 50
        vr_nproc = random.randint(2, (num_core - 1) * (num_node - 1))
        vr_ppw = random.randint(1, num_core - 1)
        vr_nthread = random.randint(1, 4)
        
        if (lmp_nproc >= lmp_ppw and vr_nproc >= vr_ppw):
            if (lmp_nproc % lmp_ppw == 0 and vr_nproc % vr_ppw == 0):
                nodes = lmp_nproc // lmp_ppw + vr_nproc // vr_ppw
            elif (lmp_nproc % lmp_ppw == 0 or vr_nproc % vr_ppw == 0):
                nodes = lmp_nproc // lmp_ppw + vr_nproc // vr_ppw + 1
            else:
                nodes = lmp_nproc // lmp_ppw + vr_nproc // vr_ppw + 2
            if (nodes <= num_node):
                lv_smpls.add((lmp_l2s, lmp_sld, lmp_nproc, lmp_ppw, lmp_nthread, lmp_io_step, vr_nproc, vr_ppw, vr_nthread))

    smpls_df = pd.DataFrame(data = list(lv_smpls), columns=lv_in_conf_colns)
    if (smpl_filename != ''):
        df2csv(smpls_df, smpl_filename)
    return smpls_df

def gen_lmp_smpl(smpl_num, smpl_filename=''):
    random.seed(2021)
    smpls = set([])
    while (len(smpls) < smpl_num):
        lmp_nproc = random.randint(2, (num_core - 1) * (num_node - 1))
        lmp_ppw = random.randint(1, num_core - 1)
        lmp_nthread = random.randint(1, 4)
        lmp_io_step = random.randint(1, 8) * 50
        if (lmp_nproc >= lmp_ppw):
            if (lmp_nproc % lmp_ppw == 0):
                nodes = lmp_nproc // lmp_ppw
            else:
                nodes = lmp_nproc // lmp_ppw + 1
            if (nodes <= num_node - 1):
                smpls.add((lmp_nproc, lmp_ppw, lmp_nthread, lmp_io_step))
    smpls_df = pd.DataFrame(data = list(smpls), columns=lmp_conf_colns)
    if (smpl_filename != ''):
        df2csv(smpls_df, smpl_filename)
    return smpls_df

def gen_vr_smpl(smpl_num, smpl_filename):
    random.seed(2022)
    smpls = set([])
    while (len(smpls) < smpl_num):
        vr_nproc = random.randint(2, (num_core - 1) * (num_node - 1))
        vr_ppw = random.randint(1, num_core - 1)
        vr_nthread = random.randint(1, 4)
        lmp_io_step = random.randint(1, 8) * 50
        if (vr_nproc >= vr_ppw):
            if (vr_nproc % vr_ppw == 0):
                nodes = vr_nproc // vr_ppw
            else:
                nodes = vr_nproc // vr_ppw + 1
            if (nodes <= num_node - 1):
                smpls.add((vr_nproc, vr_ppw, vr_nthread, lmp_io_step))
    smpls_df = pd.DataFrame(data = list(smpls), columns=vr_conf_colns)
    if (smpl_filename != ''):
        df2csv(smpls_df, smpl_filename)
    return smpls_df     

def lmp_load(fns, conf_colns, perfn='run_time'):
    if (perfn == ''):
        colns = conf_colns
    else:
        colns = conf_colns + [perfn]
    val = []
    for fn in fns:
        for l in open(fn):
            val.append([float(s) for s in l.split()])
    return pd.DataFrame(val, columns=colns)

def vr_load(fns, conf_colns, perfn='run_time'):
    if (perfn == ''):
        colns = conf_colns
    else:
        colns = conf_colns + [perfn]
    val = []
    for fn in fns:
        for l in open(fn):
            val.append([float(s) for s in l.split()])
    return pd.DataFrame(val, columns=colns)

def lv_load(fns, conf_colns, perfn='run_time'):
    if (perfn == ''):
        colns = conf_colns
    else:
        colns = conf_colns + [perfn]
    val = []
    for fn in fns:
        for l in open(fn):
            val.append([float(s) for s in l.split()[:len(colns)]])
    return pd.DataFrame(val, columns=colns)

def lv_in_load(fns, conf_colns, perfn='run_time'):
    if (perfn == ''):
        colns = conf_colns
    else:
        colns = conf_colns + [perfn]
    val = []
    for fn in fns:
        for l in open(fn): 
            val.append([float(s) for s in l.split()[:len(colns)]])
    return pd.DataFrame(val, columns=colns)

def gen_hs_smpl(num_smpl, smpl_filename=''):
    # incr_rand_seed()
    random.seed(2019)
    hs_smpls = set([])
    while (len(hs_smpls) < num_smpl):
        max_nproc = (num_core - 1) * (num_node - 1)
        ht_x_nproc = random.randint(2, int(math.floor(math.sqrt(float(max_nproc)))))
        ht_y_nproc = random.randint(2, int(math.floor(math.sqrt(float(max_nproc)))))
        ht_ppw = random.randint(1, num_core - 1)
        ht_io_step = random.randint(1, 8) * 4
        ht_io_buf = random.randint(1, 40)
        sw_nproc = random.randint(2, max_nproc)
        sw_ppw = random.randint(1, num_core - 1)
        
        ht_nproc = ht_x_nproc * ht_y_nproc
        if (ht_nproc >= ht_ppw and sw_nproc >= sw_ppw):
            if (ht_nproc % ht_ppw == 0 and sw_nproc % sw_ppw == 0):
                nodes = ht_nproc // ht_ppw + sw_nproc // sw_ppw
            elif (ht_nproc % ht_ppw == 0 or sw_nproc % sw_ppw == 0):
                nodes = ht_nproc // ht_ppw + sw_nproc // sw_ppw + 1
            else:
                nodes = ht_nproc // ht_ppw + sw_nproc // sw_ppw + 2
            if (nodes <= num_node):
                hs_smpls.add((ht_x_nproc, ht_y_nproc, ht_ppw, ht_io_step, ht_io_buf, sw_nproc, sw_ppw))

    hs_smpls_df = pd.DataFrame(data = list(hs_smpls), columns=hs_conf_colns)
    if (smpl_filename != ''):
        df2csv(hs_smpls_df, smpl_filename)
    return hs_smpls_df

def gen_hs_in_smpl(num_smpl, smpl_filename=''):
    random.seed(2020)
    hs_smpls = set([])
    while (len(hs_smpls) < num_smpl):
        max_nproc = (num_core - 1) * (num_node - 1)
        ht_x = ht_in_params[0] / (2 ** random.randint(0, 5))
        ht_y = ht_in_params[1] / (2 ** random.randint(0, 5))
        ht_iter = ht_in_params[2] / (2 ** random.randint(0, 5))
        ht_x_nproc = random.randint(2, int(math.floor(math.sqrt(float(max_nproc)))))
        ht_y_nproc = random.randint(2, int(math.floor(math.sqrt(float(max_nproc)))))
        ht_ppw = random.randint(1, num_core - 1)
        ht_io_step = random.randint(1, 8) * 4
        ht_io_buf = random.randint(1, 40)
        sw_nproc = random.randint(2, max_nproc)
        sw_ppw = random.randint(1, num_core - 1)
        
        ht_nproc = ht_x_nproc * ht_y_nproc
        if (ht_nproc >= ht_ppw and sw_nproc >= sw_ppw):
            if (ht_nproc % ht_ppw == 0 and sw_nproc % sw_ppw == 0):
                nodes = ht_nproc // ht_ppw + sw_nproc // sw_ppw
            elif (ht_nproc % ht_ppw == 0 or sw_nproc % sw_ppw == 0):
                nodes = ht_nproc // ht_ppw + sw_nproc // sw_ppw + 1
            else:
                nodes = ht_nproc // ht_ppw + sw_nproc // sw_ppw + 2
            if (nodes <= num_node):
                hs_smpls.add((ht_x, ht_y, ht_iter, ht_x_nproc, ht_y_nproc, ht_ppw, ht_io_step, ht_io_buf, \
                              sw_nproc, sw_ppw))

    smpls_df = pd.DataFrame(data = list(hs_smpls), columns=hs_in_conf_colns)
    if (smpl_filename != ''):
        df2csv(smpls_df, smpl_filename)
    return smpls_df

def gen_ht_smpl(smpl_num, smpl_filename=''):
    random.seed(2021)
    smpls = set([])
    while (len(smpls) < smpl_num):
        max_nproc = (num_core - 1) * (num_node - 1)
        ht_x_nproc = random.randint(2, int(math.floor(math.sqrt(float(max_nproc)))))
        ht_y_nproc = random.randint(2, int(math.floor(math.sqrt(float(max_nproc)))))
        ht_ppw = random.randint(1, num_core - 1)
        ht_io_step = random.randint(1, 8) * 4
        ht_io_buf = random.randint(1, 40)
        
        ht_nproc = ht_x_nproc * ht_y_nproc
        if (ht_nproc >= ht_ppw):
            if (ht_nproc % ht_ppw == 0):
                nodes = ht_nproc // ht_ppw
            else:
                nodes = ht_nproc // ht_ppw + 1
            if (nodes <= num_node - 1):
                smpls.add((ht_x_nproc, ht_y_nproc, ht_ppw, ht_io_step, ht_io_buf))
    smpls_df = pd.DataFrame(data = list(smpls), columns=ht_conf_colns)
    if (smpl_filename != ''):
        df2csv(smpls_df, smpl_filename)
    return smpls_df

def gen_sw_smpl(smpl_num, smpl_filename=''):
    random.seed(2022)
    smpls = set([])
    while (len(smpls) < smpl_num):
        sw_nproc = random.randint(2, (num_core - 1) * (num_node - 1))
        sw_ppw = random.randint(1, num_core - 1)
        ht_io_step = random.randint(1, 8) * 4
        
        if (sw_nproc >= sw_ppw):
            if (sw_nproc % sw_ppw == 0):
                nodes = sw_nproc // sw_ppw
            else:
                nodes = sw_nproc // sw_ppw + 1
            if (nodes <= num_node - 1):
                smpls.add((sw_nproc, sw_ppw, ht_io_step))
    smpls_df = pd.DataFrame(data = list(smpls), columns=sw_conf_colns)
    if (smpl_filename != ''):
        df2csv(smpls_df, smpl_filename)
    return smpls_df

def ht_load(fns, conf_colns, perfn='run_time'):
    if (perfn == ''):
        colns = conf_colns
    else:
        colns = conf_colns + [perfn]
    val = []
    for fn in fns:
        for l in open(fn):
            val.append([float(s) for s in l.split()])
    return pd.DataFrame(val, columns=colns)

def sw_load(fns, conf_colns, perfn='run_time'):
    if (perfn == ''):
        colns = conf_colns
    else:
        colns = conf_colns + [perfn]
    val = []
    for fn in fns:
        for l in open(fn):
            val.append([float(s) for s in l.split()])
    return pd.DataFrame(val, columns=colns)

def hs_load(fns, conf_colns, perfn='run_time'):
    if (perfn == ''):
        colns = conf_colns
    else:
        colns = conf_colns + [perfn]
    val = []
    for fn in fns:
        for l in open(fn):
            val.append([float(s) for s in l.split()[:len(colns)]])
    return pd.DataFrame(val, columns=colns)

def hs_in_load(fns, conf_colns, perfn='run_time'):
    if (perfn == ''):
        colns = conf_colns
    else:
        colns = conf_colns + [perfn]
    val = []
    for fn in fns:
        for l in open(fn): 
            val.append([float(s) for s in l.split()[:len(colns)]])
    return pd.DataFrame(val, columns=colns)

def get_runnable_df(df, conf_colns, perf_coln='run_time'):
    arr = np.ones(df.shape[0])
    for i in range(df.shape[0]):
        if (df[perf_coln].values[i] == float('inf')):
            arr[i] = 0.0
    rem_colns = [i for i in df.columns.tolist() if i not in conf_colns]
    vld_df = pd.DataFrame(np.c_[df[conf_colns].values, arr, df[rem_colns].values], \
                          columns=conf_colns + ['runnable'] + rem_colns)
    return vld_df

def get_mach_time(nproc, ppn, runtime):
    nnode = np.negative(np.floor_divide(np.negative(nproc), ppn))
    mach_time = np.multiply(nnode, runtime) * num_core / 3600.0
    return mach_time

def invld_mach_time(nproc, ppn, timeout):
    nnode = np.negative(np.floor_divide(np.negative(nproc), ppn))
    return nnode * timeout * num_core / 3600.0

def get_exec_mach_df(exec_df):
    if ('run_time' not in exec_df.columns.tolist()):
        print "Error: there is no information on exection time!"
        return exec_df

    if ('mach_time' in exec_df.columns.tolist()):
        return exec_df

    df_name = get_name(exec_df.columns.tolist())
    if (df_name != 'lmp' and df_name != 'vr' and df_name != 'lv' and df_name != 'lvi' \
        and df_name != 'ht' and df_name != 'sw' and df_name != 'hs' and df_name != 'hsi'):
        print "Error: unknown dataframe!"
        return exec_df
    
    runtime = exec_df['run_time'].values
    if (df_name == 'lmp' or df_name == 'vr' or df_name == 'ht' or df_name == 'sw'):
        if (df_name == 'lmp'):
            nproc = exec_df['lmp_nproc'].values
            ppn = exec_df['lmp_ppw'].values
        elif (df_name == 'vr'):
            nproc = exec_df['vr_nproc'].values
            ppn = exec_df['vr_ppw'].values
        elif (df_name == 'ht'):
            nproc = exec_df['ht_x_nproc'].values * exec_df['ht_y_nproc'].values
            ppn = exec_df['ht_ppw'].values
        else:
            nproc = exec_df['sw_nproc'].values
            ppn = exec_df['sw_ppw'].values
        mach_time = get_mach_time(nproc, ppn, runtime)
    else:
        if (df_name == 'lv' or df_name == 'lvi'):
            sim_nproc = exec_df['lmp_nproc'].values
            sim_ppn = exec_df['lmp_ppw'].values
            anal_nproc = exec_df['vr_nproc'].values
            anal_ppn = exec_df['vr_ppw'].values
        else:
            sim_nproc = exec_df['ht_x_nproc'].values * exec_df['ht_y_nproc'].values
            sim_ppn = exec_df['ht_ppw'].values
            anal_nproc = exec_df['sw_nproc'].values
            anal_ppn = exec_df['sw_ppw'].values
        mach_time = get_mach_time(sim_nproc, sim_ppn, runtime) + get_mach_time(anal_nproc, anal_ppn, runtime)
    
    exec_mach_df = pd.DataFrame(np.c_[exec_df.values, mach_time], columns=exec_df.columns.tolist() + ['mach_time'])
    return exec_mach_df

def get_vld_df(df):
    return df[(df.runnable == 1.0)]

def get_invld_df(df):
    return df[(df.runnable == 0.0)]

def app_mach_time(df, timeout=0.0):
    if (df.shape[0] == 0):
        return 0.0
    
    df_name = get_name(df)
    if (df_name != 'lmp' and df_name != 'vr' and df_name != 'ht' and df_name != 'sw'):
        print "Error: in app_mach_time(), df is not lammps, vr, heat-transfer, or stage-write!"
        return -1.0
    
    vld_df = get_vld_df(df)
    if (df_name == 'lmp'):
        vld_nproc = vld_df['lmp_nproc'].values
        vld_ppn = vld_df['lmp_ppw'].values
    elif (df_name == 'vr'):
        vld_nproc = vld_df['vr_nproc'].values
        vld_ppn = vld_df['vr_ppw'].values
    elif (df_name == 'ht'):
        vld_nproc = vld_df['ht_x_nproc'].values * vld_df['ht_y_nproc'].values
        vld_ppn = vld_df['ht_ppw'].values
    else:
        vld_nproc = vld_df['sw_nproc'].values
        vld_ppn = vld_df['sw_ppw'].values
    vld_runtime = vld_df['run_time'].values
    vld_time = get_mach_time(vld_nproc, vld_ppn, vld_runtime).sum()
    
    invld_df = get_invld_df(df)
    if (df_name == 'lmp'):
        invld_nproc = invld_df['lmp_nproc'].values
        invld_ppn = invld_df['lmp_ppw'].values
    elif (df_name == 'vr'):
        invld_nproc = invld_df['vr_nproc'].values
        invld_ppn = invld_df['vr_ppw'].values
    elif (df_name == 'ht'):
        invld_nproc = invld_df['ht_x_nproc'].values * invld_df['ht_y_nproc'].values
        invld_ppn = invld_df['ht_ppw'].values
    else:
        invld_nproc = invld_df['sw_nproc'].values
        invld_ppn = invld_df['sw_ppw'].values
    if (timeout <= 0.0):
        timeout = max(vld_runtime) * 1.1
    invld_time = invld_mach_time(invld_nproc, invld_ppn, timeout).sum()
    return vld_time + invld_time

def sa_mach_time(df, timeout=0.0):
    if (df.shape[0] == 0):
        return 0.0
    
    df_name = get_name(df)
    if (df_name != 'lv' and df_name != 'lvi' and df_name != 'hs' and df_name != 'hsi'):
        print "Error: in sa_mach_time(), df is not lv, lvi, hs, or hsi!"
        return -1.0
    
    vld_df = get_vld_df(df)
    if (df_name == 'lv' or df_name == 'lvi'):
        vld_sim_nproc = vld_df['lmp_nproc'].values
        vld_sim_ppn = vld_df['lmp_ppw'].values
        vld_anal_nproc = vld_df['vr_nproc'].values
        vld_anal_ppn = vld_df['vr_ppw'].values
    else:
        vld_sim_nproc = vld_df['ht_x_nproc'].values * vld_df['ht_y_nproc'].values
        vld_sim_ppn = vld_df['ht_ppw'].values
        vld_anal_nproc = vld_df['sw_nproc'].values
        vld_anal_ppn = vld_df['sw_ppw'].values
    vld_runtime = vld_df['run_time'].values
    vld_time = get_mach_time(vld_sim_nproc, vld_sim_ppn, vld_runtime).sum() \
               + get_mach_time(vld_anal_nproc, vld_anal_ppn, vld_runtime).sum()
    
    invld_df = get_invld_df(df)
    if (df_name == 'lv' or df_name == 'lvi'):
        invld_sim_nproc = invld_df['lmp_nproc'].values
        invld_sim_ppn = invld_df['lmp_ppw'].values
        invld_anal_nproc = invld_df['vr_nproc'].values
        invld_anal_ppn = invld_df['vr_ppw'].values
    else:
        invld_sim_nproc = invld_df['ht_x_nproc'].values * invld_df['ht_y_nproc'].values
        invld_sim_ppn = invld_df['ht_ppw'].values
        invld_anal_nproc = invld_df['sw_nproc'].values
        invld_anal_ppn = invld_df['sw_ppw'].values
    if (timeout <= 0.0):
        timeout = max(vld_runtime) * 1.1
    invld_time = invld_mach_time(invld_sim_nproc, invld_sim_ppn, timeout).sum() \
                 + invld_mach_time(invld_anal_nproc, invld_anal_ppn, timeout).sum()
    return vld_time + invld_time

