#!/usr/bin/env python
__version__ = '1.0'
__revision__ = "$Revision: 2977 $"
__date__     = '$Date: 2007-05-09 10:10:27 -0700 (Wed, 09 May 2007) $'

import os
from os.path import join

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs
    nxheader = join(get_numpy_include_dirs()[0],'numpy',)
    confgr = Configuration('timeseries',parent_package,top_path)
    sources = [join('src', x) for x in ('c_lib.c',
                                        'c_tdates.c',
                                        'c_tseries.c',
                                        'cseries.c')]
    confgr.add_extension('cseries',
                         sources=sources,
                         include_dirs=[nxheader, 'include'])

    confgr.add_subpackage('lib')
    confgr.add_subpackage('io')
    confgr.add_subpackage('plotlib')
    confgr.add_subpackage('tests')
    return confgr

if __name__ == "__main__":
    from numpy.distutils.core import setup
    #setup.update(nmasetup)
    config = configuration(top_path='').todict()
    setup(**config)