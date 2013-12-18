#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# Copyright 2013 Alberto Rojas (rojas.alberto@gmail.com)
# All rights reserved.

import datetime
import sys

_TSTAMP = False

def InitLog(logfile=None, tstamp=False):
  if logfile:
    sys.stdout = open(logfile, 'at')
  global _TSTAMP
  if tstamp:
    _TSTAMP = True

def Log(string):
  if _TSTAMP:
    tstamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print tstamp, string
  else:
    print string
