import pandas as pd
from quantregCF import quantregCF

# load data from https://www.kathryngraddy.org/research#pubdata
# data = [dataframe, variable_lst]
data_source = "https://uploads-ssl.webflow.com/629e460595fdd36617348189/62a0fd19b6742078eed59f47_fish.out.txt"
df = pd.read_csv(data_source, sep="\t")
var_lst = ['qty', 'price', ["day1", "day2", "day3", "day4"], ["stormy", "mixed"]]
data_lst = [df, var_lst]

# regressions
tau_1 = 0.5
tau_2 = 0.5
beta, se = quantregCF(option=1, degree=3, tau_first_stage=tau_1, tau_second_stage=tau_2, data=data_lst)

# CI
betahat = beta[0]

# obtain the 95% confidence interval
ci_lb = betahat - 1.96 * se[0]
ci_ub = betahat + 1.96 * se[0]

print("Using tau as {} and {}, the estimated beta is {}, and the standard error is {}.".format(tau_1, tau_2, betahat, se[0]))
print("The 95% confidence interval is [{}, {}].".format(ci_lb, ci_ub))

## 99% confidence interval
ci_lb = betahat - 2.58 * se[0]
ci_ub = betahat + 2.58 * se[0]
print("The 99% confidence interval is [{}, {}].".format(ci_lb, ci_ub))