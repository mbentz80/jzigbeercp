"""Masked arrays add-ons.

A collection of utilities for maskedarray

:author: Pierre GF Gerard-Marchant
:contact: pierregm_at_uga_dot_edu
:version: $Id: __init__.py 2773 2007-02-27 21:41:19Z pierregm $
"""
__author__ = "Pierre GF Gerard-Marchant ($Author: pierregm $)"
__version__ = '1.0'
__revision__ = "$Revision: 2773 $"
__date__     = '$Date: 2007-02-27 13:41:19 -0800 (Tue, 27 Feb 2007) $'

import core
from core import *

import extras
from extras import *


__all__ = ['core', 'extras']
__all__ += core.__all__
__all__ += extras.__all__