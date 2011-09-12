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
Application class
"""
from transience import __version__
#from transience import server
from transience import inscore
from twisted.internet import reactor
from txosc import osc
import time
import os
import sys


class Application(object):
    """
    Starts the transience application
    """
    def __init__(self, configuration):
        # TODO: move this one to inscore.py
        # parser = PrefParser()
        self.configuration = configuration
        self.oscore = inscore.INScore()
        print("*** Running Transience version {}".format(__version__))
        #print("Did it work?")
        reactor.callLater(12.0,self.oscore._send, osc.Message("/ITL/scene/text","scale",10.0))
        reactor.callLater(2.0,self.greet)
        self.oscore.run() # move to INSCore's __init__?
    
    def greet(self):
        print("Entered greet")
        reactor.callLater(0.1,self._hello)
        print("Called callLater?")

    def _hello(self):
        print("Entered _hello")
        self.oscore._send(osc.Message("/ITL/scene/text","del"))
        self.oscore._send(osc.Message("/ITL/scene/text","set","txt","Hello SELF.OSCORE!"))
        self.oscore._send(osc.Message("/ITL/scene/text", "scale", 4.0))
        #def _stop():
        #    reactor.stop()
        #reactor.callLater(20.0,_stop)


## if __name__ == "__main__":
##     app = Application()
##     print("will run application!")
##     app.run()
