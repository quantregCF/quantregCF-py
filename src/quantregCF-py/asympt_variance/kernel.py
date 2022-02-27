# TODO: change to other kernal function (or give multiple options)
def kl_normal(x):
    kl = np.exp(-x**2/2)/np.sqrt(2*np.pi)
    return kl
