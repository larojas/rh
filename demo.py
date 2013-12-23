#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# Copyright 2013 Alberto Rojas (rojas.alberto@gmail.com)
# All rights reserved.

from config_manager import ReadConfig
from log import InitLog, Log
import relay_control as rc
import time
from relays import Relays

def main():
  InitLog(tstamp=False)
  config = ReadConfig()

  val_map = { rc.LEVEL_LO: rh.Relay.OPEN, rc.LEVEL_HI: rh.Relay.CLOSED }
  relays = Relays(config, rc.On, rc.Off, rc.Status, val_map=val_map)
  rc.Init(relays.HwIdList())

  #Log('Will run a sample loop.')
  #rc.SampleLoop(1)

  Log('Setting solenoid 2')
  time.sleep(1)
  relays.Close('sol_02')
  time.sleep(1)
  relays.ReadAllStates()
  for id in relays.IdList():
    relay = relays.Relay(id)
    Log("Status for relay '%s':%d. (%s)" % (relay.id, relay.state, relay.name))
  time.sleep(1)
  relays.Open('sol_02')

  Log('Finished successfully.')

if __name__ == '__main__':
  main()
