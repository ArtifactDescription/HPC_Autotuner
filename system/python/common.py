import json
import os
import pandas as pd
import random
import sys

import data
import eqpy
import learn
import search
import tool

# Global variable names we are going to set from the JSON settings file
global_settings = ["app_name", "perf_coln", "num_core", "num_node", "rand_seed", \
                   "num_smpl", "pool_size", "num_iter", "prec_rand", "prec_init", \
                   "lmp_l2s", "lmp_sld", "ht_x", "ht_y", "ht_iter"]

def load_settings(settings_filename):
    print("Reading settings: '%s'" % settings_filename)
    try:
        with open(settings_filename) as fp:
            settings = json.load(fp)
    except IOError as e:
        print("Could not open: '%s'" % settings_filename)
        print("PWD is: '%s'" % os.getcwd())
        sys.exit(1)
    try:
        for s in global_settings:
            globals()[s] = settings[s]
            print("%s: %s" % (s, str(settings[s])))
        data.rand_seed = rand_seed
        random.seed(rand_seed)
        data.num_core = num_core
        data.num_node = num_node
        data.lmp_in_params = [lmp_l2s, lmp_sld]
        data.ht_in_params = [ht_x, ht_y, ht_iter]
    except KeyError as e:
        print("Settings file (%s) does not contain key: %s" % (settings_filename, str(e)))
        sys.exit(1)
    print("Settings loaded.")

def init():
    eqpy.OUT_put("Settings")
    settings_filename = eqpy.IN_get()
    load_settings(settings_filename)

def app_in_name(app_name):
    return app_name + "i"

def app1_name(app_name):
    if (app_name == "lv"):
        return "lmp"
    elif (app_name == "hs"):
        return "ht"
    else:
        return "none"

def app2_name(app_name):
    if (app_name == "lv"):
        return "vr"
    elif (app_name == "hs"):
        return "sw"
    else:
        return "none"

def measure_perf(conf_df):
    conf_colns = conf_df.columns.tolist()
    app_name = data.get_name(conf_colns)
    data_df = data.csv2df(app_name + "_time.csv", conf_colns)
    conf_perf_df = tool.df_intersection(data_df, conf_df, conf_colns)
    new_conf_df = tool.df_sub(conf_df, conf_perf_df, conf_colns)
    if (new_conf_df.shape[0] > 0):
        new_conf_df = new_conf_df.astype(int)
        eqpy.OUT_put(app_name)
        eqpy.OUT_put(data.df2string(new_conf_df))
        result = eqpy.IN_get()
        time_df = data.string2df(result, ['run_time'])
        new_conf_perf_df = pd.concat([new_conf_df, time_df], axis=1)
        data.df2csv(new_conf_perf_df, app_name + "_time_new.csv")
        conf_perf_df = tool.df_union(conf_perf_df, new_conf_perf_df)
    conf_perf_df = data.get_exec_mach_df(data.get_runnable_df(conf_perf_df, conf_colns))
    if (conf_df.shape[0] != conf_perf_df.shape[0]):
        print "Error: conf_df.shape[0] != conf_perf_df.shape[0]", conf_df.shape[0], conf_perf_df.shape[0]
    return conf_perf_df

def find_top(algo, mdls, conf_colns, perf_coln, train_df):
    print "Start searching for the top!"
    top_pred_df = search.get_pred_top_smpl(algo, mdls, conf_colns, perf_coln)
    top_conf_df = top_pred_df[conf_colns]
    top_df = measure_perf(top_conf_df)
    top_df = tool.df_union(top_df, train_df)
    top_df = top_df.sort_values([perf_coln]).reset_index(drop=True)
    top_df = top_df.head(1)
    data.df2csv(top_df, app_name + "_top.csv")
    return top_df

def test(train_df, conf_colns, perf_coln):
    test_df = data.csv2df(app_name + "_time.csv", conf_colns)
    test_df = data.get_exec_mach_df(data.get_runnable_df(test_df, conf_colns))
'''
    pred_top_df, err_df, rs_df = learn.whl_pred_top_eval(train_df, test_df, conf_colns, perf_coln, 10)
    data.df2csv(pred_top_df, app_name + "_test.csv")
    data.df2csv(rs_df, app_name + "_rs")
    data.df2csv(err_df, app_name + "_err.csv")
'''

def finish(train_df, top_df):
    eqpy.OUT_put("FINAL")
    eqpy.OUT_put("{0}\n{1}".format(data.df2string(train_df), data.df2string(top_df)))

