#ifndef C_TSERIES_H
#define C_TSERIES_H

#include "c_lib.h"

PyObject *TimeSeries_convert(PyObject *, PyObject *);

PyObject *MaskedArray_mov_sum(PyObject *, PyObject *, PyObject *);
PyObject *MaskedArray_mov_median(PyObject *, PyObject *, PyObject *);
PyObject *MaskedArray_mov_average(PyObject *, PyObject *, PyObject *);
PyObject *MaskedArray_mov_stddev(PyObject *, PyObject *, PyObject *);

void import_c_tseries(PyObject *);

#endif
