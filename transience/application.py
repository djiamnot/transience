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
        # TODO: move this one to inscore.py
        # parser = PrefParser()
        self.configuration = configuration
        #print("Got config from COnfiguration: ", self.configuration.p.pages)
        print("*** Running Transience version {}".format(__version__))
        #self.set_score_page(self.current_page)
        self.page = stacks.Page()
        reactor.callLater(0.0,self.page.oscore._send,
                          osc.Message("/ITL/scene/*","del"))
        reactor.callLater(0.02,self.page.oscore._send,
                          osc.Message("/ITL/scene","fullscreen", 1))
        reactor.callLater(0.01,self.page.oscore._send,
                          osc.Message("/ITL/scene","foreground"))
        t = 0.05
        for i in range(0,150):
            reactor.callLater(
                t,
                self.page.oscore._send,
                osc.Message("/ITL/scene","color", 255-i,255-i, 255-i))
            t += 0.05
        reactor.callLater(12.0,self.page.oscore._send,
                          osc.Message("/ITL/scene/text","del"))
        reactor.callLater(2.0,self.page.greet)
        self.current_page = 0
        reactor.callLater(12.0, self.set_score_page, self.current_page)
        self.page.oscore.run()
        
    def set_score_page(self, p):
        self.page.instructions.number = self.configuration.p.pages[p]['instructions']
        self.page.mood.number = self.configuration.p.pages[p]['mood']
        self.page.recitation.number = self.configuration.p.pages[p]['recitation']
        self.page.durations.number = self.configuration.p.pages[p]['durations']
        self.page.glissandis.number = self.configuration.p.pages[p]['glissandis']
        self.page.interactions.number = self.configuration.p.pages[p]['interactions']
        self.page.envelopes.number = self.configuration.p.pages[p]['envelopes']
        self.page.melos.number = self.configuration.p.pages[p]['melos']
        self.page.rhythms.number = self.configuration.p.pages[p]['rhythms']
        self.page.poems.number = self.configuration.p.pages[p]['poems']
        self.page.jtexts.number = self.configuration.p.pages[p]['jtexts']
        reactor.callLater(0.01,self.page.make_recitation)
        reactor.callLater(0.01, self.page.make_mood)
        reactor.callLater(0.01, self.page.make_instructions)
        reactor.callLater(0.01, self.page.make_durations)
        reactor.callLater(0.01, self.page.make_glissandis)
        reactor.callLater(0.01, self.page.make_interactions)
        reactor.callLater(0.01, self.page.make_envelopes)
        reactor.callLater(0.01, self.page.make_melos)
        reactor.callLater(0.01, self.page.make_rhythms)
        reactor.callLater(0.01, self.page.make_poems)
        reactor.callLater(0.01, self.page.make_jtexts)
        reactor.callLater(0.01, self.page.make_quit_button)
        
## if __name__ == "__main__":
##     app = Application()
##     print("will run application!")
##     app.run()
