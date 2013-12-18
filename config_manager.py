#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# Copyright 2013 Alberto Rojas (rojas.alberto@gmail.com)
# All rights reserved.

from optparse import OptionParser

import fileinput
import google.protobuf.text_format as text_format
from log import InitLog, Log
import rh_pb2 as rh
import rh_config_pb2 as rh_config
import relay_control as rc
import time

DEFAULT_CONFIG_FILE = 'rh.conf'

class Relays(object):
  """This class manages the set of configured relays."""
  def __init__(self, config):
    self.relaydict = {relay.relay.id: relay for relay in config.relay_config}

  def IdList(self):
    return self.relaydict.keys()

  def HwIdList(self):
    return [relay.hardware_id for relay in self.relaydict.values()]

  def Init(self):
    """Initialize the hardware."""
    rc.Init(self.HwIdList())

  def Relay(self, id):
    """Returns the relay proto for the given id."""
    return self.relaydict[id].relay

  def ReadState(self, id):
    relay = self.relaydict[id]
    status = rc.Status(relay.hardware_id)
    relay.relay.state = (rh.Relay.CLOSED if status == rc.LEVEL_HI
                         else rh.Relay.OPEN)
    return relay.relay.state

  def ReadAllStates(self):
    for id in self.IdList():
      self.ReadState(id)

  def Close(self, id):
    rc.On(self.relaydict[id].hardware_id)

  def Open(self, id):
    rc.Off(self.relaydict[id].hardware_id)

def InitOptions():
  parser = OptionParser()
  parser.add_option('-c', '--conf', dest='config', metavar='FILE',
                    help='Configuration file name.')

  options, args = parser.parse_args()

  if not options.config:
    options.config = DEFAULT_CONFIG_FILE

  Log('Looking for config file \'%s\'.' % options.config)
  try:
    config_file = open(options.config, 'rt')
  except IOError:
    Log('ERROR: Could not open config file.\n')
    return

  config = rh_config.Config()
  text_format.Merge(config_file.read(), config)

  Log('Okay, read %d relay and %d sensor configurations.' 
      % (len(config.relay_config), len(config.sensor_config)))
  config_file.close()
  return config


def main():
  InitLog(tstamp=False)
  config = InitOptions()

  relays = Relays(config)
  relays.Init()

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
