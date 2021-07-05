import sample as sp
import sys

if (len(sys.argv) != 3):
    print("dist.py application performance")
    print("\tapplication: lmp, vr, lv, ht, sw, hs, gs, pdf, gvpv")
    print("\tperformance: exec_time, comp_time")
    exit()

wf = sys.argv[1]
perfn = sys.argv[2]

dir_name = '../plot/dist/'

if (wf == 'lmp'):
    df_perf = sp.df_lmp[['exec_time', 'comp_time']]
elif (wf == 'vr'):
    df_perf = sp.df_vr[['exec_time', 'comp_time']]
elif (wf == 'lv'):
    df_perf = sp.df_lv[['exec_time', 'comp_time']]
elif (wf == 'ht'):
    df_perf = sp.df_ht[['exec_time', 'comp_time']]
elif (wf == 'sw'):
    df_perf = sp.df_sw[['exec_time', 'comp_time']]
elif (wf == 'hs'):
    df_perf = sp.df_hs[['exec_time', 'comp_time']]
elif (wf == 'gs'):
    df_perf = sp.df_gs[['exec_time', 'comp_time']]
elif (wf == 'pdf'):
    df_perf = sp.df_pdf[['exec_time', 'comp_time']]
elif (wf == 'gvpv'):
    df_perf = sp.df_gvpv[['exec_time', 'comp_time']]
else:
    print("Error: unknown workflow!")
    exit()

sp.df2csv(df_perf[perfn], dir_name + wf + '_' + perfn + '.csv')
'''
exec_upper = 20 * min(df_perf['exec_time'].values)
comp_upper = 20 * min(df_perf['comp_time'].values)
if (perfn == 'exec_time'):
    sp.df2csv(df_perf[df_perf.exec_time <= exec_upper][perfn], \
            dir_name + wf + '_' + perfn + '.csv')
elif (perfn == 'comp_time'):
    sp.df2csv(df_perf[df_perf.comp_time <= comp_upper][perfn], \
            dir_name + wf + '_' + perfn + '.csv')
else:
    print("Error: unknown performance metrics!")
    exit()
'''
