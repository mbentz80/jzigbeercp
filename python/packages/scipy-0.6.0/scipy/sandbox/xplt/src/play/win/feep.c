/*
 * feep.c -- $Id: feep.c 685 2003-03-08 15:26:51Z travo $
 * p_feep for MS Windows
 *
 * Copyright (c) 1999.  See accompanying LEGAL file for details.
 */

#include "playw.h"

/* ARGSUSED */
void
p_feep(p_win *w)
{
  MessageBeep(MB_OK);
}
