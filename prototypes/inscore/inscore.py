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
INScore communication and control
"""

import os
from twisted.internet import reactor
from txosc import osc
from txosc import async
from txosc import dispatch

class INScoreCom(object):
    """
    INScore test of OSC message exchange
    """
    def __init__(self, host='127.0.0.1', port=7000):
        self.send_host = host
        self.send_port = port
        # the following values are defined by INScore, OSCMsg.pdf p.3
        self.receive_out_port = 7001
        self.receive_error_port = 7002
        self.receiver = dispatch.Receiver()
        self.sender = async.DatagramClientProtocol()
        self._sender_port = reactor.listenUDP(0,self.sender)
        # self._receiver_out_port = reactor.listenUDP(
        #     self.receive_out_port, async.DatagramClientProtocol(self.receiver))
        # self._receiver_err_port = reactor.listenUDP(
        #     self.receive_err_port, async.DatagramClientProtocol(self.receiver))
        reactor.callLater(0.1,self._hello)

    def _send(self,element):
        self.sender.send(element, (self.send_host, self.send_port))

        
    def _hello(self):
        #self._send(osc.Message("/ITL/scene","del"))
        self._send(osc.Message("/ITL/scene/text","set","txt","Hello!"))
        def _stop():
            reactor.stop()
        reactor.callLater(0.1,_stop)

if __name__ == "__main__":
    app = INScoreCom()
    reactor.run()
