import cvxpy as cp

def first_stage_reg(endog_var, z_var, dim_z, tau_first_stage):
    # Create optimization variables and a parameter
    beta = cp.Variable(dim_z)
    alpha = cp.Variable()
    tau = cp.Parameter()
    tau.value = tau_first_stage

    # Create the residual and error term of quatile regression model
    fit = z_var@beta + alpha
    resid = endog_var - fit
    error = cp.sum(0.5*cp.abs(resid) + (tau - 0.5)*resid)

    # Form the problem
    prob = cp.Problem(cp.Minimize(error))
    prob.solve()

    # Estimate the value of V to be used in the second stage
    vhat = resid.value
    return vhat
