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
    """
    try:
        cm.init()
        app_name = cm.app_name
        perf_coln = cm.perf_coln
        num_smpl = cm.num_smpl
    
        if (app_name == "lv"):
            conf_colns = data.lv_conf_colns
            conf1_colns = data.lmp_conf_colns
            conf2_colns = data.vr_conf_colns
        elif (app_name == "hs"):
            conf_colns = data.hs_conf_colns
            conf1_colns = data.ht_conf_colns
            conf2_colns = data.sw_conf_colns

        train1_fn = cm.app1_name(app_name) + "_time.csv"
        train1_df = data.csv2df(train1_fn, conf1_colns)
        train1_df = data.get_exec_mach_df(data.get_runnable_df(train1_df, conf1_colns))
        mdl1_chk, mdl1 = learn.train_mdl_chk(train1_df, conf1_colns, perf_coln)

        train2_fn = cm.app2_name(app_name) + "_time.csv"
        train2_df = data.csv2df(train2_fn, conf2_colns)
        train2_df = data.get_exec_mach_df(data.get_runnable_df(train2_df, conf2_colns))
        mdl2_chk, mdl2 = learn.train_mdl_chk(train2_df, conf2_colns, perf_coln)

        conf_df = data.gen_smpl(app_name, num_smpl)
        train_df = cm.measure_perf(conf_df)
        data.df2csv(train_df, app_name + "_train.csv")
        train_intrmdt_df = learn.add_layer_sprt_pred(train_df, conf1_colns, conf2_colns, conf_colns, \
                                                     perf_coln, mdl1_chk, mdl1, mdl2_chk, mdl2)
        mdl_chk, mdl = learn.train_mdl_chk(train_intrmdt_df, \
                                           conf_colns + [perf_coln+'1', perf_coln+'2'], perf_coln)
        top_df = cm.find_top('cmtl_ch', (mdl1_chk, mdl1, mdl2_chk, mdl2, mdl_chk, mdl, ), conf_colns, perf_coln, train_df)

        test_df = data.csv2df(app_name + "_time.csv", conf_colns)
        test_df = data.get_exec_mach_df(data.get_runnable_df(test_df, conf_colns))
        test_intrmdt_df = learn.add_layer_sprt_pred(test_df, conf1_colns, conf2_colns, conf_colns, \
                                                    perf_coln, mdl1_chk, mdl1, mdl2_chk, mdl2)
        '''
        pred_top, err, rs = learn.whl_pred_top_eval(train_intrmdt_df, test_intrmdt_df, \
                                                    conf_colns + [perf_coln+'1', perf_coln+'2'], \
                                                    perf_coln, 10)
        data.df2csv(pred_top, app_name + "_test.csv")
        data.df2csv(rs, app_name + "_rs")
        data.df2csv(err, app_name + "_err.csv")
        '''
        cm.finish(train_df, top_df)
    except:
        traceback.print_exc()

