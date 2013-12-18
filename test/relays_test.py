#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# Copyright 2013 Alberto Rojas (rojas.alberto@gmail.com)
# All rights reserved.

import os, sys
# The next line assumes tests are run from the dir where the tested class is.
sys.path.append(os.path.abspath('./'))

import unittest
import relays
import rh_pb2 as rh
import rh_config_pb2 as rh_config

class MockRelayControl(object):
  def __init__(self, num_relays):
    self.relays = [0] * num_relays

  def close(self, id):
    self.relays[id] = 1

  def open(self, id):
    self.relays[id] = 0

  def state(self, id):
    return self.relays[id]


class TestRelays(unittest.TestCase):

  def setUp(self):
    config = rh_config.Config()
    config.server_name = 'test_server'
    for i in range(5):
      relay_config = rh_config.RelayConfig()
      relay_config.hardware_id = i
      relay_config.relay.id = "r%d" % i
      relay_config.relay.name = "relay no.%d" % i
      config.relay_config.add().MergeFrom(relay_config)

    self.rc = MockRelayControl(5)
    val_map = {0: rh.Relay.OPEN, 1: rh.Relay.CLOSED }
    self.relays = relays.Relays(config, self.rc.close, self.rc.open,
                                self.rc.state, val_map)

  def testIdList(self):
    self.assertEqual(["r%d" % i for i in range(5)],
                     sorted(self.relays.IdList()))

  def testHwIdList(self):
    self.assertEqual(list(range(5)), sorted(self.relays.HwIdList()))

  def testRelay(self):
    relay = self.relays.Relay("r1")
    self.assertEqual("r1", relay.id)
    self.assertEqual("relay no.1", relay.name)
    self.assertEqual(rh.Relay.UNKNOWN, relay.state)

  def testReadState(self):
    self.assertEqual(rh.Relay.UNKNOWN, self.relays.Relay('r2').state)
    self.assertEqual(rh.Relay.OPEN, self.relays.ReadState('r2'))
    self.assertEqual(rh.Relay.OPEN, self.relays.Relay('r2').state)
    self.rc.relays[2] = 1
    self.assertEqual(rh.Relay.CLOSED, self.relays.ReadState('r2'))
    self.assertEqual(rh.Relay.CLOSED, self.relays.Relay('r2').state)

  def testReadAllStates(self):
    self.rc.relays[1] = self.rc.relays[3] = 1
    self.relays.ReadAllStates()
    all_open = [self.relays.Relay(i).state for i in ['r0', 'r2', 'r4']]
    self.assertEqual([rh.Relay.OPEN] * 3, all_open)
    all_closed = [self.relays.Relay(i).state for i in ['r1', 'r3']]
    self.assertEqual([rh.Relay.CLOSED] * 2, all_closed)

  def testClose(self):
    self.relays.Close('r4')
    self.assertEqual(1, self.rc.relays[4])

  def testOpen(self):
    self.rc.relays[2] = 1
    self.relays.Open('r2')
    self.assertEqual(0, self.rc.relays[2])

if __name__ == '__main__':
  unittest.main()
