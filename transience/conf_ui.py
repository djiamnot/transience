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
Configuration screen
"""
import os
import random
from twisted.internet import reactor
from txosc import osc
from transience import score
from transience import inscore


class ConfScreen(object):
    """
    ConfScreen defines layout and behaviour of the configuration screen 
    """

    def __init__(self, conf):
        """
        Initialize the page
        @param conf: the configuration handed down by application
        """
        self.sconf = inscore.INScore()
        # TODO: This may be confusing...  this constructor depends on a
        # configuration handed down. Maybe it is OK... 
        self.configuration = conf
        self.arrangement = self.configuration.parser.elements
        self.OSCcallback = self.sconf.receiver.addCallback("/mouse",self.mouse_handler)
                
    def mouse_handler(self, message, address):
        """
        Handle mouse clicks in visible elements
        """
        # TODO: implement a check for visibility
        print("App received {} from {}".format(message.getValues()[0], address))
        print("Values: ")
        print(message.getValues())
        if message.getValues()[0] == 'clicked':
            try:
                self.page = self.page_iter.next()
            except StopIteration:
                print("||||||||| END OF PIECE |||||||||")
                self.sconf._send(osc.Message("/ITL/scene/*","del"))
                #self.page_iter = iter(page_sequence)
            self.set_score_page()
            reactor.callLater(1.0,self.next_page)
            print("Current page should be: ", self.page)
        if message.getValues()[0] == 'quitB' and message.getValues()[1] == "clicked":
            print("Quit invoked!  Going for sys.exit")
            self.sconf._send(osc.Message("/ITL", "quit"))
            self.sconf.stop()
    
    def _init_conf_screen(self):
        self.sconf._send(osc.Message("/ITL/conf/*","del"))
        self.sconf._send(osc.Message("/ITL/conf/title","set","txt",
                                     "Transience Configuration"))
        self.sconf._send(osc.Message("/ITL/conf/title", "scale", 4.0))
        self.sconf._send(osc.Message("/ITL/conf/title", "x", 0.0))
        self.sconf._send(osc.Message("/ITL/conf/title", "y", -0.5))
        #def _stop():
        #    reactor.stop()
        #reactor.callLater(20.0,_stop)

    def make_cancel_button(self):
        ## quitbutton = score.Button(x=-1., y=-1., URI="quitB", txt="Quit")
        ## self.sconf._send(quitbutton.doit())
        ## self.sconf._send(quitbutton.watch_mouse_down())
        ## self.sconf._send(quitbutton.set_color(255, 0, 0))
        URI = "/ITL/scene/cancel_conf"
        txt = "CANCEL"
        self.sconf._send(osc.Message(URI, "set", "txt", txt))
        self.sconf._send(osc.Message(URI, "x", -1.2))
        self.sconf._send(osc.Message(URI, "y", -0.90))
        self.sconf._send(osc.Message(URI, "xorigin", -1))
        self.sconf._send(osc.Message(URI, "yorigin", 1))
        self.sconf._send(osc.Message(URI, "scale", 2.0))
        self.sconf._send(osc.Message(URI, "color", 255, 0, 0))
        self.sconf._send(osc.Message(URI,"watch","mouseUp",
                                     "127.0.0.1:7001/mouse", "cancel_conf", "clicked"))

    def make_cancel_button(self):
        ## quitbutton = score.Button(x=-1., y=-1., URI="quitB", txt="Quit")
        ## self.sconf._send(quitbutton.doit())
        ## self.sconf._send(quitbutton.watch_mouse_down())
        ## self.sconf._send(quitbutton.set_color(255, 0, 0))
        URI = "/ITL/scene/save_conf"
        txt = "SAVE"
        self.sconf._send(osc.Message(URI, "set", "txt", txt))
        self.sconf._send(osc.Message(URI, "x", -1.2))
        self.sconf._send(osc.Message(URI, "y", -0.90))
        self.sconf._send(osc.Message(URI, "xorigin", -1))
        self.sconf._send(osc.Message(URI, "yorigin", 1))
        self.sconf._send(osc.Message(URI, "scale", 2.0))
        self.sconf._send(osc.Message(URI, "color", 255, 0, 0))
        self.sconf._send(osc.Message(URI,"watch","mouseUp",
                                     "127.0.0.1:7001/mouse", "save_conf", "clicked"))

    def set_conf_page(self):
        reactor.callLater(0.01,self.make_recitation)
        reactor.callLater(0.01, self.make_mood)
        reactor.callLater(0.01, self.make_instructions)
        reactor.callLater(0.01, self.make_durations)
        reactor.callLater(0.01, self.make_glissandis)
        reactor.callLater(0.01, self.make_interactions)
        reactor.callLater(0.01, self.make_envelopes)
        reactor.callLater(0.01, self.make_melos)
        reactor.callLater(0.01, self.make_rhythms)
        reactor.callLater(0.01, self.make_poems)
        reactor.callLater(0.01, self.make_jtexts)
        reactor.callLater(0.01, self.make_quit_button)
