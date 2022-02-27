### 2. First Stage Regression

# Create optimization variables and a parameter
dim_z = len(z_var_list)
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
