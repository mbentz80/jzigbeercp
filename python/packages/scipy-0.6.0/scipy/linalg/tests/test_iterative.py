#!/usr/bin/env python
#
# Created by: Ed Schofield, Jan 2007
#
""" Test functions for the linalg.iterative module
"""
__usage__ = """
Build linalg:
  python setup_linalg.py build
Run tests if scipy is installed:
  python -c 'import scipy;scipy.linalg.test(<level>)'
Run tests if linalg is not installed:
  python tests/test_iterative.py [<level>]
"""

from numpy import zeros, dot, diag, ones
from numpy.testing import *
from numpy.random import rand
#from numpy import arange, add, array, dot, zeros, identity, conjugate, transpose

import sys
set_package_path()
from linalg import iterative, norm, cg, cgs, bicg, bicgstab, gmres, qmr
restore_path()


def callback(x):
    global A, b
    res = b-dot(A,x)
    #print "||A.x - b|| = " + str(norm(dot(A,x)-b))

class test_iterative_solvers(NumpyTestCase):
    def __init__(self, *args, **kwds):
        NumpyTestCase.__init__(self, *args, **kwds)
        self.setUp()
    def setUp (self):
        global A, b
        n = 10
        self.tol = 1e-5
        self.x0 = zeros(n, float)
        A = rand(n, n)+diag(4*ones(n))
        self.A = 0.5 * (A+A.T)
        A = self.A
        self.b = rand(n)
        b = self.b

    def check_cg(self):
        bx0 = self.x0.copy()
        x, info = cg(self.A, self.b, self.x0, callback=callback)
        assert_array_equal(bx0, self.x0)
        assert norm(dot(self.A, x) - self.b) < 5*self.tol

    def check_bicg(self):
        bx0 = self.x0.copy()
        x, info = bicg(self.A, self.b, self.x0, callback=callback)
        assert_array_equal(bx0, self.x0)
        assert norm(dot(self.A, x) - self.b) < 5*self.tol

    def check_cgs(self):
        bx0 = self.x0.copy()
        x, info = cgs(self.A, self.b, self.x0, callback=callback)
        assert_array_equal(bx0, self.x0)
        assert norm(dot(self.A, x) - self.b) < 5*self.tol

    def check_bicgstab(self):
        bx0 = self.x0.copy()
        x, info = bicgstab(self.A, self.b, self.x0, callback=callback)
        assert_array_equal(bx0, self.x0)
        assert norm(dot(self.A, x) - self.b) < 5*self.tol

    def check_gmres(self):
        bx0 = self.x0.copy()
        x, info = gmres(self.A, self.b, self.x0, callback=callback)
        assert_array_equal(bx0, self.x0)
        assert norm(dot(self.A, x) - self.b) < 5*self.tol

    def check_qmr(self):
        bx0 = self.x0.copy()
        x, info = qmr(self.A, self.b, self.x0, callback=callback)
        assert_array_equal(bx0, self.x0)
        assert norm(dot(self.A, x) - self.b) < 5*self.tol

if __name__ == "__main__":
    NumpyTest().run()

