import json
import threading
import time
import traceback

import common as cm
import data
import learn

def run():
    """
    :param app_name: HPC application
    :param perf_coln: performance name to be optimized
    :param num_core: number of CPU cores
    :param num_node: number of computing nodes
    :param rand_seed: random seed
    :param num_smpl: number of samples
    """
    try:
        cm.init()
        app_name = cm.app_name
        perf_coln = cm.perf_coln
        num_smpl = cm.num_smpl

        if (app_name == "lv"):
            conf_colns = data.lv_conf_colns 
        elif (app_name == "hs"):
            conf_colns = data.hs_conf_colns

        conf_df = data.gen_smpl(app_name, num_smpl)
        train_df = cm.measure_perf(conf_df)
        data.df2csv(train_df, app_name + "_train.csv")
        mdl_chk, mdl = learn.train_mdl_chk(train_df, conf_colns, perf_coln)
        top_df = cm.find_top('baseline', (mdl_chk, mdl, ), conf_colns, perf_coln, train_df)

        cm.test(train_df, conf_colns, perf_coln)
        cm.finish(train_df, top_df)
    except:
         traceback.print_exc()

