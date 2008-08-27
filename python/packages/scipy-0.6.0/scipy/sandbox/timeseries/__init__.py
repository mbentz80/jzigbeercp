"""TimeSeries


__author__ = "Pierre GF Gerard-Marchant  & Matt Knox ($Author: pierregm $)"
__version__ = '1.0'
__revision__ = "$Revision: 2953 $"
__date__     = '$Date: 2007-05-02 07:30:15 -0700 (Wed, 02 May 2007) $'

import tcore
from tcore import *
import tdates
from tdates import *
import tseries
from tseries import *
import tmulti
from tmulti import *
:author: Pierre GF Gerard-Marchant & Matt Knox
:contact: pierregm_at_uga_dot_edu - mattknox_ca_at_hotmail_dot_com
:version: $Id: __init__.py 2953 2007-05-02 14:30:15Z pierregm $
"""


__author__ = "Pierre GF Gerard-Marchant  & Matt Knox ($Author: pierregm $)"
__version__ = '1.0'
__revision__ = "$Revision: 2953 $"
__date__     = '$Date: 2007-05-02 07:30:15 -0700 (Wed, 02 May 2007) $'

# initialize python callbacks for C code
import tcore
from tcore import *
import const
import tdates
from tdates import *
import tseries
from tseries import *
import tmulti
from tmulti import *
import reportlib

from reportlib import *
import lib
from lib import filters, interpolate, moving_funcs


__all__ = ['tdates', 'tseries','tmulti','reportlib','filters','interpolate']
__all__ += tdates.__all__
__all__ += tseries.__all__

__all__ = ['const', 'tdates','tseries','tmulti','reportlib','filters',
           'interpolate', 'moving_funcs']
__all__ += tdates.__all__
__all__ += tseries.__all__
__all__ += tmulti.__all__
__all__ += reportlib.__all__

