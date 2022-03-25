from loaddata import loaddata
from first_reg import first_stage_reg
from second_reg import second_stage_reg
from dev_lambda import dev_lambda
from asympt_variance import asympt_variance

### Set variables
# TODO: The program takes 6 inputs: option, degree, tau_first_stage, tau_second_stage, data_type, data_source
tau_first_stage = 0.5
tau_second_stage = 0.5
option = 1
degree = 3
data_type = 0  # default = 0 (url link)
data_source = "http://people.brandeis.edu/~kgraddy/datasets/fishdata.dta"

### Load the dataset
dep_var, endog_var, exog_var, z_var, dim_z = loaddata(data_type, data_source)

### Regressions
vhat = first_stage_reg(endog_var, z_var, dim_z, tau_first_stage)
w_hat, beta, second_stage_res = second_stage_reg(dep_var, endog_var, exog_var, tau_second_stage, degree, option, vhat)
derivative_lambda = dev_lambda(exog_var, beta, option, degree, vhat)
se = asympt_variance(exog_var, z_var, tau_second_stage, w_hat, vhat, second_stage_res, derivative_lambda)

### Test results
# TODO: separate test files
betahat = beta.value[0]

# obtain the 95% confidence interval
ci_lb = betahat - 1.96 * se[0]
ci_ub = betahat + 1.96 * se[0]

## Expected results from `original.py`
# Quantile:  0.5 0.5 Estimate:  -0.3229033782770835  Standard Error:  0.344419675456656
# 95% Confidence interval:  -0.9979659421721293 0.35215918561796233

print("Quantile: ", tau_first_stage, tau_second_stage, "Estimate: ", betahat, " Standard Error: ", se[0])
print("95% Confidence interval: ", ci_lb, ci_ub)