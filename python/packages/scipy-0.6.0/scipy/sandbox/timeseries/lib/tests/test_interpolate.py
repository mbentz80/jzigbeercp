"""
:author: Pierre Gerard-Marchant & Matt Knox
:contact: pierregm_at_uga_dot_edu & mattknox_ca_at_hotmail_dot_com
:version: $Id: test_interpolate.py 2912 2007-04-12 20:11:53Z mattknox_ca $
"""
__author__ = "Pierre GF Gerard-Marchant & Matt Knox ($Author: mattknox_ca $)"
__version__ = '1.0'
__revision__ = "$Revision: 2912 $"
__date__     = '$Date: 2007-04-12 13:11:53 -0700 (Thu, 12 Apr 2007) $'

import numpy as N
import numpy.core.numeric as numeric

from numpy.testing import NumpyTest, NumpyTestCase

import maskedarray.testutils
from maskedarray.testutils import *

import maskedarray.core as coremodule
from maskedarray.core import MaskedArray, masked

from timeseries.lib.interpolate import backward_fill, forward_fill, interp_masked1d

class test_funcs(NumpyTestCase):
    
    def __init__(self, *args, **kwds):
        NumpyTestCase.__init__(self, *args, **kwds)
        self.mask = [1,0,1,0,0,1,1,0,0,0]
        self.data = numeric.arange(10)
        self.test_array = masked_array(self.data, mask=self.mask)

    def test_backward_fill (self):
        result = masked_array(self.data, mask=self.mask)
        result[0] = 1
        result[2] = 3
       
        assert_equal(backward_fill(self.test_array, maxgap=1), result)
        
        result[5] = 7
        result[6] = 7
        
        assert_equal(backward_fill(self.test_array), result)

    def test_forward_fill (self):
        result = masked_array(self.data, mask=self.mask)
        result[2] = 1
       
        assert_equal(forward_fill(self.test_array, maxgap=1), result)
        
        result[5] = 4
        result[6] = 4
        
        assert_equal(forward_fill(self.test_array), result)

    def test_interp_fill(self):
        result_lin = masked_array(self.data).astype(float_)
        result_lin[0] = masked
        
        approx(interp_masked1d(self.test_array.astype(float_), kind='linear'), result_lin)
        
###############################################################################
#------------------------------------------------------------------------------
if __name__ == "__main__":
    NumpyTest().run()              