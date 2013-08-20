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
import re

from twisted.internet import reactor
from txosc import osc

from transience import conf_matrix
from transience import score
from transience import inscore
from transience import configuration

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
        self.elements = [
            'recitations',
            'moods',
            'instructions',
            'durations',
            'glissandis',
            'interactions',
            'envelopes',
            'melos',
            'rhythms',
            #'poems',
            'etexts',
            ]
        self.path = iter(conf_matrix.paths)
        self.settings = {}
        for element in self.arrangement:
            # we remap to ints because I/O back and forth a text file
            # turns the ints into strings...
            print(element)
            if "midi" in element:
                # midi element is not enumerable so it needs to be treated differently
                self.settings[element] = self.arrangement[element]
            else:
                self.settings[element] = map(int, self.arrangement[element])
            print("settings as we read them in: ", self.settings)
        print("Initial settings: ", self.settings)
        self._set_osc_callbacks()
        self._scale = 0
        self._index = 0
        self._init_conf_screen()
        # Instantiate ConfStrip classes
        ## for element in self.arrangement:
        ##     if element == 'poems' or element == 'jtexts':
        ##         pass
        ##     else:
        ##         exec("self.{} = ConfStrip()".format(element))

    def mouse_handler(self, message, address):
        """
        Handle mouse clicks in visible elements
        """
        new_sequence = []
        if len(message.getValues()) == 2:
            element, click = message.getValues()
            base_element = element[:-1]
            if element == 'cancel_conf' and click == "clicked":
                print("Canceling configuration")
                self.sconf._send(osc.Message("/ITL/conf", "del"))
            if element == 'next_stack' and click == "clicked":
                print("Advancing to ")
                if self._index < 10:
                    self.set_conf_strip(self._index)
                    self._index += 1
                else:
                    self._index = 0
            if element == 'save_conf' and click == "clicked":
                print("Saving current configuration")
                self.save_keys()
            if base_element in self.elements and click == "clicked":
                print("Clicked self.{0}.{1}".format(base_element, element))
                try:
                    new_sequence = self.path.next()
                except StopIteration:
                    self.path = iter(conf_matrix.paths)
                for stack in range(0, 5):
                    exec("self.{0}.{0}{1}.stack_sequence = {2}"
                         .format(base_element, stack, new_sequence))
                    exec("self.{0}.{0}{1}.number = self.{0}.{0}{1}.stack_sequence[{1}]"
                         .format(base_element, stack))
                    eval("self.sconf._send(self.{0}.{0}{1}.image())"
                     .format(base_element, stack))
                    self.settings[base_element] = new_sequence
            ## if base_element in self.elements and click == "hover":
            ##     element, hover = message.getValues()
            ##     print("Hovered over ", element)
            ##     self._query_element("/ITL/conf/"+element, 'scale')
            ##     self.sconf._send(osc.Message("/ITL/conf/"+element, "scale", self._scale*2))
            ## if base_element in self.elements and click == "leave":
            ##     self.sconf._send(osc.Message("/ITL/conf/"+element, "scale", self._scale))
                
    def _query_element(self, element, query):
        uri = element
        query = query
        self.sconf._send(osc.Message(uri, "get", query))

    def _set_osc_callbacks(self):
        self.sconf.receiver.addCallback("/ITL/conf/*",self._conf_element_handler)

    def _conf_element_handler(self, message, address):
        """
        Handles /ITL/conf/*
        """
        if message.getTypeTags() == "sf":
            print("Got {0} from {1}".format(message.getValues(), address))
            if message.getValues()[0] == "scale":
                self._scale = message.getValues()[1]

    def _magnify_element(self, message, address):
        """
        Scale up a given element
        """
        if message.getTypeTags() == "sf":
            print("Got { } from { }".format(message, address))
            

    def save_keys(self):
        ## for element in self.elements:
        ##     sequence = eval("self.{0}.{0}+str(1).stack_sequence"
        ##                     .format(element))
        ##     self.settings[element] = sequence
        print("Saving the following settings: ",self.settings)
        configuration.save_backup_conf()
        configuration.save_conf(self.settings)
        
        
    def hover_handler(self):
        pass

    def _init_conf_screen(self):
        self.sconf._send(osc.Message("/ITL/conf/*","del"))
        self.sconf._send(osc.Message("/ITL/conf","new"))
        self.sconf._send(osc.Message("/ITL/conf","width", 2.39062))
        self.sconf._send(osc.Message("/ITL/conf","height", 1.71875))
        self.sconf._send(osc.Message("/ITL/conf/title","set","txt",
                                     "Transience Configuration"))
        self.sconf._send(osc.Message("/ITL/conf/title", "scale", 4.0))
        self.sconf._send(osc.Message("/ITL/conf/title", "x", 0.0))
        self.sconf._send(osc.Message("/ITL/conf/title", "y", -0.9))
        self.sconf._send(osc.Message("/ITL/conf","color", 100, 100, 100))
        self.make_save_button()
        self.make_cancel_button()
        self.make_next_button()
        self.set_conf_strip(0)
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

    def make_next_button(self):
        ## quitbutton = score.Button(x=-1., y=-1., URI="quitB", txt="Quit")
        ## self.sconf._send(quitbutton.doit())
        ## self.sconf._send(quitbutton.watch_mouse_down())
        ## self.sconf._send(quitbutton.set_color(255, 0, 0))
        URI = "/ITL/conf/next_stack"
        txt = "Next element -->"
        self.sconf._send(osc.Message(URI, "set", "txt", txt))
        self.sconf._send(osc.Message(URI, "x", -0.7))
        self.sconf._send(osc.Message(URI, "y", -0.7))
        self.sconf._send(osc.Message(URI, "xorigin", -1))
        self.sconf._send(osc.Message(URI, "yorigin", 1))
        self.sconf._send(osc.Message(URI, "scale", 2.0))
        self.sconf._send(osc.Message(URI, "color", 255, 0, 0))
        self.sconf._send(osc.Message(URI,"watch","mouseUp",
                                     "127.0.0.1:7001/mouse", "next_stack", "clicked"))

    def set_conf_strip(self, index):
        #sequence = [1,2,3,4, 5]
        #self.recitations = ConfStrip()
        _y = -0.55
        _x = -0.55
        _component = "conf/"
        for i in self.elements:
            self.sconf._send(osc.Message("/ITL/conf/"+i+"*", "del"))
        element = self.elements[index]
        #_x = -0.9
        # using eval/exec functionality to dynamically instantiate
        # classes and build variables.
        # this could have been done with class.attribute.__dict__
        # kind of thing, not sure hwich one is more elegant...
        exec("self.{} = ConfStrip()".format(element))
        self.sconf._send(osc.Message("/ITL/conf/help", "set", "htmlf", score.MEDIA_PATH+"doc/"+element+".html"))
        self.sconf._send(osc.Message("/ITL/conf/help", "xorigin", -1.))
        self.sconf._send(osc.Message("/ITL/conf/help", "yorigin", -1.))
        self.sconf._send(osc.Message("/ITL/conf/help", "x", 0.3))
        self.sconf._send(osc.Message("/ITL/conf/help", "y", -0.8))
        self.sconf._send(osc.Message("/ITL/conf/help", "scale", 1.3))
        for stack in range(0,5):
            setattr(eval("self.{}".format(element)), "{}{}"
                    .format(element,str(stack)), score.Element(
                x = _x,
                y = _y,
                URI = element+str(stack),
                path = element,
                number = self.arrangement[element][stack],
                scale = self.scale_by_element(element)
                ))
            exec("self.{0}.{0}{1}.component = _component"
                 .format(element, str(stack)))
            eval("self.sconf._send(self.{0}.{0}{1}.image())"
                 .format(element, str(stack)))
            # TODO: it would be nice to control the placement by left corner's origin but for some reason
            # this situation below interferes with the cycling of stack arrangements in *some of the components*,
            # not all! Mystery that begs to be solved but mayble a little later.
            ## self.sconf._send(osc.Message("/ITL/conf/{}{}".format(element, str(stack)), "xorigin", -1.))
            ## self.sconf._send(osc.Message("/ITL/conf/{}{}".format(element, str(stack)), "yorigin", -1.))
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
            eval("self.sconf._send(self.{0}.{0}{1}.watch_mouse_enter())"
                 .format(element, str(stack)))
            eval("self.sconf._send(self.{0}.{0}{1}.watch_mouse_leave())"
                 .format(element, str(stack)))
            _y += 0.3
            
    def scale_by_element(self, element):
        if element == 'rhythms':
            return 0.55
        elif element == 'melos':
            return 0.55
        elif element == 'interactions':
            return 0.8
        elif element == 'durations':
            return 1.0
        elif element == 'instructions':
            return 1.0
        elif element == 'glissandis':
            return 0.5
        elif element == 'moods':
            return 1.0
        elif element == 'envelopes':
            return 0.6
        elif element == 'etexts':
            return 1.0
        elif element == 'recitations':
            return 1.0

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
        
        
    
       
