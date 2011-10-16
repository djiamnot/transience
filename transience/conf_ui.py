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

    def __init__(self, conf, osc_conf):
        """
        Initialize the configuration screen
        @param conf: the configuration handed down by application
        """
        self.sconf = osc_conf
        self.configuration = conf
        self.arrangement = self.configuration.parser.elements
        self.OSCcallback = self.sconf.receiver.addCallback("/mouse",self.mouse_handler)
        self._init_conf_screen()

    def mouse_handler(self, message, address):
        """
        Handle mouse clicks in visible elements
        """
        # TODO: implement a check for visibility
        print("App received {} from {}".format(message.getValues()[0], address))
        print("Values: ")
        print(message.getValues())
        if message.getValues()[0] == 'cancel_conf' and message.getValues()[1] == "clicked":
            print("Canceling configuration")
            self.sconf._send(osc.Message("/ITL/conf", "del"))
        if message.getValues()[0] == 'save_conf' and message.getValues()[1] == "clicked":
            print("Saving current configuration")
            
            
    
    def _init_conf_screen(self):
        self.sconf._send(osc.Message("/ITL/conf","new"))
        self.sconf._send(osc.Message("/ITL/conf","width", 1.89583))
        self.sconf._send(osc.Message("/ITL/conf","height", 1.34115))
        self.sconf._send(osc.Message("/ITL/conf/title","set","txt",
                                     "Transience Configuration"))
        self.sconf._send(osc.Message("/ITL/conf/title", "scale", 4.0))
        self.sconf._send(osc.Message("/ITL/conf/title", "x", 0.0))
        self.sconf._send(osc.Message("/ITL/conf/title", "y", -0.7))
        self.make_save_button()
        self.make_cancel_button()
        self.set_conf_page()
        #def _stop():
        #    reactor.stop()
        #reactor.callLater(20.0,_stop)

    def make_cancel_button(self):
        ## quitbutton = score.Button(x=-1., y=-1., URI="quitB", txt="Quit")
        ## self.sconf._send(quitbutton.doit())
        ## self.sconf._send(quitbutton.watch_mouse_down())
        ## self.sconf._send(quitbutton.set_color(255, 0, 0))
        URI = "/ITL/conf/cancel_conf"
        txt = "CANCEL"
        self.sconf._send(osc.Message(URI, "set", "txt", txt))
        self.sconf._send(osc.Message(URI, "x", -1.2))
        self.sconf._send(osc.Message(URI, "y", 0.90))
        self.sconf._send(osc.Message(URI, "xorigin", -1))
        self.sconf._send(osc.Message(URI, "yorigin", 1))
        self.sconf._send(osc.Message(URI, "scale", 2.0))
        self.sconf._send(osc.Message(URI, "color", 255, 0, 0))
        self.sconf._send(osc.Message(URI,"watch","mouseUp",
                                     "127.0.0.1:7001/mouse", "cancel_conf", "clicked"))

    def make_save_button(self):
        ## quitbutton = score.Button(x=-1., y=-1., URI="quitB", txt="Quit")
        ## self.sconf._send(quitbutton.doit())
        ## self.sconf._send(quitbutton.watch_mouse_down())
        ## self.sconf._send(quitbutton.set_color(255, 0, 0))
        URI = "/ITL/conf/save_conf"
        txt = "SAVE"
        self.sconf._send(osc.Message(URI, "set", "txt", txt))
        self.sconf._send(osc.Message(URI, "x", 1.2))
        self.sconf._send(osc.Message(URI, "y", 0.90))
        self.sconf._send(osc.Message(URI, "xorigin", -1))
        self.sconf._send(osc.Message(URI, "yorigin", 1))
        self.sconf._send(osc.Message(URI, "scale", 2.0))
        self.sconf._send(osc.Message(URI, "color", 255, 0, 0))
        self.sconf._send(osc.Message(URI,"watch","mouseUp",
                                     "127.0.0.1:7001/mouse", "save_conf", "clicked"))

    def set_conf_page(self):
        sequence = [1,2,3,4, 5]
        self.recitations = ConfStrip()
        _x = -0.9
        _y = -0.5
        _component = "conf/"
        for i in sequence:
            setattr(self.recitations, "recitation%s"%(str(i)), score.Element(
                x = _x,
                y = _y,
                URI = "recitation"+str(i),
                path = "recitation",
                number = i,
                scale = 0.7
                ))
            exec("self.recitations.recitation%s.component = _component"%(str(i)))
            self.sconf._send(eval("self.recitations.{}.image()".format("recitation"+str(i))))
            exec("self.recitations.recitation%s.stack_sequence = self.arrangement['recitation']"%(str(i)))
            eval("self.sconf._send(self.recitations.recitation%s.get_x())"
                 %(str(i)))
            eval("self.sconf._send(self.recitations.recitation%s.get_y())"
                 %(str(i)))
            eval("self.sconf._send(self.recitations.recitation%s.scale_element())"
                 %(str(i)))
            eval("self.sconf._send(self.recitations.recitation%s.watch_mouse_down())"
                 %(str(i)))
            _x += 0.4
        ## reactor.callLater(0.01, self.make_recitation)
        ## reactor.callLater(0.01, self.make_mood)
        ## reactor.callLater(0.01, self.make_instructions)
        ## reactor.callLater(0.01, self.make_durations)
        ## reactor.callLater(0.01, self.make_glissandis)
        ## reactor.callLater(0.01, self.make_interactions)
        ## reactor.callLater(0.01, self.make_envelopes)
        ## reactor.callLater(0.01, self.make_melos)
        ## reactor.callLater(0.01, self.make_rhythms)
        ## reactor.callLater(0.01, self.make_poems)
        ## reactor.callLater(0.01, self.make_jtexts)
        ## reactor.callLater(0.01, self.make_quit_button)
        ## reactor.callLater(0.01, self.make_cancel_button)
        ## reactor.callLater(0.01, self.make_save_button)

class ConfStrip(object):
    """
    A strip of images representing one possible configuration of the score
    elements.  The possibilities are precomputed following the instructions
    of creating 'paths' from rombic matrices and presented as horizintal strips,
    one strip per score element.
    """

    def __init__(self):
        """
        @param element: The score element
        @param type: string
        @param sequence: The sequence of elements on the score stack
        @param type: list
        """
        
        
    def _createStrip(self, element, sequence):
       """
       Dynamically create class variables representing the objects to be
       displayed on screen

       @param element: The score element
       @param type: string
       @param sequence: The sequence of elements on the score stack
       @param type: list
       """
       
