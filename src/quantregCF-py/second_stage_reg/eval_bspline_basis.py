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
