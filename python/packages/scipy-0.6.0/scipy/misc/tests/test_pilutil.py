from numpy.testing import *
set_package_path()
import PIL.Image
import scipy.misc.pilutil as pilutil
restore_path()

import glob
import os.path
import numpy as N

datapath = os.path.join(os.path.dirname(__file__),'data')

class test_pilutil(NumpyTestCase):
    def test_imresize(self):
        im = N.random.random((10,20))
        for T in N.sctypes['float'] + [float]:
            im1 = pilutil.imresize(im,T(1.1))
            assert_equal(im1.shape,(11,22))

    def test_bytescale(self):
        x = N.array([0,1,2],N.uint8)
        y = N.array([0,1,2])
        assert_equal(pilutil.bytescale(x),x)
        assert_equal(pilutil.bytescale(y),[0,127,255])

    def test_fromimage(self):
        data = {'icon.png':(0,255),
                'icon_mono.png':(0,2),
                'icon_mono_flat.png':(0,1)}

        for fn,irange in data.iteritems():
            img = pilutil.fromimage(PIL.Image.open(os.path.join(datapath,fn)))
            imin,imax = irange
            assert img.min() >= imin
            assert img.max() <= imax

if __name__ == "__main__":
    NumpyTest().run()
