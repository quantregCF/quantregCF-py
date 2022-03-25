from urllib.request import urlopen
import pandas as pd
import numpy as np
import cvxpy as cp

# take the following inputs: option, degree, tau_first_stage, tau_second_stage

# 'tau_first_stage' is for the first stage regression
# 'tau' is for the second stage regression
tau_first_stage = 0.5
tau_second_stage = 0.5
option = 1
degree = 3

### 1. Prepare data
# TODO: change to any dataset

# load the dataset
url = urlopen("http://people.brandeis.edu/~kgraddy/datasets/fishdata.dta")
df = pd.read_stata(url)

# define the dependent variable (Y) and the endogenous right-hand side variable (X)
dep_var = df["qty"].to_numpy()
endog_var = df["price"].to_numpy()

# define exogenous included variables
exog_var_list = ["day1", "day2", "day3", "day4"]
exog_var = df[exog_var_list].to_numpy()

# define instrumental variables
iv_var_list = ["stormy", "mixed"]
iv_var = df[iv_var_list].to_numpy()

# define all exogenous variables
z_var_list = ["day1", "day2", "day3", "day4", "stormy", "mixed"]
z_var = df[z_var_list].to_numpy()


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


### 3. Second Stage Regression

# The following functions 'R_compat_quantile' and 'eval_bspline_basis' are copied from patsy.
def R_compat_quantile(x, probs):
    #return np.percentile(x, 100 * np.asarray(probs))
    probs = np.asarray(probs)
    quantiles = np.asarray([np.percentile(x, 100 * prob) for prob in probs.ravel(order="C")])
    return quantiles.reshape(probs.shape, order="C")

def eval_bspline_basis(x, df, degree, der, include_intercept):
    # Note: the order of a spline is the same as its degree + 1.
    # Note: there are (len(knots) - order) basis functions.
    order = degree + 1
    n_inner_knots = df - order
    if not include_intercept:
        n_inner_knots += 1
    knot_quantiles = np.linspace(0, 1, n_inner_knots + 2)[1:-1]
    inner_knots = R_compat_quantile(x, knot_quantiles)
    knots = np.concatenate(([np.min(x), np.max(x)] * order, inner_knots))
    knots.sort()
    n_bases = len(knots) - (degree + 1)
    basis = np.empty((x.shape[0], n_bases), dtype=float)
    for i in range(n_bases):
        coefs = np.zeros((n_bases,))
        coefs[i] = 1
        basis[:, i] = splev(x, (knots, coefs, degree), der)
    if not include_intercept:
            basis = basis[:, 1:]
    return basis

# create w_hat and vhat for the second stage regression
# option 0: polynomial series
if option == 0:
    w_hat = [endog_var, exog_var]
    for j in range(1, degree+1):
        w_hat.append(np.power(vhat, j))
    w_hat = np.column_stack(w_hat)

# option 1: B-splines
if option == 1:
    vhat_bs_hand = eval_bspline_basis(x=vhat, df=2*degree-1, degree=degree, der=0, include_intercept=False)
    w_hat = np.column_stack([endog_var, exog_var, vhat_bs_hand])

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

### 4. Asymptotic variance

# define a kernal function
# Now, use the Gaussian kernel for simplicity
# TODO: change to other kernal function (or give multiple options)
def kl_normal(x):
    kl = np.exp(-x**2/2)/np.sqrt(2*np.pi)
    return kl

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