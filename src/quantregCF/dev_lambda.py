from .eval_bspline_basis import eval_bspline_basis

def dev_lambda(exog_var, beta, option, degree, vhat):
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

    return derivative_lambda