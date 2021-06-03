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
    """
    try:
        cm.init()
        app_name = cm.app_name
        perf_coln = cm.perf_coln
        num_smpl = cm.num_smpl
        pool_size = cm.pool_size
        num_iter = cm.num_iter
        prec_rand = cm.prec_rand
    
        if (app_name == "lv"):
            conf_colns = data.lv_conf_colns 
        elif (app_name == "hs"):
            conf_colns = data.hs_conf_colns

        num_rand = int(num_smpl * prec_rand)
        nspi = int((num_smpl - num_rand) / num_iter)
        # pool_df = data.gen_smpl(app_name, pool_size)
        # conf_df = pool_df.head(num_rand)
        conf_df = data.gen_smpl(app_name, num_rand)
        train_df = cm.measure_perf(conf_df)

        for iter_idx in range(num_iter):
            num_curr = num_smpl - nspi * (num_iter - 1 - iter_idx)
 
            pool_df = data.gen_smpl(app_name, pool_size)
            pred_top_smpl = learn.whl_pred_top_eval(train_df, pool_df, conf_colns, perf_coln, num_smpl, 0)
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
    
        data.df2csv(train_df, app_name + "_train.csv")
        mdl_chk, mdl = learn.train_mdl_chk(train_df, conf_colns, perf_coln)
        top_df = cm.find_top('ALe', (mdl_chk, mdl, ), conf_colns, perf_coln, train_df)
    
        cm.test(train_df, conf_colns, perf_coln)
        cm.finish(train_df, top_df)
    except:
        traceback.print_exc()

