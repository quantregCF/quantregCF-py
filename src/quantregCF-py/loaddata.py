from urllib.request import urlopen
import pandas as pd

def loaddata(data_type, data_source):
    if data_type == 0:
        url = urlopen(data_source)
        df = pd.read_stata(url)

    # define the dependent variable (Y) and the endogenous right-hand side variable (X)
    dep_var = df["qty"].to_numpy()
    endog_var = df["price"].to_numpy()

    # define exogenous included variables
    exog_var_list = ["day1", "day2", "day3", "day4"]
    exog_var = df[exog_var_list].to_numpy()

    # define instrumental variables
    #iv_var_list = ["stormy", "mixed"]
    #iv_var = df[iv_var_list].to_numpy()

    # define all exogenous variables
    z_var_list = ["day1", "day2", "day3", "day4", "stormy", "mixed"]
    z_var = df[z_var_list].to_numpy()

    dim_z = len(z_var_list)

    return dep_var, endog_var, exog_var, z_var, dim_z
