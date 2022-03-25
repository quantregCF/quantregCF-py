from quantregCF import quantregCF

# data
data_source = "http://people.brandeis.edu/~kgraddy/datasets/fishdata.dta"
var_lst = ['qty', 'price', ["day1", "day2", "day3", "day4"], ["stormy", "mixed"]]
data_lst = [0, data_source, var_lst]

# regressions
beta, se = quantregCF(option=1, degree=3, tau_first_stage=0.5, tau_second_stage=0.5, data=data_lst):

# CI
betahat = beta.value[0]

# obtain the 95% confidence interval
ci_lb = betahat - 1.96 * se[0]
ci_ub = betahat + 1.96 * se[0]

## Expected results from `original.py`
# Quantile:  0.5 0.5 Estimate:  -0.3229033782770835  Standard Error:  0.344419675456656
# 95% Confidence interval:  -0.9979659421721293 0.35215918561796233

print("Quantile: ", tau_first_stage, tau_second_stage, "Estimate: ", betahat, " Standard Error: ", se[0])
print("95% Confidence interval: ", ci_lb, ci_ub)
