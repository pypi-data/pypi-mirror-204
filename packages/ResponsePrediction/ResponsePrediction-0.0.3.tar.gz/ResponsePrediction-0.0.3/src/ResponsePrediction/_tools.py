# _tools.py

"""General tools for prediction algorithms.

Suggested functionallities
--------------------------

 - Calculation of the PSD
 - Calculation of spectral moments
 - Shallow water dispersion relation

"""

import numpy as np
from scipy.linalg import toeplitz
from scipy.signal import welch

def disp_relation(w, g=9.81, h=2, eps=1e-5, max_iter=5000):
    k_old = w**2/g
    k_new = k_old*np.tanh(k_old*h)
    count = 0
    while (np.abs(k_old - k_new) > eps) and (count < max_iter):
        k_old = k_new
        k_new = k_old*np.tanh(k_old*h)
        count += 1
    return k_new


def psd(timeseries, fs, window=None, nperseg=None, freq_hz=True):
    scale = 2*np.pi
    if nperseg is None:
        n = timeseries.size
        if n >= 2**11:
            nperseg = 2**11
        else:
            nperseg = n // 2
    f, Sx_f = welch(timeseries, fs, window=window, nperseg=nperseg)
    w, Sx_w = f*scale, Sx_f/scale
    return (f, Sx_f) if freq_hz else (w, Sx_w)

def moment(f, Sx_f, moment=0):
    return np.trapz(Sx_f*f**moment, f)

def acf(f, Sx, dt, n, m0):
    Rxx = np.zeros(n)
    N = np.arange(n)
    return 1/m0*np.trapz(Sx*np.cos(f*2*np.pi*N[:, None]*dt), f, axis=1)

def acf_to_acorr_matrix(Rxx):
    return toeplitz(Rxx, np.hstack((Rxx[0], Rxx[1:])))


def pearson_corr_coef(x, x_hat):
    mu_x_hat = np.mean(x_hat)
    mu_x = np.mean(x)
    num = np.sum((x_hat - mu_x_hat)*(x-mu_x))
    denum_1 = np.sqrt(np.sum((x_hat - mu_x_hat)**2))
    denum_2 = np.sqrt(np.sum((x - mu_x)**2))
    return num/(denum_1*denum_2)


def determ_coeff(x, x_hat):
    mu_x = np.mean(x)
    num = np.sum((x_hat - x)**2)
    denum = np.sum((x - mu_x)**2)
    return 1 - num/denum