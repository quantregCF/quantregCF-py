import R_compat_quantile, eval_bspline_basis

# Create optimization variables and a parameter
dim_w = w_hat.shape[1]
beta = cp.Variable(dim_w)
alpha = cp.Variable()
tau = cp.Parameter()

# Create the residual and error term of quatile regression model
fit = w_hat@beta + alpha
resid = dep_var - fit
error = cp.sum(0.5*cp.abs(resid) + (tau - 0.5)*resid)

# Form the problem
prob = cp.Problem(cp.Minimize(error))

tau.value = tau_second_stage
prob.solve()
betahat = beta.value[0]
second_stage_residual = resid.value
