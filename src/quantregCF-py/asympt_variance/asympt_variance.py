import kernel

# calculate derivative_lambda

# dim_endo_exo = total length of endogenous variable and exogenous variables
dim_endo_exo = 1 + exog_var.shape[1]
derivative_lambda = 0

# option 0: polynomial series
if option == 0:
    # `beta` has length `dim_endo_exo` + `degree`
    # we need the last `degree` terms in `beta`, so we skip the first `dim_endo_exo` terms of `beta`
    # Note that the derivative of vhat^i is i*vhat^(i-1)
    # Thus, each derivative term of vhat, vhat^2, ..., vhat^degree is
    # 1, 2*vhat, 3*vhat^2, ..., degree*vhat^(degree-1)
    # Each term corresponds to beta[dim_endo_exo], ..., beta[dim_endo_exo+degree-1]
    for i in range(1, degree+1):
        derivative_lambda += i*(vhat**(i-1))*beta.value[dim_endo_exo+i-1]

# option 1: B-splines
if option == 1:
    # der = 1 for derivative
    derivative_lambda = 0
    all_derivative = eval_bspline_basis(x=vhat, df=2*degree-1, degree=degree, der=1, include_intercept=False)
    num_columns = all_derivative.shape[1]

    # `beta` has length `dim_endo_exo` + 2*`degree`-1
    # `all_derivative` has 2*`degree`-1 columns (`num_columns` = 2*`degree`-1)
    # we need the last `num_columns` terms in `beta`, so we skip the first `dim_endo_exo` terms of `beta`
    # Each column in `derivative_lambda` corresponds to beta[dim_endo_exo], ..., beta[dim_endo_exo+num_columns-1]
    for i in range(num_columns):
        derivative_lambda += all_derivative[:, i] * beta.value[dim_endo_exo+i]

# estimate K
tau = tau_second_stage
n = len(second_stage_residual)
bdw = np.std(second_stage_residual)*np.power(n, -1/5)
kl_weight = kl_normal(second_stage_residual/bdw)/bdw
Khat = np.diag(kl_weight)

# estimate Phi
Phat = np.column_stack([w_hat, np.tile(1, (len(w_hat), 1))])
Phihat = Phat.T@Khat@Phat/n

# estimate Sigma
Sigmahat = tau*(1-tau)*Phat.T@Phat/n

# estimate Gamma
tmp = kl_weight*derivative_lambda
KLdhat = np.diag(tmp)
Zhat = np.column_stack([z_var, np.tile(1, (len(z_var), 1))])
Gammahat = Phat.T@KLdhat@Zhat/n

# estimate Sigma_first_stage
bdw = np.std(vhat)*np.power(n, -1/5)
kl_weight = kl_normal(vhat/bdw)/bdw
Khat = np.diag(kl_weight)
tmp0 = Zhat.T@Khat@Zhat/n
tmp1 = tau*(1-tau)*Zhat.T@Zhat/n
Sigma_first_stage = np.linalg.inv(tmp0)@tmp1@np.linalg.inv(tmp0)

# estimate Omega
# first, specify A
dim_z1 = len(exog_var[0])
dim_w = len(Phat[0])
Amat1 = np.eye(1+dim_z1)
Amat2 = np.zeros((1+dim_z1, dim_w-1-dim_z1))
Amat = np.column_stack([Amat1, Amat2])

# then, estimate Omega
Omega1 = Amat@np.linalg.inv(Phihat)
Omega2 = Sigmahat + Gammahat@Sigma_first_stage@Gammahat.T
Omega = Omega1@Omega2@Omega1.T

# compute the standard error
avar = np.diag(Omega/n)
se = np.sqrt(avar)

# obtain the 95% confidence interval
ci_lb = betahat - 1.96*se[0]
ci_ub = betahat + 1.96*se[0]

print("Quantile: ", tau_first_stage, tau_second_stage, "Estimate: ", betahat, " Standard Error: ", se[0])
print("95% Confidence interval: ", ci_lb, ci_ub)