import numpy as np
from scipy.linalg import toeplitz
import ResponsePrediction._tools as rt

class Autocorrelation():
    """Response prediction using the measured autocorrelation function.
    
    Procedures
    ----------

     1. Calculate the autocorrelation matrix
        - Should be calculated from the PSD using FFT
     2. Calculate the predictive vector
     3. Calculate x_hat(t+k*dT) for t+k*dT < t_max, where t_max
        is the prediction furthest ahead.
        - x_hat(t) = y(t)^T@x
        - y(t)^T = r(t)^T@R^-1
    """

    def __init__(self, x, dt, time_array, dt_pred=None, window="hann", t_future=5):
        self.x = x      # Timeseries (measurement)
        self.dt = dt    # Sampling time
        self.dt_pred = self._check_dt_pred(dt_pred) # Sampling time for pred.
        self.fs = 1/dt  # Sampling frequency
        self.time = time_array  # Time array
        self.t_future=t_future
        self.m = int(self.t_future/self.dt_pred)
        if x.size != time_array.size:
            raise ValueError(f"x and time_array must have same dimensions.")

        self.f, self._Sx = rt.psd(x, fs=self.fs, window=window, nperseg=2**11)
        self.m0 = rt.moment(self.f, self.Sx, moment=0)
        self.x_m = 0
        self.x_hat = 0
        self.x_pred = np.zeros(int(self.t_future/self.dt_pred))
        self.t_pred = np.linspace(0, t_future, self.m)
        # Rxx = rt.acf(self.f, self.Sx, self.dt, 1000, self.m0)
        # self._R = rt.acf_to_acorr_matrix(Rxx)
        # self.omega = self.f*2*np.pi
        # self.x_hat = np.zeros(1)

    @property
    def Sx(self):
        return self._Sx
    
    @property
    def R(self):
        return self._R
    
    @property
    def Y(self):
        return self._Y
    
    @property
    def x_m(self):
        return self._x_m
    
    @x_m.setter
    def x_m(self, x):
        self._x_m = x

    def init(self, n, dt_m):
        self.n = n
        self.dt_m = dt_m
        self.set_R()


    def measurement(self, t, x):
        if t[1] > t[0]:
            t = t[::-1]
            x = x[::-1]
        if x.size != self.n:
            raise ValueError(f"x has size {x.size}, which is different to n {self.n}")
        self.n = x.size
        self.x_m = x
        self.t_m = t
        self.dt_m = t[0] - t[1]
        if self.dt_m < 0:
            raise ValueError(f"Timestep is negative: {self.dt_m}")
    
    def set_R(self):
        # This should only be calculated once, and 
        # therefore we must define the variables used
        # here earlier in the process.
        self.Rxx = rt.acf(
            self.f,
            self.Sx,
            self.dt_m,
            self.n,
            self.m0
        )
        self._R = rt.acf_to_acorr_matrix(self.Rxx)
        self._Rinv = np.linalg.pinv(self._R)
        self.set_prediction_vector()


    def y_m(self, m):
        N = np.arange(self.n)
        r = 1/self.m0 * np.trapz(
            self.Sx*np.cos(2*np.pi*self.f*(m*self.dt_pred + N[:, None]*self.dt_m)),
            x=self.f,
            axis=1
        )
        return r.T@self._Rinv

    def set_prediction_vector(self):
        Y = np.zeros((self.m, self.n))
        for m in range(self.m):
            Y[m] = self.y_m(m)
        self._Y = Y

    def predict(self):
        self.x_hat = self.Y @ self.x_m


    def _check_dt_pred(self, dt_pred):
        if dt_pred is not None and (dt_pred < self.dt):
            print(f"Prediction timestep is less than measurement.")
            print(f"Measurement timestep = {self.dt}, pred. timestep = {dt_pred}")
            raise ValueError(f"dt: {self.dt} !< dt_pred: {dt_pred}")
        elif dt_pred is None:
            dt_pred = self.dt
        return dt_pred

    def __repr__(self) -> str:
        return f"NOT IMPLEMENTED."    


class PRWR():
    """
    Phase-Resolved wave reconstruction (PRWR).

    Use the FFT to obtain the individual wave components of a measured wave elevation. The 
    wave elevation at a location x can be estimated from these wave components by using
    the dispersion relation. The wave elevation should be estimated at a location downwave.
    Whether the prediction is possible or not can be determined from the predictable zone.

    The prediction algorithm uses the linear dispersion relation.

    Attributes
    ----------
    t_pred : array_like
        The time instances where we want to estimate the wave elevation.
    t0 : float
        The start point of measurement
    beta : float
        The wave direction. It is defined in the North-East-Down frame as waves going to.
        beta = 0.0 corresponds to waves coming from south moving north, and beta=pi the opposit.
    g : float
        Gravitational acceleration.
    """
    def __init__(self, t0, t_pred, wavedir):
        self.t0 = t0
        self.t_pred = t_pred
        self.beta = wavedir
        self.g = 9.81

    def __call__(self, wave_measurement, fs=100, x=0):
        """Calculate an estimate of the wave elevation at a point x based on a measurement
        of the wave elevation."""
        self._wave_reconstruction(wave_measurement, fs)
        return np.sum(np.real(self.amp*np.cos(self.w*self.t_pred[:, None] - self.k*np.cos(self.beta)*x)), axis=1)

    def _wave_reconstruction(self, wave_measurement, fs=100):
        # Use the FFT to obtain the phase-resolved wave
        zeta_hat = np.fft.rfft(wave_measurement)
        f_hat = np.fft.rfftfreq(n=wave_measurement.size, d=1/fs)
        self.w = f_hat*2*np.pi
        self.k = self.w**2/self.g
        self.amp = zeta_hat