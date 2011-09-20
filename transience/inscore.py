#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Transience
# Copyright (C) 2011 Michal Seta
#
# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Transience is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Transience.  If not, see <http://www.gnu.org/licenses/>.

"""
INScore control
"""
import os
from twisted.internet import reactor
from txosc import osc
from txosc import async
from txosc import dispatch
from configuration import PrefParser
import time

class INScore(object):
    """
    sends OSC messages to INScore instance
    """
    def __init__(self, host='127.0.0.1', port=7000):
        print("INScore loaded")
        self.send_host = host
        self.send_port = port
        # the following values are defined by INScore, OSCMsg.pdf p.3
        self.receive_out_port = 7001
        self.receive_error_port = 7002
        self.receiver = dispatch.Receiver()
        self.sender = async.DatagramClientProtocol()
        self._sender_port = reactor.listenUDP(0,self.sender)
        self._running = False
        print("INScore inited ...")
        # TODO: Catch any message sent over UDP ports (see comment in runner.py)
        self._receiver_out_port = reactor.listenUDP(
            self.receive_out_port, async.DatagramServerProtocol(self.receiver))
        self._receiver_err_port = reactor.listenUDP(
           self.receive_error_port, async.DatagramServerProtocol(self.receiver))
        self.receiver.addCallback("/mouse", self.mouse_handler)
        # fallback
        self.receiver.fallback = self.fallback

    def fallback(self, message, address):
        """
        Fallback message
        """
        print("Fallback:")
        print("Received {} from {}".format(message,address))

    def mouse_handler(self, message, address):
        """
        mouse interaction handler
        """
        # TODO:L fix this
        #if message.getValues()[0] == 'clicked':
        print("Received {} from {}".format(message,address))
        
        
    def _send(self, msg):
        """
        Prepare an OSC message for INScore element
        The message is
        @param l1: OSC message starting with OSC address.
        """
        self.sender.send(msg, (self.send_host, self.send_port))
        
    def run(self):
        """
        Runs blocking mainloop
        """
        print("Entered runner.run()")
        self._running = True
        try:
        #    print("reactor running")
        #    if self._use_twisted:
        #        from twisted.internet import reactor
        #        reactor.run()
        #    else:
        #        while self._running:
        #            time.sleep(0.1)
            reactor.run()
        except KeyboardInterrupt, e:
            print("Interrupted")
            self.stop()
        
    def stop(self):
        """
        Stops the main loop
        """
        self._running = False
        if reactor.running:
            reactor.stop()
