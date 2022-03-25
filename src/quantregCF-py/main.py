import first_reg
import second_reg
import asympt_variance
import kernel
from urllib.request import urlopen
import pandas as pd

# load the dataset
url = urlopen("http://people.brandeis.edu/~kgraddy/datasets/fishdata.dta")
df = pd.read_stata(url)

# define the dependent variable (Y) and the endogenous right-hand side variable (X)
dep_var = df["qty"].to_numpy()
endog_var = df["price"].to_numpy()

# define exogenous included variables
exog_var_list = ["day1", "day2", "day3", "day4"]
exog_var = df[exog_var_list].to_numpy()

# define instrumental variables
iv_var_list = ["stormy", "mixed"]
iv_var = df[iv_var_list].to_numpy()

# define all exogenous variables
z_var_list = ["day1", "day2", "day3", "day4", "stormy", "mixed"]
z_var = df[z_var_list].to_numpy()



if __name__ == "__main__":
