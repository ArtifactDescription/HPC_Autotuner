import pandas as pd
import threading
import traceback

import common as cm
import data
import learn
import tool

def run():
    """
    :param app_name: HPC application
    :param perf_coln: performance name to be optimized
    :param num_core: number of CPU cores
    :param num_node: number of computing nodes
    :param rand_seed: random seed
    :param num_smpl: number of samples
    :param pool_size: pool size
    :param num_iter: number of iterations
    :param prec_rand: precentage of random samples
    :param prec_init: precentage of initial samples replaced by equivalent samples
    """
    try:
        cm.init()
        app_name = cm.app_name
        perf_coln = cm.perf_coln
        num_smpl = cm.num_smpl
        pool_size = cm.pool_size
        num_iter = cm.num_iter
        prec_rand = cm.prec_rand
        prec_init = cm.prec_init
    
        if (app_name == "lv"):
            conf_colns = data.lv_conf_colns
            conf1_colns = data.lmp_conf_colns
            conf2_colns = data.vr_conf_colns
        elif (app_name == "hs"):
            conf_colns = data.hs_conf_colns
            conf1_colns = data.ht_conf_colns
            conf2_colns = data.sw_conf_colns

        num_rand = int(num_smpl * prec_rand)
        # pool_df = data.gen_smpl(app_name, pool_size)
        # conf_df = pool_df.head(num_rand)
        conf_df = data.gen_smpl(app_name, num_rand)
        train_df = cm.measure_perf(conf_df)

        num_init = int(num_smpl * prec_init)
        pool1_df = data.gen_smpl(cm.app1_name(app_name), num_init * 100)
        conf1_df = pool1_df.head(num_init)
        train1_df = cm.measure_perf(conf1_df)
        pool2_df = data.gen_smpl(cm.app2_name(app_name), num_init * 100)
        conf2_df = pool2_df.head(num_init)
        train2_df = cm.measure_perf(conf2_df)

        avg_mach_time = data.sa_mach_time(train_df) / num_rand
        avg_sprt_mach_time = (data.app_mach_time(train1_df) + \
                              data.app_mach_time(train2_df)) / num_init
        factor = max(1, avg_mach_time / avg_sprt_mach_time)
        if (factor > 1):
            num_sprt = int(num_init * factor)
            new_conf1_df = pool1_df.head(num_sprt).tail(num_sprt - num_init)
            new_train1_df = cm.measure_perf(new_conf1_df)
            train1_df = tool.df_union(train1_df, new_train1_df)
            new_conf2_df = pool2_df.head(num_sprt).tail(num_sprt - num_init)
            new_train2_df = cm.measure_perf(new_conf2_df)
            train2_df = tool.df_union(train2_df, new_train2_df)

        pool_df = data.gen_smpl(app_name, pool_size)
        pred_top_smpl = learn.sprt_pred_top_eval(train1_df, train2_df, pool_df, conf1_colns, conf2_colns, conf_colns, perf_coln, num_smpl, 0) 

        nspi = int((num_smpl - num_init - num_rand) / num_iter)

        for iter_idx in range(num_iter):
            num_curr = num_smpl - num_init - nspi * (num_iter - 1 - iter_idx)

            pred_top_smpl = pred_top_smpl.sort_values([perf_coln]).reset_index(drop=True)
            new_conf_df = pred_top_smpl[conf_colns].head(nspi)
            conf_df = tool.df_union(conf_df, new_conf_df)

            last = nspi
            while (conf_df.shape[0] < num_curr):
                last = last + 1
                new_conf_df = pred_top_smpl[conf_colns].head(last)
                conf_df = tool.df_union(conf_df, new_conf_df)

            new_train_df = cm.measure_perf(new_conf_df)
            train_df = tool.df_union(train_df, new_train_df)
            if (iter_idx < num_iter - 1):
                pool_df = data.gen_smpl(app_name, pool_size)
                pred_top_smpl = learn.whl_pred_top_eval(train_df, pool_df, conf_colns, perf_coln, num_smpl, 0)

        data.df2csv(train_df, app_name + "_train.csv")
        mdl_chk, mdl = learn.train_mdl_chk(train_df, conf_colns, perf_coln)
        top_df = cm.find_top('TaLeC', (mdl_chk, mdl, ), conf_colns, perf_coln, train_df)
    
        cm.test(train_df, conf_colns, perf_coln)
        cm.finish(train_df, top_df)
    except:
        traceback.print_exc()

