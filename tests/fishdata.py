from quantregCF import quantregCF

# data
data_source = "http://people.brandeis.edu/~kgraddy/datasets/fishdata.dta"
var_lst = ['qty', 'price', ["day1", "day2", "day3", "day4"], ["stormy", "mixed"]]
data_lst = [data_source, data_source, var_lst]

# regressions
tau_1 = 0.5
tau_2 = 0.5
beta, se = quantregCF(option=1, degree=3, tau_first_stage=tau_1, tau_second_stage=tau_2, data=data_lst)

# CI
betahat = beta[0]

# obtain the 95% confidence interval
ci_lb = betahat - 1.96 * se[0]
ci_ub = betahat + 1.96 * se[0]

## Expected results
# Estimated beta = -0.3229033782770835,  Standard Error = 0.344419675456656
# 95% Confidence interval = [-0.9979659421721293 0.35215918561796233]
print("Using tau as {} and {}, the estimated beta is {}, and the standard error is {}.".format(tau_1, tau_2, betahat, se[0]))
print("The 95% confidence interval is [{}, {}].".format(tau_1, tau_2, ci_lb, ci_ub))

## 99% confidence interval
ci_lb = betahat - 2.58 * se[0]
ci_ub = betahat + 2.58 * se[0]
print("The 99% confidence interval is [{}, {}].".format(tau_1, tau_2, ci_lb, ci_ub))