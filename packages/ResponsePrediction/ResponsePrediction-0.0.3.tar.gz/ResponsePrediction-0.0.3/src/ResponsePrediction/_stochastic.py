import numpy as np


class WaveSpectra():

    def __init__(self, freq):
        self._freq = freq

    def __call__(self, *args, **kwargs):
        raise NotImplementedError
    

class RAO():

    def __init__(self, freq):
        self._freq = freq

    
    def __call__(self, freq):
        raise NotImplementedError


def moment(freqs, spectrum, n=0):
    """Calculate the spectral moment.

    Calculated as:

    ``m_n = \int_0^{\infty}S(\omega)\omega^n d\omega``

    Parameters
    ----------
    freqs : array_like
        Spectrum frequencies.
    spectrum : array_like
        Spectrum to calculate the moment
    n : int
        Order of spectral moment.
    
    Returns
    -------
    m_n : float
        Spectral moment m_n.
    """
    return np.trapz((freqs**n)*spectrum, freqs)


def extreme_response(freqs, spectrum, duration, p=0.99):
    """Calculates the q-th quantile extreme value (assuming Gaussian process).
    
    Parameters
    ----------
    freqs : array_like
        Frequencies in [rad].
    spectrum : array_like
        Spectrum (response spectrum) to be evaluated.
    duration : float
        Duration for which the extreme response should be calculated.
    p : float
        Percentile. Should be a number between 0. and 1.
    
    Returns
    -------
    extreme response : float
        Response.

    q = 0.37 yields the most probable maximum.
    """
    m0 = moment(freqs, spectrum, n=0)
    m2 = moment(freqs, spectrum, n=2)
    tz = 2*np.pi*m0/m2
    return np.sqrt(m0)*np.sqrt(2*np.log((duration/tz) / (np.log(1/p))))