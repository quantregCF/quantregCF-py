from loaddata import loaddata
from first_reg import first_stage_reg
from second_reg import second_stage_reg
from dev_lambda import dev_lambda
from asympt_variance import asympt_variance

# data = [data_type, data_source, variable_lst]
def quantregCF(option=1, degree=3, tau_first_stage=0.5 , tau_second_stage=0.5, data=[]):
    # load the dataset
    dep_var, endog_var, exog_var, z_var, dim_z = loaddata(data[0], data[1], data[2])

    # regressions
    vhat = first_stage_reg(endog_var, z_var, dim_z, tau_first_stage)
    w_hat, beta, second_stage_res = second_stage_reg(dep_var, endog_var, exog_var, tau_second_stage, degree, option, vhat)
    derivative_lambda = dev_lambda(exog_var, beta, option, degree, vhat)
    se = asympt_variance(exog_var, z_var, tau_second_stage, w_hat, vhat, second_stage_res, derivative_lambda)

    return beta, se