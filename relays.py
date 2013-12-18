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
  def __init__(self, config, close_func, open_func, read_func, val_map):
    """Construct the object from a configuration proto.

    Args:
      config: Configuration proto (see rh_config.proto).
      close_func: Function to close a relay. Takes the hardware id as an int
          and returns a bool.
      open_func: Function to open a relay. Takes the hardware id as an int
          and returns a bool.
      read_func: Function to read a relay status. Takes the hardware id as an
          int and returns something.
      val_map: Dictionary of the form {read_func_value: proto_relay_state}.
    """
    self.relaydict = {relay.relay.id: relay for relay in config.relay_config}
    self.close_func = close_func
    self.open_func = open_func
    self.read_func = read_func
    self.val_map = val_map

  def IdList(self):
    """A list with the string ids of all configured relays."""
    return self.relaydict.keys()

  def HwIdList(self):
    """A list with the hardware ids of all configured relays."""
    return [relay.hardware_id for relay in self.relaydict.values()]

  def Relay(self, id):
    """Returns the relay proto for the given id."""
    return self.relaydict[id].relay

  def ReadState(self, id):
    """Reads the state of a relay, writes it in the proto, and returns it."""
    relay = self.relaydict[id]
    hw_status = self.read_func(relay.hardware_id)
    relay.relay.state = self.val_map.get(hw_status, rh.Relay.UNKNOWN)
    return relay.relay.state

  def ReadAllStates(self):
    """Reads the state of all relays and writes them in the proto."""
    for id in self.IdList():
      self.ReadState(id)

  def Close(self, id):
    return self.close_func(self.relaydict[id].hardware_id)

  def Open(self, id):
    return self.open_func(self.relaydict[id].hardware_id)
