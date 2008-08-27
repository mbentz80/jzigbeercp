"""

A collection of filters for timeseries

:author: Pierre GF Gerard-Marchant & Matt Knox
:contact: pierregm_at_uga_dot_edu - mattknox_ca_at_hotmail_dot_com
:version: $Id: filters.py 2906 2007-04-12 14:13:39Z mattknox_ca $
"""
__author__ = "Pierre GF Gerard-Marchant & Matt Knox ($Author: mattknox_ca $)"
__version__ = '1.0'
__revision__ = "$Revision: 2906 $"
__date__     = '$Date: 2007-04-12 07:13:39 -0700 (Thu, 12 Apr 2007) $'

import numpy as N
from numpy import bool_, float_
narray = N.array

from scipy.signal import convolve, get_window

import maskedarray as MA
from maskedarray import MaskedArray, nomask, getmask, getmaskarray, masked
marray = MA.array

from moving_funcs import mov_average_expw, cmov_average, cmov_mean, \
                         cmov_window

__all__ = ['mov_average_expw'
           'cmov_average', 'cmov_mean', 'cmov_window']
