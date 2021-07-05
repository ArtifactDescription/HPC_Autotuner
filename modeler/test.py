import numpy as np
import pandas as pd
import xgboost as xgb
import sample as sp
import modeler as mdlr

gs_mdl = mdlr.train_mdl(sp.df_gs, sp.gs_confn, 'exec_time')
pdf_mdl = mdlr.train_mdl(sp.df_pdf, sp.pdf_confn, 'exec_time')
cpnt_mdls = [gs_mdl, pdf_mdl, sp.df_gplot, sp.df_pplot]
for i in range(len(cpnt_mdls)):
    if isinstance(cpnt_mdls[i], xgb.sklearn.XGBRegressor):
        print("xgb.sklearn.XGBRegressor")
    elif isinstance(cpnt_mdls[i], float):
        print("float")
    elif isinstance(cpnt_mdls[i], pd.core.frame.DataFrame):
        print("pd.core.frame.DataFrame")
    else:
        print(f"Unknown type of cpnt_mdls[{i}]")

print(3 * np.ones(5))
