import numpy as np
import pandas as pd
import random
import sys

if (len(sys.argv) != 2):
    print("gen_smpl.py workflow")
    print("\tworkflow: lv, hs, gvpv")
    exit()

wf = sys.argv[1]

num_node_lv = 32
num_node_hs = 32
num_node_gp = 32
num_core = 36
num_levl = 4

lmp_confn = ['lmp_nproc', 'lmp_ppn', 'lmp_tpp']
vr_confn = ['vr_nproc', 'vr_ppn', 'vr_tpp']
lmp_inn = ['lmp_nstep_out', 'lmp_l2s', 'lmp_sld']
lv_confn = lmp_confn + vr_confn
lmp_paramn = lmp_confn + lmp_inn
vr_paramn = vr_confn + lmp_inn
lv_paramn = lv_confn + lmp_inn

ht_confn = ['ht_x_nproc', 'ht_y_nproc', 'ht_ppn', 'ht_bufsize']
sw_confn = ['sw_nproc', 'sw_ppn']
ht_inn = ['ht_nout', 'ht_x', 'ht_y', 'ht_iter']
hs_confn = ht_confn + sw_confn
ht_paramn = ht_confn + ht_inn
sw_paramn = sw_confn + ht_inn
hs_paramn = hs_confn + ht_inn

gs_confn = ['gs_nproc', 'gs_ppn']
pdf_confn = ['pdf_nproc', 'pdf_ppn']
gs_inn = ['gs_cs', 'gs_step']
gp_confn = gs_confn + pdf_confn
gs_paramn = gs_confn + gs_inn
pdf_paramn = pdf_confn + gs_inn
gp_paramn = gp_confn + gs_inn

def df_slct(df, paramn, op, val=0):
    mask = (op(df[paramn].values, val))
    df = df.loc[mask]
    return df

def scal_input(df, in_paramn, r):
    for paramn in in_paramn:
        df[paramn] = np.ceil(np.divide(df[paramn], r))
    df = df.drop_duplicates().reset_index(drop=True).astype(int)
    return df

def scal_nproc(df, paramns, r):
    def ge(x1, x2):
        return x1 >= x2

    for paramn in paramns:
        df[paramn] = np.ceil(np.divide(df[paramn], r))
        df = df_slct(df, paramn, ge, 2)
    df = df.drop_duplicates().reset_index(drop=True).astype(int)
    return df

def df2csv(df, filename):
    f = open(filename, "w")
    f.write(df.to_csv(sep='\t', header=False, index=False))
    f.close()

def gen_smpl_lv(num_smpl_lv, filename_lv, filename_lmp, filename_vr, smll_smpl=True):
    random.seed(2019)
    smpls_lv = set([])
    smpls_lmp = set([])
    smpls_vr = set([])
    lmp_nstep_out_c = 200
    lmp_l2s_c = 16000
    lmp_sld_c = 20000
    while (len(smpls_lv) < num_smpl_lv):
        lmp_nproc = random.randint(2, (num_core - 1) * num_node_lv)
        lmp_ppn = random.randint(1, num_core - 1)
        lmp_tpn = random.randint(1, 2 * (num_core - 1))
        vr_nproc = random.randint(2, (num_core - 1) * num_node_lv)
        vr_ppn = random.randint(1, num_core - 1)
        vr_tpn = random.randint(1, 2 * (num_core - 1))
        lmp_nstep_out = random.randint(1, 8) * 50
        lmp_l2s = int(16000 / (2 ** random.randint(0, 5)))
        lmp_sld = int(20000 / (2 ** random.randint(0, 5)))

        if (lmp_nproc >= lmp_ppn):
            if (lmp_tpn % lmp_ppn == 0):
                lmp_tpp = lmp_tpn // lmp_ppn
            else:
                lmp_tpp = lmp_tpn // lmp_ppn + 1
            if (lmp_nproc % lmp_ppn == 0):
                lmp_nnode = lmp_nproc // lmp_ppn
            else:
                lmp_nnode = lmp_nproc // lmp_ppn + 1
            if (lmp_nnode <= num_node_lv):
                smpls_lmp.add((lmp_nproc, lmp_ppn, lmp_tpp, lmp_nstep_out, lmp_l2s, lmp_sld))

        if (vr_nproc >= vr_ppn):
            if (vr_tpn % vr_ppn == 0):
                vr_tpp = vr_tpn // vr_ppn
            else:
                vr_tpp = vr_tpn // vr_ppn + 1
            if (vr_nproc % vr_ppn == 0):
                vr_nnode = vr_nproc // vr_ppn
            else:
                vr_nnode = vr_nproc // vr_ppn + 1
            if (vr_nnode <= num_node_lv):
                smpls_vr.add((vr_nproc, vr_ppn, vr_tpp, lmp_nstep_out, lmp_l2s, lmp_sld))

        if (lmp_nproc >= lmp_ppn and vr_nproc >= vr_ppn):
            nnode = lmp_nnode + vr_nnode
            if (nnode <= num_node_lv):
                smpls_lv.add((lmp_nproc, lmp_ppn, lmp_tpp, vr_nproc, vr_ppn, vr_tpp, \
                        lmp_nstep_out, lmp_l2s, lmp_sld))

    df_smpl_lv = pd.DataFrame(data = list(smpls_lv), columns=lv_paramn)
    df_smpl_lv = df_smpl_lv.drop_duplicates().reset_index(drop=True).astype(int)
    print("The number of coupled LAMMPS and Voro++ samples =", df_smpl_lv.shape[0])
    print(df_smpl_lv.head(10))
    df2csv(df_smpl_lv, filename_lv + ".csv")

    df_smpl_lvc = pd.DataFrame(np.c_[df_smpl_lv.values[:, 0:6]], columns=lv_confn)
    df_smpl_lvc = df_smpl_lvc.drop_duplicates().reset_index(drop=True).astype(int)
    df_smpl_lvc['lmp_nstep_out'] = lmp_nstep_out_c
    df_smpl_lvc['lmp_l2s'] = lmp_l2s_c
    df_smpl_lvc['lmp_sld'] = lmp_sld_c
    print("The number of coupled LAMMPS and Voro++ samples =", df_smpl_lvc.shape[0])
    print(df_smpl_lvc.head(3))
    df2csv(df_smpl_lvc, filename_lv + "c.csv")

    df_smpl_lmp = pd.DataFrame(np.c_[df_smpl_lv.values[:, 0:3], df_smpl_lv.values[:, 6:9]], \
            columns=lmp_paramn)
    df_smpl_lmp2 = pd.DataFrame(data = list(smpls_lmp), columns=lmp_paramn)
    df_smpl_lmp = df_smpl_lmp.append(df_smpl_lmp2)
    df_smpl_lmp = df_smpl_lmp.drop_duplicates().reset_index(drop=True).astype(int)
    print("The number of LAMMPS samples =", df_smpl_lmp.shape[0])
    print(df_smpl_lmp.head(3))
    df2csv(df_smpl_lmp, filename_lmp + ".csv")
    
    df_smpl_lmpc = pd.DataFrame(np.c_[df_smpl_lmp.values[:, 0:3]], columns=lmp_confn)
    df_smpl_lmpc = df_smpl_lmpc.drop_duplicates().reset_index(drop=True).astype(int)
    df_smpl_lmpc['lmp_nstep_out'] = lmp_nstep_out_c
    df_smpl_lmpc['lmp_l2s'] = lmp_l2s_c
    df_smpl_lmpc['lmp_sld'] = lmp_sld_c
    print("The number of LAMMPS samples =", df_smpl_lmpc.shape[0])
    print(df_smpl_lmpc.head(3))
    df2csv(df_smpl_lmpc, filename_lmp + "c.csv")

    df_smpl_vr = pd.DataFrame(np.c_[df_smpl_lv.values[:, 3:9]], columns=vr_paramn)
    df_smpl_vr2 = pd.DataFrame(data = list(smpls_vr), columns=vr_paramn)
    df_smpl_vr = df_smpl_vr.append(df_smpl_vr2)
    df_smpl_vr = df_smpl_vr.drop_duplicates().reset_index(drop=True).astype(int)
    print("The number of Voro++ samples =", df_smpl_vr.shape[0])
    print(df_smpl_vr.head(3))
    df2csv(df_smpl_vr, filename_vr + ".csv")

    df_smpl_vrc = pd.DataFrame(np.c_[df_smpl_vr.values[:, 0:3]], columns=vr_confn)
    df_smpl_vrc = df_smpl_vrc.drop_duplicates().reset_index(drop=True).astype(int)
    df_smpl_vrc['lmp_nstep_out'] = lmp_nstep_out_c
    df_smpl_vrc['lmp_l2s'] = lmp_l2s_c
    df_smpl_vrc['lmp_sld'] = lmp_sld_c
    print("The number of Voro++ samples =", df_smpl_vrc.shape[0])
    print(df_smpl_vrc.head(3))
    df2csv(df_smpl_vrc, filename_vr + "c.csv")
    
    if (smll_smpl):
        df_smpl_lv_smll = df_smpl_lv.copy()
        df_smpl_lmp_smll = df_smpl_lmp.copy()
        df_smpl_vr_smll = df_smpl_vr.copy()
        ratio = 2
        for i in range(num_levl):
            df_smpl_lv_smll = scal_input(df_smpl_lv_smll, ['lmp_l2s', 'lmp_sld'], ratio)
            df_smpl_lv_smll = scal_nproc(df_smpl_lv_smll, ['lmp_nproc', 'vr_nproc'], ratio)
            print(df_smpl_lv_smll.head(3))
            df2csv(df_smpl_lv_smll, filename_lv + str(i+1) + ".csv")

            df_smpl_lmp_smll = scal_input(df_smpl_lmp_smll, ['lmp_l2s', 'lmp_sld'], ratio)
            df_smpl_lmp_smll = scal_nproc(df_smpl_lmp_smll, ['lmp_nproc'], ratio)
            print(df_smpl_lmp_smll.head(3))
            df2csv(df_smpl_lmp_smll, filename_lmp + str(i+1) + ".csv")

            df_smpl_vr_smll = scal_input(df_smpl_vr_smll, ['lmp_l2s', 'lmp_sld'], ratio)
            df_smpl_vr_smll = scal_nproc(df_smpl_vr_smll, ['vr_nproc'], ratio)
            print(df_smpl_vr_smll.head(3))
            df2csv(df_smpl_vr_smll, filename_vr + str(i+1) + ".csv")


def gen_smpl_hs(num_smpl_hs, filename_hs, filename_ht, filename_sw, smll_smpl=True):
    random.seed(2019)
    smpls_hs = set([])
    smpls_ht = set([])
    smpls_sw = set([])
    ht_nout_c = 16
    ht_x_c = 2048
    ht_y_c = 2048
    ht_iter_c = 1024
    while (len(smpls_hs) < num_smpl_hs):
        ht_x_nproc = random.randint(2, 32)
        ht_y_nproc = random.randint(2, 32)
        ht_ppn = random.randint(1, num_core - 1)
        ht_bufsize = random.randint(1, 40)
        sw_nproc = random.randint(2, (num_core - 1) * num_node_hs)
        sw_ppn = random.randint(1, num_core - 1)
        ht_nout = random.randint(1, 8) * 4
        ht_x = int(2048 / (2 ** random.randint(0, 5)))
        ht_y = int(2048 / (2 ** random.randint(0, 5)))
        ht_iter = int(1024 / (2 ** random.randint(0, 5)))

        ht_nproc = ht_x_nproc * ht_y_nproc
        if (ht_nproc >= ht_ppn):
            if (ht_nproc % ht_ppn == 0):
                ht_nnode = ht_nproc // ht_ppn
            else:
                ht_nnode = ht_nproc // ht_ppn + 1
            if (ht_nnode <= num_node_hs):
                smpls_ht.add((ht_x_nproc, ht_y_nproc, ht_ppn, ht_bufsize, \
                        ht_nout, ht_x, ht_y, ht_iter))

        if (sw_nproc >= sw_ppn):
            if (sw_nproc % sw_ppn == 0):
                sw_nnode = sw_nproc // sw_ppn
            else:
                sw_nnode = sw_nproc // sw_ppn + 1
            if (sw_nnode <= num_node_hs):
                smpls_sw.add((sw_nproc, sw_ppn, ht_nout, ht_x, ht_y, ht_iter))

        if (ht_nproc >= ht_ppn and sw_nproc >= sw_ppn):
            nnode = ht_nnode + sw_nnode
            if (nnode <= num_node_hs):
                smpls_hs.add((ht_x_nproc, ht_y_nproc, ht_ppn, ht_bufsize, sw_nproc, sw_ppn, \
                        ht_nout, ht_x, ht_y, ht_iter))

    df_smpl_hs = pd.DataFrame(data = list(smpls_hs), columns=hs_paramn)
    df_smpl_hs = df_smpl_hs.drop_duplicates().reset_index(drop=True).astype(int)
    print("The number of coupled Heat-transfer and Stage-write samples = ", df_smpl_hs.shape[0])
    print(df_smpl_hs.head(10))
    df2csv(df_smpl_hs, filename_hs + ".csv")
    
    df_smpl_hsc = pd.DataFrame(np.c_[df_smpl_hs.values[:, 0:6]], columns=hs_confn)
    df_smpl_hsc = df_smpl_hsc.drop_duplicates().reset_index(drop=True).astype(int)
    df_smpl_hsc['ht_nout'] = ht_nout_c
    df_smpl_hsc['ht_x'] = ht_x_c
    df_smpl_hsc['ht_y'] = ht_y_c
    df_smpl_hsc['ht_iter'] = ht_iter_c
    print("The number of coupled Heat-transfer and Stage-write samples =", df_smpl_hsc.shape[0])
    print(df_smpl_hsc.head(3))
    df2csv(df_smpl_hsc, filename_hs + "c.csv")

    df_smpl_ht = pd.DataFrame(np.c_[df_smpl_hs.values[:, 0:4], df_smpl_hs.values[:, 6:10]], \
            columns=ht_paramn)
    df_smpl_ht2 = pd.DataFrame(data = list(smpls_ht), columns=ht_paramn)
    df_smpl_ht = df_smpl_ht.append(df_smpl_ht2)
    df_smpl_ht = df_smpl_ht.drop_duplicates().reset_index(drop=True).astype(int)
    print("The number of Heat-transfer samples = ", df_smpl_ht.shape[0])
    print(df_smpl_ht.head(3))
    df2csv(df_smpl_ht, filename_ht + ".csv")
    
    df_smpl_htc = pd.DataFrame(np.c_[df_smpl_ht.values[:, 0:4]], columns=ht_confn)
    df_smpl_htc = df_smpl_htc.drop_duplicates().reset_index(drop=True).astype(int)
    df_smpl_htc['ht_nout'] = ht_nout_c
    df_smpl_htc['ht_x'] = ht_x_c
    df_smpl_htc['ht_y'] = ht_y_c
    df_smpl_htc['ht_iter'] = ht_iter_c
    print("The number of Heat-transfer samples =", df_smpl_htc.shape[0])
    print(df_smpl_htc.head(3))
    df2csv(df_smpl_htc, filename_ht + "c.csv")

    df_smpl_sw = pd.DataFrame(np.c_[df_smpl_hs.values[:, 4:10]], columns=sw_paramn)
    df_smpl_sw2 = pd.DataFrame(data = list(smpls_sw), columns=sw_paramn)
    df_smpl_sw = df_smpl_sw.append(df_smpl_sw2)
    df_smpl_sw = df_smpl_sw.drop_duplicates().reset_index(drop=True).astype(int)
    print("The number of Stage-write samples = ", df_smpl_sw.shape[0])
    print(df_smpl_sw.head(3))
    df2csv(df_smpl_sw, filename_sw + ".csv")
    
    df_smpl_swc = pd.DataFrame(np.c_[df_smpl_sw.values[:, 0:2]], columns=sw_confn)
    df_smpl_swc = df_smpl_swc.drop_duplicates().reset_index(drop=True).astype(int)
    df_smpl_swc['ht_nout'] = ht_nout_c
    df_smpl_swc['ht_x'] = ht_x_c
    df_smpl_swc['ht_y'] = ht_y_c
    df_smpl_swc['ht_iter'] = ht_iter_c
    print("The number of Stage-write samples =", df_smpl_swc.shape[0])
    print(df_smpl_swc.head(3))
    df2csv(df_smpl_swc, filename_sw + "c.csv")

    if (smll_smpl):
        df_smpl_hs_smll = df_smpl_hs.copy()
        df_smpl_ht_smll = df_smpl_ht.copy()
        df_smpl_sw_smll = df_smpl_sw.copy()
        ratio = 2
        for i in range(num_levl):
            if (i % 2 == 0):
                df_smpl_hs_smll = scal_input(df_smpl_hs_smll, ['ht_x'], ratio)
                df_smpl_hs_smll = scal_nproc(df_smpl_hs_smll, ['ht_x_nproc', 'sw_nproc'], ratio)
                df_smpl_ht_smll = scal_input(df_smpl_ht_smll, ['ht_x'], ratio)
                df_smpl_ht_smll = scal_nproc(df_smpl_ht_smll, ['ht_x_nproc'], ratio)
                df_smpl_sw_smll = scal_input(df_smpl_sw_smll, ['ht_x'], ratio)
            else:
                df_smpl_hs_smll = scal_input(df_smpl_hs_smll, ['ht_y'], ratio)
                df_smpl_hs_smll = scal_nproc(df_smpl_hs_smll, ['ht_y_nproc', 'sw_nproc'], ratio)
                df_smpl_ht_smll = scal_input(df_smpl_ht_smll, ['ht_y'], ratio)
                df_smpl_ht_smll = scal_nproc(df_smpl_ht_smll, ['ht_y_nproc'], ratio)
                df_smpl_sw_smll = scal_input(df_smpl_sw_smll, ['ht_y'], ratio)
            df_smpl_sw_smll = scal_nproc(df_smpl_sw_smll, ['sw_nproc'], ratio)

            print(df_smpl_hs_smll.head(3))
            df2csv(df_smpl_hs_smll, filename_hs + str(i+1) + ".csv")
            print(df_smpl_ht_smll.head(3))
            df2csv(df_smpl_ht_smll, filename_ht + str(i+1) + ".csv")
            print(df_smpl_sw_smll.head(3))
            df2csv(df_smpl_sw_smll, filename_sw + str(i+1) + ".csv")


def gen_smpl_gp(num_smpl_gp, filename_gp, filename_gs, filename_pdf, smll_smpl=True):
    random.seed(2019)
    smpls_gp = set([])
    smpls_gs = set([])
    smpls_pdf = set([])
    gs_cs_c = 512
    gs_step_c = 800
    while (len(smpls_gp) < num_smpl_gp):
        gs_nproc = random.randint(2, (num_core - 1) * (num_node_gp - 2))
        gs_ppn = random.randint(1, num_core - 1)
        pdf_nproc = random.randint(2, (num_core - 1) * (num_node_gp - 2))
        pdf_ppn = random.randint(1, num_core - 1)
        gs_cs = int(512 / (2 ** random.randint(0, 5)))
        gs_step = int(800 / (2 ** random.randint(0, 5)))

        if (gs_nproc >= gs_ppn):
            if (gs_nproc % gs_ppn == 0):
                gs_nnode = gs_nproc // gs_ppn
            else:
                gs_nnode = gs_nproc // gs_ppn + 1
            if (gs_nnode <= num_node_gp - 2):
                smpls_gs.add((gs_cs, gs_step, gs_nproc, gs_ppn))

        if (pdf_nproc >= pdf_ppn and pdf_nproc <= gs_cs):
            if (pdf_nproc % pdf_ppn == 0):
                pdf_nnode = pdf_nproc // pdf_ppn
            else:
                pdf_nnode = pdf_nproc // pdf_ppn + 1
            if (pdf_nnode <= num_node_gp - 2):
                smpls_pdf.add((gs_cs, gs_step, pdf_nproc, pdf_ppn))

        if (gs_nproc >= gs_ppn and pdf_nproc >= pdf_ppn and pdf_nproc <= gs_cs):
            nnode = gs_nnode + pdf_nnode
            if (nnode <= num_node_gp - 2):
                smpls_gp.add((gs_cs, gs_step, gs_nproc, gs_ppn, pdf_nproc, pdf_ppn))

    df_smpl_gp = pd.DataFrame(data = list(smpls_gp), columns=gp_paramn)
    df_smpl_gp = df_smpl_gp.drop_duplicates().reset_index(drop=True).astype(int)
    print("The number of GP samples =", df_smpl_gp.shape[0])
    print(df_smpl_gp.head(10))
    df2csv(df_smpl_gp, filename_gp + ".csv")

    df_smpl_gs = pd.DataFrame(np.c_[df_smpl_gp.values[:, 0:2], df_smpl_gp.values[:, 4:6]], \
            columns=gs_paramn)
    df_smpl_gs = df_smpl_gs.drop_duplicates().reset_index(drop=True)
    df_smpl_gs2 = pd.DataFrame(data = list(smpls_gs), columns=gs_paramn)
    df_smpl_gs = df_smpl_gs.append(df_smpl_gs2)
    df_smpl_gs = df_smpl_gs.drop_duplicates().reset_index(drop=True).astype(int)
    print("The number of Gray-scott samples =", df_smpl_gs.shape[0])
    print(df_smpl_gs.head(3))
    df2csv(df_smpl_gs, filename_gs + ".csv")

    df_smpl_pdf = pd.DataFrame(np.c_[df_smpl_gp.values[:, 2:6]], columns=pdf_paramn)
    df_smpl_pdf = df_smpl_pdf.drop_duplicates().reset_index(drop=True)
    df_smpl_pdf2 = pd.DataFrame(data = list(smpls_pdf), columns=pdf_paramn)
    df_smpl_pdf = df_smpl_pdf.append(df_smpl_pdf2)
    df_smpl_pdf = df_smpl_pdf.drop_duplicates().reset_index(drop=True).astype(int)
    print("The number of PDF calculator samples =", df_smpl_pdf.shape[0])
    print(df_smpl_pdf.head(3))
    df2csv(df_smpl_pdf, filename_pdf + ".csv")

    gp_smll_smpls_df = df_smpl_gp.copy()
    gs_smll_smpls_df = df_smpl_gs.copy()
    pdf_smll_smpls_df = df_smpl_pdf.copy()
    ratio = 1.259921
    for i in range(num_levl):
        gp_smll_smpls_df = scal_input(gp_smll_smpls_df, ['gs_cs'], ratio)
        gp_smll_smpls_df = scal_nproc(gp_smll_smpls_df, ['gs_nproc', 'pdf_nproc'], ratio ** 3)
        print(gp_smll_smpls_df.head(3))
        df2csv(gp_smll_smpls_df, filename_gp + str(i+1) + ".csv")

        gs_smll_smpls_df = scal_input(gs_smll_smpls_df, ['gs_cs'], ratio)
        gs_smll_smpls_df = scal_nproc(gs_smll_smpls_df, ['gs_nproc'], ratio ** 3)
        print(gs_smll_smpls_df.head(3))
        df2csv(gs_smll_smpls_df, filename_gs + str(i+1) + ".csv")

        pdf_smll_smpls_df = scal_input(pdf_smll_smpls_df, ['gs_cs'], ratio)
        pdf_smll_smpls_df = scal_nproc(pdf_smll_smpls_df, ['pdf_nproc'], ratio ** 3)
        print(pdf_smll_smpls_df.head(3))
        df2csv(pdf_smll_smpls_df, filename_pdf + str(i+1) + ".csv")


if (wf == 'lv'):
    gen_smpl_lv(2500, "lv/smpl_lv", "lv/smpl_lmp", "lv/smpl_vr")
elif (wf == 'hs'):
    gen_smpl_hs(2500, "hs/smpl_hs", "hs/smpl_ht", "hs/smpl_sw")
elif (wf == 'gvpv'):
    gen_smpl_gp(2500, "gp/smpl_gp", "gp/smpl_gs", "gp/smpl_pdf")
else:
    print("Error: unknown workflow!")
    exit()

