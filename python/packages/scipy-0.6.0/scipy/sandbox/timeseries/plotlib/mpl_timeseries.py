"""
Classes to plot TimeSeries w/ matplotlib.

:author: Pierre GF Gerard-Marchant & Matt Knox
:contact: pierregm_at_uga_dot_edu - mattknow_ca_at_hotmail_dot_com
:date: $Date: 2007-07-18 20:52:17 -0700 (Wed, 18 Jul 2007) $
:version: $Id: mpl_timeseries.py 3175 2007-07-19 03:52:17Z pierregm $
"""
__author__ = "Pierre GF Gerard-Marchant & Matt Knox ($Author: pierregm $)"
__version__ = '1.0'
__revision__ = "$Revision: 3175 $"
__date__     = '$Date: 2007-07-18 20:52:17 -0700 (Wed, 18 Jul 2007) $'


import matplotlib
from matplotlib import pylab, rcParams
from matplotlib import _pylab_helpers
from matplotlib.artist import setp
from matplotlib.axes import Subplot, PolarSubplot
from matplotlib.cbook import flatten
from matplotlib.collections import LineCollection
from matplotlib.contour import ContourSet
from matplotlib.dates import DayLocator, MonthLocator, YearLocator, \
                             DateFormatter
from matplotlib.figure import Figure
from matplotlib.legend import Legend
from matplotlib.mlab import meshgrid
from matplotlib.ticker import Formatter, ScalarFormatter, FuncFormatter, \
                              Locator, FixedLocator
#from matplotlib.transforms import nonsingular

import numpy
import maskedarray as MA

import timeseries
from timeseries import date_array, Date, DateArray, TimeSeries, get_freq_group
from timeseries import const as _c

import warnings

#####---------------------------------------------------------------------------
#---- --- Matplotlib extensions ---
#####---------------------------------------------------------------------------

def add_generic_subplot(figure_instance, *args, **kwargs):
    """Generalizes the `add_subplot` figure method to generic subplots.
The specific Subplot object class to add is given through the keywords
`SubplotClass` or `class`.

:Parameters:
    `figure_instance` : Figure object
        Figure to which the generic subplot should be attached.
    `args` : Misc
        Miscellaneous arguments to the subplot.
    `kwargs` : Dictionary
        Keywords. Same keywords as `Subplot`, with the addition of
        - `SubplotClass` : Type of subplot
        - `subclass` : Shortcut to `SubplotClass`.
        - any keyword required by the `SubplotClass` subclass.
    """

    key = figure_instance._make_key(*args, **kwargs)
    #TODO: Find why, sometimes, key is not hashable (even if tuple)
    # else, there's a fix below
    try:
        key.__hash__()
    except TypeError:
        key = str(key)
    #
    if figure_instance._seen.has_key(key):
        ax = figure_instance._seen[key]
        figure_instance.sca(ax)
        return ax
    #
    if not len(args):
        return
#    if hasattr(args[0], '__array__'):
#        fixedargs = args[1:]
#    else:
#        fixedargs = args
    #
    SubplotClass = kwargs.pop("SubplotClass", Subplot)
    SubplotClass = kwargs.pop("subclass",SubplotClass)
    if isinstance(args[0], Subplot) or isinstance(args[0], PolarSubplot):
        a = args[0]
        assert(a.get_figure() is figure_instance)
#        a.set_figure(figure_instance)
    else:
        ispolar = kwargs.pop('polar', False)
        if ispolar:
            a = PolarSubplot(figure_instance, *args, **kwargs)
        else:
            a = SubplotClass(figure_instance, *args, **kwargs)

    figure_instance.axes.append(a)
    figure_instance._axstack.push(a)
    figure_instance.sca(a)
    figure_instance._seen[key] = a
    return a


def nonsingular(vmin, vmax, expander=0.001, tiny=1e-15, increasing=True):
    '''
    Ensure the endpoints of a range are not too close together.

    "too close" means the interval is smaller than 'tiny' times
            the maximum absolute value.

    If they are too close, each will be moved by the 'expander'.
    If 'increasing' is True and vmin > vmax, they will be swapped.
    '''
    #TODO: Remove that when matplotlib incorporate it by default
    swapped = False
    if vmax < vmin:
        vmin, vmax = vmax, vmin
        swapped = True
    if vmax - vmin <= max(abs(vmin), abs(vmax)) * tiny:
        if vmin == 0.0:
            vmin = -expander
            vmax = expander
        else:
            vmin -= expander*abs(vmin)
            vmax += expander*abs(vmax)
    if swapped and not increasing:
        vmin, vmax = vmax, vmin
    return vmin, vmax

##### -------------------------------------------------------------------------
#---- --- Locators ---
##### -------------------------------------------------------------------------

def _get_default_annual_spacing(nyears):
    """Returns a default spacing between consecutive ticks for annual data."""
    if nyears < 11:
        (min_spacing, maj_spacing) = (1, 1)
    elif nyears < 20:
        (min_spacing, maj_spacing) = (1, 2)
    elif nyears < 50:
        (min_spacing, maj_spacing) = (1, 5)
    elif nyears < 100:
        (min_spacing, maj_spacing) = (5, 10)
    elif nyears < 200:
        (min_spacing, maj_spacing) = (5, 25)
    elif nyears < 600:
        (min_spacing, maj_spacing) = (10, 50)
    else:
        factor = nyears // 1000 + 1
        (min_spacing, maj_spacing) = (factor*20, factor*100)
    return (min_spacing, maj_spacing)


def period_break(dates, period):
    """Returns the indices where the given period changes.

:Parameters:
    dates : DateArray
        Array of dates to monitor.
    period : string
        Name of the period to monitor.
    """
    current = getattr(dates, period)
    previous = getattr(dates-1, period)
    return (current - previous).nonzero()[0]

def has_level_label(label_flags):
    """returns true if the label_flags indicate there is at least
one label for this level"""
    if label_flags.size == 0 or \
       (label_flags.size == 1 and label_flags[0] == 0):
        return False
    else:
        return True

def _daily_finder(vmin, vmax, freq, aslocator):

    if freq == _c.FR_BUS:
        periodsperyear = 261
        periodspermonth = 19
    elif freq == _c.FR_DAY:
        periodsperyear = 365
        periodspermonth = 28
    elif get_freq_group(freq) == _c.FR_WK:
        periodsperyear = 52
        periodspermonth = 3
    else:
        raise ValueError("unexpected frequency")

    (vmin, vmax) = (int(vmin), int(vmax))
    span = vmax - vmin + 1
    dates = date_array(start_date=Date(freq,vmin),
                       end_date=Date(freq, vmax))
    default = numpy.arange(vmin, vmax+1)
    # Initialize the output
    if not aslocator:
        format = numpy.empty(default.shape, dtype="|S10")
        format.flat = ''

    def first_label(label_flags):
        if label_flags[0] == 0: return label_flags[1]
        else: return label_flags[0]

    # Case 1. Less than a month
    if span <= periodspermonth:
        month_start = period_break(dates,'month')
        if aslocator:
            major = default[month_start]
            minor = default
        else:
            year_start = period_break(dates,'year')
            format[:] = '%d'
            format[month_start] = '%d\n%b'
            format[year_start] = '%d\n%b\n%Y'
            if not has_level_label(year_start):
                if not has_level_label(month_start):
                    if dates.size > 1:
                        idx = 1
                    else:
                        idx = 0
                    format[idx] = '%d\n%b\n%Y'
                else:
                    format[first_label(month_start)] = '%d\n%b\n%Y'
    # Case 2. Less than three months
    elif span <= periodsperyear//4:
        month_start = period_break(dates,'month')
        if aslocator:
            major = default[month_start]
            minor = default
        else:
            week_start = period_break(dates,'week')
            year_start = period_break(dates,'year')

            format[week_start] = '%d'
            format[month_start] = '\n\n%b'
            format[year_start] = '\n\n%b\n%Y'
            if not has_level_label(year_start):
                if not has_level_label(month_start):
                    format[first_label(week_start)] = '\n\n%b\n%Y'
                else:
                    format[first_label(month_start)] = '\n\n%b\n%Y'
    # Case 3. Less than 14 months ...............
    elif span <= 1.15 * periodsperyear:

        if aslocator:
            d_minus_1 = dates-1

            month_diff = numpy.abs(dates.month - d_minus_1.month)
            week_diff = numpy.abs(dates.week - d_minus_1.week)
            minor_idx = (month_diff + week_diff).nonzero()[0]

            major = default[month_diff != 0]
            minor = default[minor_idx]
        else:
            year_start = period_break(dates,'year')
            month_start = period_break(dates,'month')

            format[month_start] = '%b'
            format[year_start] = '%b\n%Y'
            if not has_level_label(year_start):
                format[first_label(month_start)] = '%b\n%Y'
    # Case 4. Less than 2.5 years ...............
    elif span <= 2.5 * periodsperyear:
        year_start = period_break(dates,'year')
        if aslocator:
            month_start = period_break(dates, 'quarter')
            major = default[year_start]
            minor = default[month_start]
        else:
            quarter_start = period_break(dates, 'quarter')
            format[quarter_start] = '%b'
            format[year_start] = '%b\n%Y'
    # Case 4. Less than 4 years .................
    elif span <= 4 * periodsperyear:
        year_start = period_break(dates,'year')
        month_start = period_break(dates, 'month')
        if aslocator:
            major = default[year_start]
            minor = default[month_start]
        else:
            month_break = dates[month_start].month
            jan_or_jul = month_start[(month_break == 1) | (month_break == 7)]
            format[jan_or_jul] = '%b'
            format[year_start] = '%b\n%Y'
    # Case 5. Less than 11 years ................
    elif span <= 11 * periodsperyear:
        year_start = period_break(dates,'year')
        if aslocator:
            quarter_start = period_break(dates, 'quarter')
            major = default[year_start]
            minor = default[quarter_start]
        else:
            format[year_start] = '%Y'
    # Case 6. More than 12 years ................
    else:
        year_start = period_break(dates,'year')
        year_break = dates[year_start].years
        nyears = span/periodsperyear
        (min_anndef, maj_anndef) = _get_default_annual_spacing(nyears)
        major_idx = year_start[(year_break % maj_anndef == 0)]
        if aslocator:
            major = default[major_idx]
            minor_idx = year_start[(year_break % min_anndef == 0)]
            minor = default[minor_idx]
        else:
            format[major_idx] = '%Y'
    #............................................
    if aslocator:
        return minor, major
    else:
        formatted = (format != '')
        return dict([(d,f) for (d,f) in zip(default[formatted],format[formatted])])
#...............................................................................
def _monthly_finder(vmin, vmax, freq, aslocator):
    if freq != _c.FR_MTH:
        raise ValueError("Unexpected frequency")
    periodsperyear = 12

    (vmin, vmax) = (int(vmin), int(vmax))
    span = vmax - vmin + 1
    #............................................
    dates = numpy.arange(vmin, vmax+1)
    format = numpy.empty(span, dtype="|S8")
    format.flat = ''
    year_start = (dates % 12 == 1).nonzero()[0]
    #............................................
    if span <= 1.15 * periodsperyear:
        if aslocator:
            major = dates[year_start]
            minor = dates
        else:

            format[:] = '%b'
            format[year_start] = '%b\n%Y'

            if not has_level_label(year_start):
                if dates.size > 1:
                    idx = 1
                else:
                    idx = 0
                format[idx] = '%b\n%Y'
    #........................
    elif span <= 2.5 * periodsperyear:
        if aslocator:
            major = dates[year_start]
            minor = dates
        else:
            quarter_start = (dates % 3 == 1).nonzero()
            format[quarter_start] = '%b'
            format[year_start] = '%b\n%Y'
    #.......................
    elif span <= 4 * periodsperyear:
        if aslocator:
            major = dates[year_start]
            minor = dates
        else:
            jan_or_jul = (dates % 12 == 1) | (dates % 12 == 7)
            format[jan_or_jul] = '%b'
            format[year_start] = '%b\n%Y'
    #........................
    elif span <= 11 * periodsperyear:
        if aslocator:
            quarter_start = (dates % 3 == 1).nonzero()
            major = dates[year_start]
            minor = dates[quarter_start]
        else:
            format[year_start] = '%Y'
   #.........................
    else:
        nyears = span/periodsperyear
        (min_anndef, maj_anndef) = _get_default_annual_spacing(nyears)
        years = dates[year_start]//12 + 1
        major_idx = year_start[(years % maj_anndef == 0)]
        if aslocator:
            major = dates[major_idx]
            minor = dates[year_start[(years % min_anndef == 0)]]
        else:
            format[major_idx] = '%Y'
    #........................
    if aslocator:
        return minor, major
    else:
        formatted = (format != '')
        return dict([(d,f) for (d,f) in zip(dates[formatted],format[formatted])])
#...............................................................................
def _quarterly_finder(vmin, vmax, freq, aslocator):
    if get_freq_group(freq) != _c.FR_QTR:
        raise ValueError("Unexpected frequency")
    periodsperyear = 4
    (vmin, vmax) = (int(vmin), int(vmax))
    span = vmax - vmin + 1
    #............................................
    dates = numpy.arange(vmin, vmax+1)
    format = numpy.empty(span, dtype="|S8")
    format.flat = ''
    year_start = (dates % 4 == 1).nonzero()[0]
    #............................................
    if span <= 3.5 * periodsperyear:
        if aslocator:
            major = dates[year_start]
            minor = dates
        else:
            format[:] = 'Q%q'
            format[year_start] = 'Q%q\n%F'
            if not has_level_label(year_start):
                if dates.size > 1:
                    idx = 1
                else:
                    idx = 0
                format[idx] = 'Q%q\n%F'
    #............................................
    elif span <= 11 * periodsperyear:
        if aslocator:
            major = dates[year_start]
            minor = dates
        else:
            format[year_start] = '%F'
    #............................................
    else:
        years = dates[year_start]//4 + 1
        nyears = span/periodsperyear
        (min_anndef, maj_anndef) = _get_default_annual_spacing(nyears)
        major_idx = year_start[(years % maj_anndef == 0)]
        if aslocator:
            major = dates[major_idx]
            minor = dates[year_start[(years % min_anndef == 0)]]
        else:
            format[major_idx] = '%F'
    #............................................
    if aslocator:
        return minor, major
    else:
        formatted = (format != '')
        return dict([(d,f) for (d,f) in zip(dates[formatted],format[formatted])])
#...............................................................................
def _annual_finder(vmin, vmax, freq, aslocator):
    if get_freq_group(freq) != _c.FR_ANN:
        raise ValueError("Unexpected frequency")
    (vmin, vmax) = (int(vmin), int(vmax+1))
    span = vmax - vmin + 1
    #............................................
    dates = numpy.arange(vmin, vmax+1)
    format = numpy.empty(span, dtype="|S8")
    format.flat = ''
    #............................................
    (min_anndef, maj_anndef) = _get_default_annual_spacing(span)
    major_idx = dates % maj_anndef == 0
    if aslocator:
        major = dates[major_idx]
        minor = dates[(dates % min_anndef == 0)]
    else:
        format[major_idx] = '%Y'
    #............................................
    if aslocator:
        return minor, major
    else:
        formatted = (format != '')
        return dict([(d,f) for (d,f) in zip(dates[formatted],format[formatted])])

#...............................................................................
class TimeSeries_DateLocator(Locator):
    "Locates the ticks along an axis controlled by a DateArray."

    def __init__(self, freq, minor_locator=False, dynamic_mode=True,
                 base=1, quarter=1, month=1, day=1):
        self.freq = freq
        self.base = base
        fgroup = get_freq_group(freq)
        (self.quarter, self.month, self.day) = (quarter, month, day)
        self.isminor = minor_locator
        self.isdynamic = dynamic_mode
        self.offset = 0
        #.....
        if fgroup == _c.FR_ANN:
            self.finder = _annual_finder
        elif fgroup == _c.FR_QTR:
            self.finder = _quarterly_finder
        elif freq == _c.FR_MTH:
            self.finder = _monthly_finder
        elif freq in (_c.FR_BUS, _c.FR_DAY) or fgroup == _c.FR_WK:
            self.finder = _daily_finder

    def asminor(self):
        "Returns the locator set to minor mode."
        self.isminor = True
        return self

    def asmajor(self):
        "Returns the locator set to major mode."
        self.isminor = False
        return self

    def _get_default_locs(self, vmin, vmax):
        "Returns the default locations of ticks."
        (minor, major) = self.finder(vmin, vmax, self.freq, True)
        if self.isminor:
            return minor
        return major

    def __call__(self):
        'Return the locations of the ticks.'
        self.verify_intervals()
        vmin, vmax = self.viewInterval.get_bounds()
        if vmax < vmin:
            vmin, vmax = vmax, vmin
        if self.isdynamic:
            locs = self._get_default_locs(vmin, vmax)
        else:
            base = self.base
            (d, m) = divmod(vmin, base)
            vmin = (d+1) * base
            locs = range(vmin, vmax+1, base)
        return locs

    def autoscale(self):
        """Sets the view limits to the nearest multiples of base that contain
    the data.
        """
        self.verify_intervals()
        dmin, dmax = self.dataInterval.get_bounds()
        locs = self._get_default_locs(dmin, dmax)
        (vmin, vmax) = locs[[0, -1]]
        if vmin == vmax:
            vmin -= 1
            vmax += 1
        return nonsingular(vmin, vmax)

#####---------------------------------------------------------------------------
#---- --- Formatter ---
#####---------------------------------------------------------------------------
class TimeSeries_DateFormatter(Formatter):
    """Formats the ticks along a DateArray axis."""

    def __init__(self, freq, minor_locator=False, dynamic_mode=True,):
        self.format = None
        self.freq = freq
        self.locs = []
        self.formatdict = {}
        self.isminor = minor_locator
        self.isdynamic = dynamic_mode
        self.offset = 0
        fgroup = get_freq_group(freq)
        #.....
        if fgroup == _c.FR_ANN:
            self.finder = _annual_finder
        elif fgroup == _c.FR_QTR:
            self.finder = _quarterly_finder
        elif freq == _c.FR_MTH:
            self.finder = _monthly_finder
        elif freq in (_c.FR_BUS, _c.FR_DAY) or fgroup == _c.FR_WK:
            self.finder = _daily_finder

    def asminor(self):
        "Returns the formatter set to minor mode."
        self.isminor = True
        return self

    def asmajor(self):
        "Returns the fromatter set to major mode."
        self.isminor = False
        return self

    def _set_default_format(self, vmin, vmax):
        "Returns the default ticks spacing."
        self.formatdict = self.finder(vmin, vmax, self.freq, False)
        return self.formatdict

    def set_locs(self, locs):
        'Sets the locations of the ticks'
        self.locs = locs
        if len(self.locs) > 0:
            self.verify_intervals()
            self._set_default_format(locs[0], locs[-1])
    #
    def __call__(self, x, pos=0):
        if self.isminor:
            fmt = self.formatdict.pop(x, '')
            if fmt is not '':
                retval = Date(self.freq, value=int(x)).strfmt(fmt)
            else:
                retval = ''
        else:
            retval = ''
        return retval




#####--------------------------------------------------------------------------
#---- --- TimeSeries plots ---
#####--------------------------------------------------------------------------
class TimeSeriesPlot(Subplot, object):
    """Defines a time series based subclass of Subplot."""
    def __init__(self, fig=None, *args, **kwargs):
        """
Accepts the same keywords as a standard subplot, plus a specific `series` keyword.

:Parameters:
    `fig` : Figure
        Base figure.

:Keywords:
    `series` : TimeSeries
        Data to plot

        """
        # Retrieve the series ...................
        _series = kwargs.pop('series',None)
        Subplot.__init__(self,fig,*args,**kwargs)
#        # Force fig to be defined .....
#        if fig is None:
#            fig = TSFigure(_series)
        # Process options .......................
        if _series is not None:
            assert hasattr(_series, "dates")
            self._series = _series.ravel()
            self.xdata = _series.dates
            self.freq = _series.dates.freq
            self.xaxis.set_major_locator

        else:
            self._series = None
            self.xdata = None
            self.freq = None
        self._austoscale = False
        # Get the data to plot
        self.legendsymbols = []
        self.legendlabels = []
    #......................................................
    def set_ydata(self, series=None):
        """Sets the base time series."""
        if self._series is not None:
            print "WARNING ! Base series is being changed."""
        self._series = series.ravel()
        if isinstance(series, TimeSeries):
            self.xdata = self.series.dates
    #....
    def get_ydata(self):
        """Gets the base time series."""
        return self._series
    ydata = property(fget=get_ydata, fset=set_ydata, doc='Time series')
    #......................................................
    def _check_plot_params(self,*args):
        """Defines the plot coordinates (and basic plotting arguments)."""
        remaining = list(args)
        # No args ? Use defaults, if any
        if len(args) == 0:
            if self.xdata is None:
                raise ValueError, "No date information available!"
            return (self.xdata, self.ydata)
        output = []
        while len(remaining) > 0:
            a = remaining.pop(0)
            # The argument is a format: use default dates/
            if isinstance(a,str):
                if self.xdata is None:
                    raise ValueError, "No date information available!"
                else:
                    output.extend([self.xdata, self.ydata, a])
            # The argument is a TimeSeries: use its dates for x
            elif isinstance(a, TimeSeries):
                (x,y) = (a._dates, a._series)
                if len(remaining) > 0 and isinstance(remaining[0], str):
                    b = remaining.pop(0)
                    output.extend([x,y,b])
                else:
                    output.extend([x,y])
            # The argument is a DateArray............
            elif isinstance(a, (Date, DateArray)):
                # Force to current freq
                if self.freq is not None:
                    if a.freq != self.freq:
                        a = a.asfreq(self.freq)
                # There's an argument after
                if len(remaining) > 0:
                    #...and it's a format string
                    if isinstance(remaining[0], str):
                        b = remaining.pop(0)
                        if self.ydata is None:
                            raise ValueError, "No data information available!"
                        else:
                            output.extend([a, self.ydata, b])
                    #... and it's another date: use the default
                    elif isinstance(remaining[0], DateArray):
                        if self.ydata is None:
                            raise ValueError, "No data information available!"
                        else:
                            output.extend([a, self.ydata])
                    #... and it must be some data
                    else:
                        b = remaining.pop(0)
                        if len(remaining) > 0:
                            if isinstance(remaining[0], str):
                                c = remaining.pop(0)
                                output.extend([a,b,c])
                            else:
                                output.extend([a,b])
                else:
                    if self.ydata is None:
                        raise ValueError, "No data information available!"
            # Otherwise..............................
            elif len(remaining) > 0 and isinstance(remaining[0], str):
                b = remaining.pop(0)
                if self.xdata is None:
                    raise ValueError, "No date information available!"
                else:
                    output.extend([self.xdata, a, b])
            elif self.xdata is None:
                raise ValueError, "No date information available!"
            else:
                output.extend([self.xdata, a])
        # Reinitialize the plot if needed ...........
        if self.xdata is None:
            self.xdata = output[0]
            self.freq = self.xdata.freq
        # Force the xdata to the current frequency
        elif output[0].freq != self.freq:
            output = list(output)
            output[0] = output[0].asfreq(self.freq)
        return output
    #......................................................
    def tsplot(self,*parms,**kwargs):
        """Plots the data parsed in argument.
This command accepts the same keywords as `matplotlib.plot`."""
#        parms = tuple(list(parms) + kwargs.pop('series',None))
#        print "Parameters: %s - %i" % (parms, len(parms))
#        print "OPtions: %s - %i" % (kwargs, len(kwargs))
        parms = self._check_plot_params(*parms)
        self.legendlabels.append(kwargs.get('label',None))
        Subplot.plot(self, *parms,**kwargs)
        self.format_dateaxis()
    #......................................................
    def format_dateaxis(self,maj_spacing=None, min_spacing=None,
                        strformat="%Y", rotate=True):
        """Pretty-formats the date axis (x-axis).

:Parameters:
    `major` : Integer *[5]*
        Major tick locator, in years (major tick every `major` years).
    `minor` : Integer *[12]*
        Minor tick locator, in months (minor ticks every `minor` months).
    `strformat` : String *['%Y']*
        String format for major ticks ("%Y").
        """
        # Get the locator class .................
        majlocator = TimeSeries_DateLocator(self.freq, dynamic_mode=True,
                                            minor_locator=False)
        minlocator = TimeSeries_DateLocator(self.freq, dynamic_mode=True,
                                            minor_locator=True)
        self.xaxis.set_major_locator(majlocator)
        self.xaxis.set_minor_locator(minlocator)
        # Get the formatter .....................
        majformatter = TimeSeries_DateFormatter(self.freq, dynamic_mode=True,
                                                minor_locator=False)
        minformatter = TimeSeries_DateFormatter(self.freq, dynamic_mode=True,
                                                minor_locator=True)
        self.xaxis.set_major_formatter(majformatter)
        self.xaxis.set_minor_formatter(minformatter)
        #........................................
#        if rcParams['backend'] == 'PS':
#            rotate = False
#            warnings.warn("dateplot: PS backend detected, rotate disabled")
#        if self.is_last_row():
#            if rotate:
#                setp(self.get_xticklabels(),rotation=45)
    #......................................................
    def set_datelimits(self, start_date=None, end_date=None):
        """Sets the date limits of the plot to start_date and end_date.
    The dates can be given as timeseries.Date objects, strings or integers.
        
:Inputs:
    start_date : var *[None]*
        Starting date of the plot. If None, the current left limit is used.
    end_date : var *[None]*
        Ending date of the plot. If None, the current right limit is used.
        """
        freq = self.freq
        if freq is None:
            raise ValueError("Undefined frequency! Date limits can't be fixed!")
        current_limits = self.get_xlim()
        #
        def get_datevalue(date, freq):
            if isinstance(date, timeseries.Date):
                return date.asfreq(freq).value
            elif isinstance(date, str):
                return timeseries.Date(freq, string=date).value
            elif isinstance(date, (int,float)) or \
                (isinstance(date, numpy.ndarray) and (date.size == 1)):
                return date
            raise ValueError("Unrecognizable date '%s'" % date)
        # Fix left limit ..............
        if start_date is None:
            xleft = current_limits[0]
        else:
            xleft = get_datevalue(start_date, freq)
        # Fix right limit .......
        if end_date is None:
            xright = current_limits[-1]
        else:
            xright = get_datevalue(end_date, freq)
        self.set_xlim(xleft, xright)
        return (xleft, xright)
    

TSPlot = TimeSeriesPlot

def add_yaxis(fsp=None, position='right', yscale=None, basey=10, subsy=None,
              **kwargs):
    """Adds a second y-axis to a plot.
 
:Parameters:
    `fsp` : Subplot *[None]*
        Subplot to which the secondary y-axis is added. If *None*, the current
        subplot is selected
    `position` : String in `('left','right')` *['right']*
        Position of the new axis.
    `yscale` : String, in `('log', 'linear')` *[None]*
        Scale of the new axis. If None, uses the same scale as the first y 
axis
    `basey` : Integer *[10]*
        Base of the logarithm for the new axis (if needed).
    `subsy` : sequence *[None]*
        Sequence of the location of the minor ticks;
        None defaults to autosubs, which depend on the number of decades in 
the plot.  
        Eg for base 10, subsy=(1,2,5) will  put minor ticks on 1,2,5,11,12,15, 
21, ....
        To turn off minor ticking, set subsy=[]
 
    """
    if fsp is None:
        fsp = pylab.gca()
    if not isinstance(fsp, TimeSeriesPlot):
        raise TypeError("The current plot is not a TimeSeriesPlot")
    fig = fsp.figure
    axisini = fsp.axis()
    fsp_alt_args = (fsp._rows, fsp._cols, fsp._num+1)
    fsp_alt = fig.add_tsplot(frameon=False, position=fsp.get_position(),
                             sharex=fsp, *fsp_alt_args)
    # Set position ....................
    if position == 'right':
        (inipos, newpos) = ('left', 'right')
    else:
        (inipos, newpos) = ('right','left')
    # Force scales tics to one side ...
    fsp.yaxis.set_ticks_position(inipos)
    fsp.yaxis.set_label_position(inipos)
    # Force 2nd ticks to the other side..
    fsp_alt.yaxis.set_ticks_position(newpos)
    fsp_alt.yaxis.set_label_position(newpos) 
    # Force period axis scale..........
    if yscale is None:
        yscale = fsp.get_yscale()
        try:
            basey = fsp.yaxis.get_major_locator()._base
        except AttributeError:
            basey = 10.
    fsp_alt.set_yscale(yscale, basey=basey, subsy=subsy)
    # Guess we're good ................
    fsp_alt.set_xticks('')
    fsp_alt.set_xticklabels('')
    
    pylab.draw_if_interactive()
    return fsp_alt

TimeSeriesPlot.add_yaxis = add_yaxis

#####--------------------------------------------------------------------------
#---- --- TimeSeries Figures ---
#####--------------------------------------------------------------------------
class TimeSeriesFigure(Figure):
    """Time Series Figure: all subplots share the same time series.
    """
    def __init__(self, series=None, **kwargs):
        self._series = series
        Figure.__init__(self,**kwargs)
        fspnum = kwargs.pop('fspnum',None)
        if fspnum is not None:
            self.add_tsplot(fspnum, series=series)
    #.........
    def add_tsplot(self, *args, **kwargs):
        """Adds a `TimeSeriesPlot` subplot to the figure."""
        kwargs.update(SubplotClass=TimeSeriesPlot)
        if self._series is not None:
            kwargs.update(series=self._series)
        return add_generic_subplot(self, *args, **kwargs)
    add_plot = add_tsplot
TSFigure = TimeSeriesFigure
#................................................
def tsfigure(series=None, **figargs):
    """Creates a new `TimeSeriesFigure` object.

:Parameters:
    `series` : TimeSeries object
        Input data.
    `figargs` : Dictionary
        Figure options [`figsize`, `dpi`, `facecolor`, `edgecolor`, `frameon`].
    """
    figargs.update(FigureClass=TSFigure)
    figargs.update(series=series)
    fig = pylab.figure(**figargs)
    return fig

def add_tsplot(axes, *args, **kwargs):
    kwargs.update(SubplotClass=TimeSeriesPlot)
    if 'series' not in kwargs.keys():
        if hasattr(axes, 'series'):
            kwargs['series'] = axes.series
        elif hasattr(axes, '_series'):
            kwargs['series'] = axes._series
        else:
            kwargs['series'] = None
    return add_generic_subplot(axes, *args, **kwargs)
Figure.add_tsplot = add_tsplot


def tsplot(series, *args, **kwargs):
    """Plots the series to the current TimeSeries subplot.
    If the current plot is not a TimeSeriesPlot, a new TimeSeriesFigure is created."""
    # allow callers to override the hold state by passing hold=True|False
    b = pylab.ishold()
    h = kwargs.pop('hold', None)
    if h is not None:
        pylab.hold(h)
    # Get the current figure, or create one
    figManager = _pylab_helpers.Gcf.get_active()
    if figManager is not None :
        fig = figManager.canvas.figure
        if not isinstance(fig, TimeSeriesFigure):
            fig = tsfigure(series=series)
    else:
        fig = tsfigure(series=series)
    # Get the current axe, or create one
    sub = fig._axstack()
    if sub is None:
        sub = fig.add_tsplot(111,series=series,**kwargs)
    try:
        ret = sub.tsplot(series, *args, **kwargs)
        pylab.draw_if_interactive()
    except:
        pylab.hold(b)
        raise
    pylab.hold(b)
    return ret

################################################################################
if __name__ == '__main__':

    da = date_array(start_date=Date(freq='B', year=2003, quarter=3, month=1, day=17),
                    length=10)
    ser = timeseries.time_series(MA.arange(len(da)), dates=da)
#    ser[4] = MA.masked
#    ser_2 = timeseries.time_series(MA.arange(len(da)), dates=da.asfreq('Q'))

    pylab.figure()
    pylab.gcf().add_tsplot(111)
    pylab.gca().tsplot(ser, 'ko-')
    pylab.gca().format_dateaxis()
#    pylab.gca().tsplot(ser_2, 'rs')
    pylab.show()
