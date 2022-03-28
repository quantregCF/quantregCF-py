from urllib.request import urlopen
import pandas as pd

def loaddata(data_type, data_source, variable_lst):
    if data_type == 0:
        url = urlopen(data_source)
        df = pd.read_stata(url)

    dep_var_name = variable_lst[0]
    endog_var_name = variable_lst[1]
    exog_var_list = variable_lst[2]
    iv_var_list = variable_lst[3]

    # define the dependent variable (Y) and the endogenous right-hand side variable (X)
    dep_var = df[dep_var_name].to_numpy()
    endog_var = df[endog_var_name].to_numpy()

    # define exogenous included variables
    exog_var = df[exog_var_list].to_numpy()

    # define all exogenous variables
    z_var_list = exog_var_list + iv_var_list
    z_var = df[z_var_list].to_numpy()

    dim_z = len(z_var_list)

    return dep_var, endog_var, exog_var, z_var, dim_z