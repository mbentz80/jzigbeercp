"""
Interpolation Tools
===================

Wrappers around FITPACK functions:

  splrep    -- find smoothing spline given (x,y) points on curve.
  splprep   -- find smoothing spline given parametrically defined curve.
  splev     -- evaluate the spline or its derivatives.
  splint    -- compute definite integral of a spline.
  sproot    -- find the roots of a cubic spline.
  spalde    -- compute all derivatives of a spline at given points.
  bisplrep   -- find bivariate smoothing spline representation.
  bisplev   -- evaluate bivariate smoothing spline.

  UnivariateSpline             -- A more recent, object-oriented wrapper;
                                  finds a (possibly smoothed) interpolating
				  spline.
  InterpolatedUnivariateSpline
  LSQUnivariateSpline
  BivariateSpline              -- A more recent, object-oriented wrapper;
                                  finds a interpolating spline for a 
				  bivariate function.

  SmoothBivariateSpline

Interpolation Class

  interp1d -- Create a class whose instances can linearly interpolate
               to compute unknown values of a univariate function.
  interp2d -- Create a class whose instances can interpolate
               to compute unknown values of a bivariate function.
"""

postpone_import = 1
