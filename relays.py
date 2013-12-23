#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# Copyright 2013 Alberto Rojas (rojas.alberto@gmail.com)
# All rights reserved.

import rh_pb2 as rh

class Relays(object):
  """This class manages the set of configured relays.

  An instance of the class represents a group of relays found on a
  configuration proto (see rh_config.proto).

  To make this class independent of the hardware interface (and to make testing
  easier), the constructor takes functions as parameters that allow it to do
  its work.

  """
  class RelayControl(object):
    """Base class for controling hardware relays."""
    def open(self, id):
      """Open the relay (turn it off)."""
      pass
    def close(self, id):
      """Close the relay (turn it on)."""
      pass
    def read(self, id):
      """Read the current status of the relay."""
      pass
    def init(self, id):
      """Initialize the relay hardware."""
      pass


  def __init__(self, config, relay_control):
    """Construct the object from a configuration proto.

    Args:
      config: Configuration proto (see rh_config.proto).
      relay_control: A RelayControl object implementing the interface to
        control real relays.
    """
    self.relaydict = {relay.relay.id: relay for relay in config.relay_config}
    self.relaycontrol = relay_control
    for hwid in self.HwIdList():
      self.relaycontrol.init(hwid)

  def IdList(self):
    """A list with the string ids of all configured relays."""
    return self.relaydict.keys()

  def HwIdList(self):
    """A list with the hardware ids of all configured relays."""
    return [relay.hardware_id for relay in self.relaydict.values()]

  def Relay(self, id):
    """Returns the relay proto for the given id."""
    relay_cfg = self.relaydict.get(id)
    if relay_cfg:
      return relay_cfg.relay

  def ReadState(self, id):
    """Reads the state of a relay, writes it in the proto, and returns it."""
    relay = self.relaydict[id]
    relay.relay.state = self.relaycontrol.read(relay.hardware_id)
    return relay.relay.state

  def ReadAllStates(self):
    """Reads the state of all relays and writes them in the proto."""
    for id in self.IdList():
      self.ReadState(id)

  def Close(self, id):
    return self.relaycontrol.close(self.relaydict[id].hardware_id)

  def Open(self, id):
    return self.relaycontrol.open(self.relaydict[id].hardware_id)
