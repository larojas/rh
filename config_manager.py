#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# Copyright 2013 Alberto Rojas (rojas.alberto@gmail.com)
# All rights reserved.

from optparse import OptionParser

import google.protobuf.text_format as text_format
from log import InitLog, Log
from relays import Relays
import rh_pb2 as rh
import rh_config_pb2 as rh_config
import relay_control as rc
import time

DEFAULT_CONFIG_FILE = 'rh.conf'


def ReadConfig():
  """Parses the command line flags and reads the config file.

  Returns:
    The config proto (see rh_config.proto) and any args.
  """
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
    return None, None

  config = rh_config.Config()
  text_format.Merge(config_file.read(), config)

  Log('Okay, read %d relay and %d sensor configurations.' 
      % (len(config.relay_config), len(config.sensor_config)))
  config_file.close()
  return config


