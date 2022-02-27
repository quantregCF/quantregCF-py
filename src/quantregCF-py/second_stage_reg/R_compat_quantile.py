def R_compat_quantile(x, probs):
    #return np.percentile(x, 100 * np.asarray(probs))
    probs = np.asarray(probs)
    quantiles = np.asarray([np.percentile(x, 100 * prob) for prob in probs.ravel(order="C")])
    return quantiles.reshape(probs.shape, order="C")
