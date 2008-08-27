"""
Numpy wrappers for lowess, loess and stl.


:author: Pierre GF Gerard-Marchant
:contact: pierregm_at_uga_edu
:date: $Date: 2007-03-21 15:53:54 -0700 (Wed, 21 Mar 2007) $
:version: $Id: __init__.py 2863 2007-03-21 22:53:54Z pierregm $
"""
__author__ = "Pierre GF Gerard-Marchant"
__version__ = '1.0'
__revision__ = "$Revision: 2863 $"
__date__     = '$Date: 2007-03-21 15:53:54 -0700 (Wed, 21 Mar 2007) $'

import pyloess
from pyloess import lowess, stl, loess, loess_anova