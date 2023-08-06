import math
import numpy as np
from scipy.stats import norm
from scipy.linalg import expm

INFEASIBLE = np.inf

def calculate_h_inv(dim):
    a = 1.
    for i in range(10000):
        a -= ((1. + a * a) * math.exp(a * a / 2.) / 0.24 - 10. - dim) / ((2. * a * math.exp(a * a / 2.) + a * (1. + a * a) * math.exp(a * a / 2.)) / 0.24)
    return a

class DXNESICI:
    def __init__(self, dim_co:int, domain_int:np.ndarray, f, m:np.ndarray, sigma:float, lamb:int, margin:float):
        """
        constractor
        """
        self.dim_co = dim_co
        self.dim_int = len(domain_int)
        self.dim = dim_co + self.dim_int
        self.domain_int = domain_int
        self.lim = (domain_int[:,1:] + domain_int[:,:-1])/2.
        self.norm_ci = norm.ppf(1. - margin)

        self.f = f
        self.m = m
        self.sigma = sigma
        self.b = np.eye(self.dim)
        self.p_sigma = np.zeros([self.dim, 1])
        self.lamb = lamb
        self.margin = margin
        self.c_gamma = 1. / (3. * (self.dim - 1.))
        self.d_gamma = min(1., self.dim / lamb)

        self.w_rank_hat = (np.log(self.lamb / 2. + 1.) - np.log(np.arange(1, self.lamb + 1))).reshape(self.lamb, 1)
        self.w_rank_hat[np.where(self.w_rank_hat < 0.)] = 0.
        self.w_rank = self.w_rank_hat / sum(self.w_rank_hat) - (1. / self.lamb)
        self.mu_eff = 1. / ((self.w_rank + (1. / self.lamb)).T @ (self.w_rank + (1. / self.lamb)))[0][0]
        self.c_sigma = ((self.mu_eff + 2.) / (self.dim + self.mu_eff + 5.)) / (2. * np.log(self.dim + 1.))
        self.h_inv = calculate_h_inv(self.dim)
        self.alpha = lambda lambF: self.h_inv * min(1., math.sqrt(self.lamb / self.dim)) * math.sqrt(lambF / self.lamb)
        self.w_dist_hat = lambda zi, lambF: math.exp(self.alpha(lambF) * np.linalg.norm(zi))

        self.state_move = 0
        self.state_stag = 1
        self.state_conv = 2
        self.eta_sigmas = [
            lambda lambF: 1.,
            lambda lambF: math.tanh((0.024 * lambF + 0.7 * self.dim + 20.) / (self.dim + 12.)),
            lambda lambF: 2. * math.tanh((0.025 * lambF + 0.75 * self.dim + 10.) / (self.dim + 4.))
        ]
        self.eta_bs = [
            lambda lambF: 1.5 * 120. * self.dim / (47. * self.dim * self.dim + 6400.) * np.tanh(0.02 * lambF),
            lambda lambF: 1.4 * 120. * self.dim / (47. * self.dim * self.dim + 6400.) * np.tanh(0.02 * lambF),
            lambda lambF: 0.1 * 120. * self.dim / (47. * self.dim * self.dim + 6400.) * np.tanh(0.02 * lambF)
        ]

        self.chiN = np.sqrt(self.dim) * (1. - 1. / (4. * self.dim) + 1. / (21. * self.dim * self.dim))
        self.gamma = np.ones(self.dim)
        self.tau = np.zeros(self.dim)
        self.threshold_over = 5
        self.no_of_over = 0
        self.eye = np.eye(self.dim)

        self.g = 0
        self.no_of_evals = 0
        self.f_best = float('inf')
        self.x_best = np.empty(self.dim)

    def optimize(self, max_generations):
        for _ in range(max_generations):
            print("#Eval:{} f_best:{}".format(self.no_of_evals, self.f_best))
            _ = self.next_generation()
        return self.f_best


    def next_generation(self):
        dim = self.dim
        lamb = self.lamb
        current_bbT = self.b @ self.b.T
        current_m = np.copy(self.m)

        # sampleOffspring
        z_positive = np.random.randn(dim, lamb//2)  # dim x lamb/2
        z = np.zeros([self.dim, self.lamb])
        z[:, :lamb//2] = z_positive
        z[:, lamb//2:] = -z_positive
        x = self.m + self.sigma * self.b @ z
        xbar = np.copy(x)
        for i in range(self.dim_int):
            xbar[i+self.dim_co] = np.array([self.domain_int[i][np.searchsorted(self.lim[i], x[i+self.dim_co][j])] for j in range(self.lamb)])

        evals = np.array([self.f(np.array(xbar[:, i].reshape(self.dim, 1))) for i in range(self.lamb)])
        z = z[:, np.argsort(evals)]
        x = x[:, np.argsort(evals)]
        xbar = xbar[:, np.argsort(evals)]

        self.g += 1
        self.no_of_evals += lamb
        self.f_best = self.f(np.array(xbar[:, 0].reshape(self.dim, 1)))
        lambF = lamb

        # updateEvolutionPath
        self.p_sigma = (1. - self.c_sigma) * self.p_sigma + np.sqrt(self.c_sigma * (2. - self.c_sigma) * self.mu_eff) * (z @ self.w_rank)
        p_sigma_norm = np.linalg.norm(self.p_sigma)
        # determineSearchPhase
        self.no_of_over = self.no_of_over + 1 if p_sigma_norm >= self.chiN else 0
        state = self.state_move if p_sigma_norm >= self.chiN and self.no_of_over >= self.threshold_over else self.state_stag if p_sigma_norm >= 0.1 * self.chiN else self.state_conv
        # calculateWeights
        w_tmp = np.array([self.w_rank_hat[i] * self.w_dist_hat(np.array(z[:, i].reshape(self.dim, 1)), lambF) for i in range(self.lamb)]).reshape(self.lamb, 1) # constractor?
        w_dist = w_tmp / sum(w_tmp) - 1. / self.lamb
        weights = w_dist if state == self.state_move else self.w_rank
        # calculateLearningRate sigma and b
        eta_sigma = self.eta_sigmas[state](lambF)
        eta_b = self.eta_bs[state](lambF)
        # calculateGradients
        grad_M = np.array([weights[i] * (z[:, i].reshape(-1, 1) @ z[:, i].reshape(1, -1) - self.eye) for i in range(self.lamb)]).sum(axis=0) # kousokuka
        grad_sigma = np.trace(grad_M) / self.dim
        grad_b = grad_M - grad_sigma * self.eye
        grad_delta = z @ weights
        # calculateLearningRate m
        eta_mean = np.ones([self.dim, 1])
        ci = (self.norm_ci * self.sigma * np.sqrt(np.diag(current_bbT)))[self.dim_co:].reshape(-1,1)
        ci_up = self.m[self.dim_co:] + ci
        ci_low = self.m[self.dim_co:] - ci
        res = np.array([np.searchsorted(self.lim[i], ci_up[i]) - np.searchsorted(self.lim[i], ci_low[i]) for i in range(self.dim_int)])
        l_close = np.array([self.lim[i][min(self.lim[i].size - 1, max(0, np.searchsorted(self.domain_int[i], self.m[self.dim_co + i]) - 1))] for i in range(self.dim_int)]).reshape(-1,1)
        eta_mean[self.dim_co:][np.where((res <= 1) & (np.sign(grad_delta[self.dim_co:]) == np.sign(self.m[self.dim_co:] - l_close)))] += 1.
        # updateParameters
        self.m += self.sigma * eta_mean * self.b @ grad_delta
        self.sigma *= np.exp((eta_sigma / 2.) * grad_sigma)
        self.b = self.b @ expm((eta_b / 2.) * grad_b)
        # emphasizeExpansion
        if state == self.state_move:
            eig = np.array(np.linalg.eig(current_bbT)[1])
            self.tau = np.sort(np.array([(eig[:, i].T @ self.b @ self.b.T @ eig[:, i]) / (eig[:, i].T @ current_bbT @ eig[:, i]) - 1. for i in range(self.dim)]))
            self.gamma = np.maximum(1., (1. - self.c_gamma) * self.gamma + self.c_gamma * np.sqrt(1. + self.d_gamma * self.tau))
            q = self.eye + (self.gamma[0] - 1.) * np.array([eig[:, i] @ eig[:, i].T for i in range(self.dim) if self.tau[i] > 0.]).sum(axis=0)
            drt_det_q = math.pow(np.linalg.det(q), 1. / self.dim)
            self.sigma *= drt_det_q
            self.b = q @ self.b / drt_det_q
        # leapOrCorrectMean
        ci = (self.norm_ci * self.sigma * np.sqrt(np.diag(self.b @ self.b.T)))[self.dim_co:].reshape(-1,1)
        ci_up = self.m[self.dim_co:] + ci
        ci_low = self.m[self.dim_co:] - ci
        res = np.array([np.searchsorted(self.lim[i], ci_up[i]) - np.searchsorted(self.lim[i], ci_low[i]) for i in range(self.dim_int)])
        for i in range(self.dim_int):
            if res[i] == 0:
                if self.m[self.dim_co + i] <= self.lim[i][0]:
                    self.m[self.dim_co + i] = self.lim[i][0] - ci[i]
                elif self.lim[i][-1] < self.m[self.dim_co + i]:
                    self.m[self.dim_co + i] = self.lim[i][-1] + ci[i]
                elif self.m[self.dim_co + i] <= current_m[self.dim_co + i]:
                    self.m[self.dim_co + i] = self.lim[i][np.searchsorted(self.lim[i], self.m[self.dim_co + i]) - 1] + ci[i]
                else:
                    self.m[self.dim_co + i] = self.lim[i][np.searchsorted(self.lim[i], self.m[self.dim_co + i])] - ci[i]
