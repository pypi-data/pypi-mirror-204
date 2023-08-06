"""
ResponsePrediction
==================

Response prediction algorihms for wave-induced vessel motions.

Contents
--------

 - TBD

Description
-----------

 - TBD

Examples
--------

 - TBD

References
----------
 - TBD
"""

from ._deterministic import Autocorrelation
from ._tools import (
    psd,
    moment,
    pearson_corr_coef,
    determ_coeff,
    acf,
    acf_to_acorr_matrix,
    disp_relation
)

from ._stochastic import (
    WaveSpectra,
    RAO
)

__version__ = "0.0.3"