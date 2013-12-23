#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# Copyright 2013 Alberto Rojas (rojas.alberto@gmail.com)
# All rights reserved.

import wiringpi2
import relays

from log import Log

PINMODE_INPUT = 0
PINMODE_OUTPUT = 1

LEVEL_LO = 0
LEVEL_HI = 1

class WiringPiRelayControl(relays.Relays.RelayControl):
  """Relay control using the WiringPi library."""
  def __init__(self):
    self._pins = set()

  def init(self, pins):
    wiringpi2.wiringPiSetup()
    self._pins = set(pins)
    Log('Setting pins %s to output mode...' % list(self._pins))
    for i in self._pins:
      wiringpi2.pinMode(i, PINMODE_OUTPUT)
    Log("Done.")

  def close(self, pin):
  """Turn the relay at the specified pin on."""
  if pin in self._pins:
    wiringpi2.digitalWrite(pin, LEVEL_HI)
    return True

  def open(self, pin):
    """Turn the relay at the specified pin off."""
    if pin in self._pins:
      wiringpi2.digitalWrite(pin, LEVEL_LO)

  def read(self, pin):
    """Read the status of the specified pin."""
    if pin in self._pins:
      hwstatus = wiringpi2.digitalRead(pin)
      if hwstatus == LEVEL_LO:
        return rh.Relay.OPEN
      elif hwstatus == LEVEL_HI:
        return rh.Relay.CLOSED
      return rh.Relay.UNKNOWN

def get():
  """To allow dynamic module load."""
  return WiringPiRelayControl()
