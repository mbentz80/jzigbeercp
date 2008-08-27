#!/usr/bin/env python
# Created by John Travers, Robert Hetland, 2007
""" Test functions for rbf module """

from numpy.testing import *
from numpy import linspace, sin, random, exp 

set_package_path()
from rbf.rbf import Rbf
restore_path()

class test_Rbf1D(NumpyTestCase):
    def check_multiquadrics(self):
        x = linspace(0,10,9)
        y = sin(x) 
        rbf = Rbf(x, y)
        yi = rbf(x)
        assert_array_almost_equal(y, yi)

class test_Rbf2D(NumpyTestCase):
    def check_multiquadrics(self):
        x = random.rand(50,1)*4-2
        y = random.rand(50,1)*4-2
        z = x*exp(-x**2-y**2)
        rbf = Rbf(x, y, z ,epsilon=2)
        zi = rbf(x, y)
        zi.shape = x.shape
        assert_array_almost_equal(z, zi)

class test_Rbf3D(NumpyTestCase):
    def check_multiquadrics(self):
        x = random.rand(50,1)*4-2
        y = random.rand(50,1)*4-2
        z = random.rand(50,1)*4-2
        d = x*exp(-x**2-y**2)
        rbf = Rbf(x, y, z, d ,epsilon=2)
        di = rbf(x, y, z)
        di.shape = x.shape
        assert_array_almost_equal(di, d)
    
if __name__ == "__main__":
    NumpyTest().run()
