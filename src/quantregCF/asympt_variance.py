import numpy as np
from .kernel import kl_normal

def asympt_variance(exog_var, z_var, tau_second_stage, w_hat, vhat, second_stage_residual, derivative_lambda):
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

    return se

