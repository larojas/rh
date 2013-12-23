#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# Copyright 2013 Alberto Rojas (rojas.alberto@gmail.com)
# All rights reserved.

import web

import rh_pb2 as rh
import rh_config_pb2 as rh_config
from log import InitLog, Log
from relays import Relays
from config_manager import ReadConfig

# Constants
OK = rh.OpResult.OK
BAD_REQ = rh.OpResult.BAD_REQUEST
NOT_FOUND = rh.OpResult.NOT_FOUND

# Globals
config = None
relays = None

# web.py initialization stuff
urls = ('/(.*)', 'Root',
        '/relaycontrol/(.*)', 'RelayControl')
render = web.template.render('templates/')

def InitGlobals():
  global config
  global relays
  # Basic log, while we read config where the log file can be specified.
  InitLog(tstamp=False)
  config = ReadConfig()
  if not config:
    Log('Could not read config file.')
    return False
  # Re-config logging if specified
  if config.has_log_file:
    Log('Logging directed to \'%s\'.' % config.log_file)
    InitLog(logfile=config.log_file, tstamp=True)
  # Get our relay management objects set up
  relay_module = config.relay_module_name + '_relay_control'
  rc = __import__(relay_module)
  relays = Relays(config, rc.get())
  if not relays:
    Log('Could not initialize relays.')
    return False
  return True

class Root(object):
  def GET(self, name):
    # i = web.input(name=None)
    age = 30
    return render.index('mi querido %s %s' % (name, str(age)))

class RelayControl(object):

  def __init__(self):
    self.get_actions = {'list': self.List }

  def GET(self, path):
    comp = path.split('/')
    if not comp:
      return self.Send(self.Response(BAD_REQ, descr='action missing'))
    action = comp[0]
    if action not in get_actions:
      return self.Send(self.Response(BAD_REQ, descr='unknown action'))
    return self.get_actions[action](comp)

  def Response(self, code=OK, subcode=None, descr=None):
    msg = rh.RelayResponse()
    msg.result.code = code
    if subcode: msg.result.subcode = subcode
    if description: msg.result.description = descr
    return msg

  def Send(self, msg):
    """Send the specified message as the response to the operation."""
    web.header('Content-Type', 'application/octet-stream')
    return msg.SerializeToString()

  def List(self, comp):
    """List all relays or a specific one."""
    # only zero or one parameter allowed
    if len(comp) > 2:
      return self.Send(
        self.Response(BAD_REQ, descr='list receives zero or one parameter'))
    elif len(comp) == 2:
      relay = relays.Relay(comp[1])
      if not relay:
        return self.Send(self.Response(NOT_FOUND, descr='relay not found'))
      resp = self.Response()
      resp.add_relay(relay)
      return self.Send(resp)
    else:
      resp = self.Response()
      for id in relays.IdList():
        resp.add_relay(relays.Relay(id))
      return self.Send(resp)

if __name__ == '__main__':
  if InitGlobals():
    app = web.application(urls, globals())
    app.run()
  else:
    Log('An error occured initializing the server. Read previous log entries '
        'to find the exact reason.')
