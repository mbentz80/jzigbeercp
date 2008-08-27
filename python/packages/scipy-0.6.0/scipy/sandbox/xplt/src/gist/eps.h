/*
 * EPS.H
 *
 * $Id: eps.h 685 2003-03-08 15:26:51Z travo $
 *
 * Declare the Encapsulated PostScript pseudo-engine for GIST.
 *
 */
/*    Copyright (c) 1994.  The Regents of the University of California.
                    All rights reserved.  */

#ifndef EPS_H
#define EPS_H

#include "gist.h"

extern Engine *EPSPreview(Engine *engine, char *file);

extern int epsFMbug;

#endif
