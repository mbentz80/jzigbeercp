#!/usr/bin/env python
__author__ = "Pierre GF Gerard-Marchant ($Author: pierregm $)"
__version__ = '1.0'
__revision__ = "$Revision: 2412 $"
__date__     = '$Date: 2006-12-14 16:59:51 -0800 (Thu, 14 Dec 2006) $'

import os

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('maskedarray',parent_package,top_path)
    config.add_data_dir('tests')
    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup
    #setup.update(nmasetup)
    config = configuration(top_path='').todict() 
    setup(**config)
