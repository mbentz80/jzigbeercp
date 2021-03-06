#!/usr/bin/env python

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('io', parent_package, top_path)
    config.add_extension('numpyio',
                         sources = ['numpyiomodule.c'])
    config.add_data_dir('tests')
    config.add_data_dir('examples')
    config.add_data_dir('docs')
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
