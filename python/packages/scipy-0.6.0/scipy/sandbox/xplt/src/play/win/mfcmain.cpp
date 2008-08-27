/*
 * mfcmain.cpp -- $Id: mfcmain.cpp 685 2003-03-08 15:26:51Z travo $
 * MFC main program stub
 *
 * Copyright (c) 2000.  See accompanying LEGAL file for details.
 */

extern "C" {
  extern int on_launch(int argc, char *argv[]);
}
#include "mfcapp.h"

mfc_boss the_boss(on_launch);
