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
        if message.getValues()[0] == 'conf/' and message.getValues()[1] == "clicked":
            print("Something on conf/ was clicked")
            
    def hover_handler(self):
        pass

    def _init_conf_screen(self):
        self.sconf._send(osc.Message("/ITL/conf","new"))
        self.sconf._send(osc.Message("/ITL/conf","width", 2.39062))
        self.sconf._send(osc.Message("/ITL/conf","height", 1.71875))
        self.sconf._send(osc.Message("/ITL/conf/title","set","txt",
                                     "Transience Configuration"))
        self.sconf._send(osc.Message("/ITL/conf/title", "scale", 4.0))
        self.sconf._send(osc.Message("/ITL/conf/title", "x", 0.0))
        self.sconf._send(osc.Message("/ITL/conf/title", "y", -0.9))
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
        #sequence = [1,2,3,4, 5]
        #self.recitations = ConfStrip()
        _y = -0.7
        _component = "conf/"
        for element in self.arrangement:
            if element == 'poems' or element == 'jtexts':
                pass
            else:
                _x = -0.9
                print("Creating", "self.{} = ConfStrip()".format(element))
                exec("self.{} = ConfStrip()".format(element))
                for stack in self.arrangement[element]:
                    setattr(eval("self.{}".format(element)), "{}{}"
                            .format(element,str(stack)), score.Element(
                        x = _x,
                        y = _y,
                        URI = element+str(stack),
                        path = element,
                        number = stack,
                        scale = self.scale_by_element(element)
                        ))
                    exec("self.{0}.{0}{1}.component = _component"
                         .format(element, str(stack)))
                    eval("self.sconf._send(self.{0}.{0}{1}.image())"
                         .format(element, str(stack)))
                    exec("self.{0}.{0}{1}.stack_sequence = self.arrangement['{0}']"
                         .format(element, str(stack)))
                    eval("self.sconf._send(self.{0}.{0}{1}.get_x())"
                         .format(element, str(stack)))
                    eval("self.sconf._send(self.{0}.{0}{1}.get_y())"
                         .format(element, str(stack)))
                    eval("self.sconf._send(self.{0}.{0}{1}.scale_element())"
                         .format(element, str(stack)))
                    eval("self.sconf._send(self.{0}.{0}{1}.watch_mouse_down())"
                         .format(element, str(stack)))
                    _x += 0.4
                _y += 0.15
            
    def scale_by_element(self, element):
        if element == 'rhythms':
            return 0.25
        elif element == 'melos':
            return 0.3
        elif element == 'interactions':
            return 0.2
        elif element == 'durations':
            return 0.5
        elif element == 'instructions':
            return 0.5
        elif element == 'glissandis':
            return 0.1
        elif element == 'moods':
            return 0.5
        elif element == 'envelopes':
            return 0.3
        elif element == 'etexts':
            return 0.3
        elif element == 'recitations':
            return 0.5

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
       
