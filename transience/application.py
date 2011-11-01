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
from transience import score
from transience import stacks
from twisted.internet import reactor
from txosc import osc
import time
import os
import sys

"""
Application
Sets up and controls the score
"""


class Application(object):
    """
    Starts the transience application
    """
    def __init__(self, configuration):
        # we read configuration here:
        self.configuration = configuration
        #print("Got config from COnfiguration: ", self.configuration.p.pages)
        print("*** Running Transience version {}".format(__version__))
        #self.set_score_page(self.current_page)
        self.page = stacks.Page(configuration)
                #reactor.callLater(0.01,self.page.greet)
        #reactor.callLater(12.0, self.page.set_score_page)
        #reactor.callLater(1.0, self.page.next_page)
        #self.page.oscore.run()

    def greet(self):
        self.page.greet()

        
## if __name__ == "__main__":
##     app = Application()
##     print("will run application!")
##     app.run()
