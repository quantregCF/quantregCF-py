import numpy as np
import cvxpy as cp
from .eval_bspline_basis import eval_bspline_basis

def second_stage_reg(dep_var, endog_var, exog_var, tau_second_stage, degree, option, vhat):
    # create w_hat and vhat for the second stage regression
    # option 0: polynomial series
    if option == 0:
        w_hat = [endog_var, exog_var]
        for j in range(1, degree + 1):
            w_hat.append(np.power(vhat, j))
        w_hat = np.column_stack(w_hat)

    # option 1: B-splines
    if option == 1:
        vhat_bs_hand = eval_bspline_basis(x=vhat, df=2 * degree - 1, degree=degree, der=0, include_intercept=False)
        w_hat = np.column_stack([endog_var, exog_var, vhat_bs_hand])

    # Create optimization variables and a parameter
    dim_w = w_hat.shape[1]
    beta = cp.Variable(dim_w)
    alpha = cp.Variable()
    tau = cp.Parameter()

    # Create the residual and error term of quantile regression model
    fit = w_hat@beta + alpha
    resid = dep_var - fit
    error = cp.sum(0.5*cp.abs(resid) + (tau - 0.5)*resid)

    # Form the problem
    prob = cp.Problem(cp.Minimize(error))
    tau.value = tau_second_stage
    prob.solve()

    second_stage_residual = resid.value

    return w_hat, beta, second_stage_residual