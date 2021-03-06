#! /usr/bin/env python

# David Cournapeau
# Last Change: Tue Jul 03 08:00 PM 2007 J

# For now, just copy the tests from sandbox.pyem, so we can check that
# kmeans works OK for trivial examples.

import sys
from numpy.testing import *

import numpy as N

set_package_path()
from cluster.vq import kmeans, kmeans2, py_vq, py_vq2, _py_vq_1d, vq, ClusterError
try:
    from cluster import _vq
    TESTC=True
except ImportError:
    print "== Error while importing _vq, not testing C imp of vq =="
    TESTC=False
restore_path()

import os.path
#Optional:
set_local_path()
# import modules that are located in the same directory as this file.
DATAFILE1 = os.path.join(sys.path[0], "data.txt")
restore_path()

# Global data
X   = N.array([[3.0, 3], [4, 3], [4, 2],
               [9, 2], [5, 1], [6, 2], [9, 4],
               [5, 2], [5, 4], [7, 4], [6, 5]])

CODET1  = N.array([[3.0000, 3.0000],
                   [6.2000, 4.0000],
                   [5.8000, 1.8000]])

CODET2  = N.array([[11.0/3, 8.0/3],
                   [6.7500, 4.2500],
                   [6.2500, 1.7500]])

LABEL1  = N.array([0, 1, 2, 2, 2, 2, 1, 2, 1, 1, 1])

class test_vq(NumpyTestCase):
    def check_py_vq(self, level=1):
        initc = N.concatenate(([[X[0]], [X[1]], [X[2]]]))
        code = initc.copy()
        label1 = py_vq(X, initc)[0]
        assert_array_equal(label1, LABEL1)

    def check_py_vq2(self, level=1):
        initc = N.concatenate(([[X[0]], [X[1]], [X[2]]]))
        code = initc.copy()
        label1 = py_vq2(X, initc)[0]
        assert_array_equal(label1, LABEL1)

    def check_vq(self, level=1):
        initc = N.concatenate(([[X[0]], [X[1]], [X[2]]]))
        code = initc.copy()
        if TESTC:
            label1, dist = _vq.vq(X, initc)
            assert_array_equal(label1, LABEL1)
            tlabel1, tdist = vq(X, initc)
        else:
            print "== not testing C imp of vq =="

    #def check_py_vq_1d(self, level=1):
    #    """Test special rank 1 vq algo, python implementation."""
    #    data = X[:, 0]
    #    initc = data[:3]
    #    code = initc.copy()
    #    a, b = _py_vq_1d(data, initc)
    #    ta, tb = py_vq(data[:, N.newaxis], initc[:, N.newaxis])
    #    assert_array_equal(a, ta)
    #    assert_array_equal(b, tb)

    def check_vq_1d(self, level=1):
        """Test special rank 1 vq algo, python implementation."""
        data = X[:, 0]
        initc = data[:3]
        code = initc.copy()
        if TESTC:
            a, b = _vq.vq(data, initc)
            ta, tb = py_vq(data[:, N.newaxis], initc[:, N.newaxis])
            assert_array_equal(a, ta)
            assert_array_equal(b, tb)
        else:
            print "== not testing C imp of vq (rank 1) =="

class test_kmean(NumpyTestCase):
    def check_kmeans_simple(self, level=1):
        initc = N.concatenate(([[X[0]], [X[1]], [X[2]]]))
        code = initc.copy()
        code1 = kmeans(X, code, iter = 1)[0]

        assert_array_almost_equal(code1, CODET2)

    def check_kmeans_lost_cluster(self, level=1):
        """This will cause kmean to have a cluster with no points."""
        data = N.fromfile(open(DATAFILE1), sep = ", ")
        data = data.reshape((200, 2))
        initk = N.array([[-1.8127404, -0.67128041],
                         [ 2.04621601, 0.07401111],
                         [-2.31149087,-0.05160469]])

        res = kmeans(data, initk)
        res = kmeans2(data, initk, missing = 'warn')
        try :
            res = kmeans2(data, initk, missing = 'raise')
            raise AssertionError("Exception not raised ! Should not happen")
        except ClusterError, e:
            print "exception raised as expected: " + str(e)

    def check_kmeans2_simple(self, level=1):
        """Testing simple call to kmeans2 and its results."""
        initc = N.concatenate(([[X[0]], [X[1]], [X[2]]]))
        code = initc.copy()
        code1 = kmeans2(X, code, iter = 1)[0]
        code2 = kmeans2(X, code, iter = 2)[0]

        assert_array_almost_equal(code1, CODET1)
        assert_array_almost_equal(code2, CODET2)

    def check_kmeans2_rank1(self, level=1):
        """Testing simple call to kmeans2 with rank 1 data."""
        data = N.fromfile(open(DATAFILE1), sep = ", ")
        data = data.reshape((200, 2))
        data1 = data[:, 0]
        data2 = data[:, 1]

        initc = data1[:3]
        code = initc.copy()
        code1 = kmeans2(data1, code, iter = 1)[0]
        code2 = kmeans2(data1, code, iter = 2)[0]

    def check_kmeans2_init(self, level = 1):
        """Testing that kmeans2 init methods work."""
        data = N.fromfile(open(DATAFILE1), sep = ", ")
        data = data.reshape((200, 2))

        kmeans2(data, 3, minit = 'random')
        kmeans2(data, 3, minit = 'points')

        # Check special case 1d
        data = data[:, :1]
        kmeans2(data, 3, minit = 'random')
        kmeans2(data, 3, minit = 'points')

if __name__ == "__main__":
    NumpyTest().run()
