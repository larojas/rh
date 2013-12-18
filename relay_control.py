#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# Copyright 2013 Alberto Rojas (rojas.alberto@gmail.com)
# All rights reserved.

import time
import wiringpi2

from log import Log

PINMODE_INPUT = 0
PINMODE_OUTPUT = 1

LEVEL_LO = 0
LEVEL_HI = 1

DELAY=0.5

_pins = set()

def Init(pins):
  global _pins

  wiringpi2.wiringPiSetup()
  _pins = set(pins)
  Log('Setting pins %s to output mode...' % list(_pins))
  for i in _pins:
    wiringpi2.pinMode(i, PINMODE_OUTPUT)
  Log("Done.")

def SampleLoop(pin):
  Log("Beginning loop...")
  for i in range(5):
    On(pin)
    time.sleep(DELAY)
    Off(pin)
    time.sleep(DELAY)
  Log("Done.")

def On(pin):
  """Turn the relay at the specified pin on."""
  if pin in _pins:
    wiringpi2.digitalWrite(pin, LEVEL_HI)
    return True

def Off(pin):
  """Turn the relay at the specified pin off."""
  if pin in _pins:
    wiringpi2.digitalWrite(pin, LEVEL_LO)

def Status(pin):
  """Read the status of the specified pin."""
  if pin in _pins:
    return wiringpi2.digitalRead(pin)
