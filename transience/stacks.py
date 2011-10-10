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
Transience elements combined into pages
"""
import os
import random
import itertools
from twisted.internet import reactor
from txosc import osc
from transience import score
from transience import inscore


# TODO: implement the 'X' card that will decide which elements are diplayed
# at which time (and the elements should know in advance so that they can show
# it)

recitation = score.Element(
    x = -1.08661,
    y = -0.85,
    URI="recitation",
    path="recitation",
    number=1,
    scale = 1.)

mood = score.Element(
    x = -0.359580,
    y = -0.85,
    URI="mood",
    path="mood",
    number=1)

instructions = score.Element(
    x = 0.446194,
    y = -0.85,
    URI="instructions",
    path="instructions",
    number=1)

durations = score.Element(
    x = 1.06037,
    y = -0.85,
    URI="durations",
    path="durations",
    number=1)

glissandis = score.Element(
    x = -0.616798,
    y = -0.572178,
    URI="glissandis",
    path="glissandis",
    number=1,
    scale = 0.25)

interactions = score.Element(
    x = 0.564305,
    y = -0.561680,
    URI="interactions",
    path="interactions",
    number=1,
    scale = 0.5)

envelopes = score.Element(
    x = 0.0918635,
    y = 0.136483,
    URI="envelopes",
    path="envelopes",
    number=1,
    scale = 0.8)

melos = score.Element(
    x = 0.186352,
    y = 0.490814,
    URI="melos",
    path="melos",
    number=1,
    scale = 0.75)

rhythms = score.Element(
    x = 0.186352,
    y = 0.839895,
    URI="rhythms",
    path="rhythms",
    number=1,
    scale = 0.75)

poems = score.Element(
    x = -1.16010,
    y = 0.154856,
    URI="poems",
    path="poems",
    number=101,
    scale = 0.6)

# TODO: deal with etexts as well!
jtexts = score.Element(
    x = 0.178478,
    y = -0.244094,
    URI="jtexts",
    path="jtexts",
    number=101,
    scale = 0.8,
    show = 0)

etexts = score.Element(
    x = 0.178478,
    y = -0.244094,
    URI="etexts",
    path="etexts",
    number=101,
    scale = 0.8,
    show = 0)

page_sequence = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# Shuffle the page sequence every time we start application.
page_sequence = random.shuffle(page_sequence)

class Page(object):
    """
    Class page defines one page layout 
    """

    def __init__(self, conf):
        """
        Initialize the page
        @param conf: the configuration handed down by application
        """
        self.oscore = inscore.INScore()
        # TODO: This may be confusing...  this constructor depends on a
        # configuration handed down. Maybe it is OK... 
        self.configuration = conf
        self.arrangement = self.configuration.parser.elements
        self.OSCcallback = self.oscore.receiver.addCallback("/mouse",self.mouse_handler)
        # Set up the page layout:
        self.durations = durations
        self.envelopes = envelopes
        self.glissandis = glissandis
        self.instructions = instructions
        self.interactions = interactions
        self.jtexts = jtexts
        self.melos = melos
        self.mood = mood
        self.poems = poems
        self.rhythms = rhythms
        self.recitation = recitation

        # set up the stacks
        self.duration.stack_sequence = int(self.arrangement['durations'])
        self.envelope.stack_sequence = int(self.arrangement['envelopes'])
        self.glissando.stack_sequence = int(self.arrangement['glissandis'])
        self.instruction.stack_sequence = int(self.arrangement['instructions'])
        self.interaction.stack_sequence = int(self.arrangement['interactions'])
        self.jtext.stack_sequence = int(self.arrangement['jtexts'])
        self.melo.stack_sequence = int(self.arrangement['melos'])
        self.mood.stack_sequence = int(self.arrangement['mood'])
        self.poem.stack_sequence = int(self.arrangement['poems'])
        self.rhythm.stack_sequence = int(self.arrangement['rhythms'])
        self.recitation.stack_sequence = int(self.arrangement['recitation'])

    def next_page(self):
        # TODO:  finish this function
        page_count = 0
        if page_count < 9:
            if page_sequence[page_count] == 0:
                self.envelope.stack_sequence = advance_stack('envelope', 1)
                self.pitch.stack_sequence = advance_stack('pitch', 1)
                self.rhythm.stack_sequence = advance_stack('rhythm', 1)
                self.melo.stack_sequence = advance_stack('melo', 1)
            elif page_sequence[page_count] == 1:
                # TODO: Japanese/English/None text changes here
                self.recitation.stack_sequence = advance_stack('recitation', 2)
                self.mood.stack_sequence = advance_stack('mood', 2)
                self.duration.stack_sequence = advance_stack('duration', 2)
            elif page_sequence[page_count] == 2:
                self.envelope.stack_sequence = advance_stack('envelopes', 3)
                self.glissando.stack_sequence = advance_stack('glissandi', 3)
                self.mood.stack_sequence = advance_stack('mood', 3)
                self.interactions = advance_stack('interactions', 3)
                
    def advance_stack(self, name, number):
        """
        Advance to the next element on stack
        """
        # TODO: perhaps make a check that we don't go beyond the stack....
        # TODO: make use of itertools here
        
        
    def mouse_handler(self, message, address):
        """
        Handle mouse clicks in visible elements
        """
        # TODO: implement a check for visibility
        print("App received {} from {}".format(message.getValues()[0], address))
        print("Values: ")
        print(message.getValues())
        if message.getValues()[0] == 'clicked':
            if self.current_page < 8:
                self.page.stack_sequence += 1
            else:
                self.page.stack_sequence = 0
            print("Current page should be: ", self.current_page)
            self.set_score_page(self.current_page)
        if message.getValues()[0] == 'quitB' and message.getValues()[1] == "clicked":
            print("Quit invoked!  Going for sys.exit")
            self.oscore._send(osc.Message("/ITL", "quit"))
            self.oscore.stop()
    
    def greet(self):
        print("Entered greet")
        reactor.callLater(0.1,self._hello)

    def _hello(self):
        self.oscore._send(osc.Message("/ITL/scene/*","del"))
        self.oscore._send(osc.Message("/ITL/scene/text","set","txt","Transience\nby Sandeep Bhagwati"))
        self.oscore._send(osc.Message("/ITL/scene/text", "scale", 4.0))
        #def _stop():
        #    reactor.stop()
        #reactor.callLater(20.0,_stop)

    def make_quit_button(self):
        ## quitbutton = score.Button(x=-1., y=-1., URI="quitB", txt="Quit")
        ## self.oscore._send(quitbutton.doit())
        ## self.oscore._send(quitbutton.watch_mouse_down())
        ## self.oscore._send(quitbutton.set_color(255, 0, 0))
        URI = "/ITL/scene/quitB"
        txt = "QUIT"
        self.oscore._send(osc.Message(URI, "set", "txt", txt))
        self.oscore._send(osc.Message(URI, "x", -1.2))
        self.oscore._send(osc.Message(URI, "y", -0.90))
        self.oscore._send(osc.Message(URI, "xorigin", -1))
        self.oscore._send(osc.Message(URI, "yorigin", 1))
        self.oscore._send(osc.Message(URI, "scale", 2.0))
        self.oscore._send(osc.Message(URI, "color", 255, 0, 0))
        self.oscore._send(osc.Message(URI,"watch","mouseUp","127.0.0.1:7001/mouse", "quitB", "clicked"))

    def make_mood(self):
        #self.mood.image()
        self.oscore._send(self.mood.image())
        self.oscore._send(self.mood.get_x())
        self.oscore._send(self.mood.get_y())
        self.oscore._send(self.mood.scale_element())
        self.oscore._send(self.mood.watch_mouse_down())
        #self.oscore._send(self.mood.watch_mouse_enter())

    def make_recitation(self):
        #self.recitation.image()
        self.oscore._send(self.recitation.image())
        self.oscore._send(self.recitation.get_x())
        self.oscore._send(self.recitation.get_y())
        self.oscore._send(self.recitation.scale_element())
        self.oscore._send(self.recitation.watch_mouse_down())
        #self.oscore._send(self.recitation.watch_mouse_enter())

    def make_rhythms(self):
        #self.rhythms.image()
        self.oscore._send(self.rhythms.image())
        self.oscore._send(self.rhythms.get_x())
        self.oscore._send(self.rhythms.get_y())
        self.oscore._send(self.rhythms.scale_element())
        self.oscore._send(self.rhythms.watch_mouse_down())
        #self.oscore._send(self.rhythms.watch_mouse_enter())

    def make_melos(self):
        #self.melos.image()
        self.oscore._send(self.melos.image())
        self.oscore._send(self.melos.get_x())
        self.oscore._send(self.melos.get_y())
        self.oscore._send(self.melos.scale_element())
        self.oscore._send(self.melos.watch_mouse_down())
        #self.oscore._send(self.melos.watch_mouse_enter())

    def make_envelopes(self):
        #self.envelopes.image()
        self.oscore._send(self.envelopes.image())
        self.oscore._send(self.envelopes.get_x())
        self.oscore._send(self.envelopes.get_y())
        #self.oscore._send(self.envelopes.shear(2.0, 1.0))
        self.oscore._send(self.envelopes.scale_element())
        self.oscore._send(self.envelopes.watch_mouse_down())
        #self.oscore._send(self.envelopes.watch_mouse_enter())

    def make_interactions(self):
        #self.interactions.image()
        self.oscore._send(self.interactions.image())
        self.oscore._send(self.interactions.get_x())
        self.oscore._send(self.interactions.get_y())
        self.oscore._send(self.interactions.scale_element())
        self.oscore._send(self.interactions.watch_mouse_down())
        #self.oscore._send(self.interactions.watch_mouse_enter())

    def make_glissandis(self):
        #self.glissandis.image()
        self.oscore._send(self.glissandis.image())
        self.oscore._send(self.glissandis.get_x())
        self.oscore._send(self.glissandis.get_y())
        self.oscore._send(self.glissandis.scale_element())
        self.oscore._send(self.glissandis.watch_mouse_down())
        #self.oscore._send(self.glissandis.watch_mouse_enter())

    def make_durations(self):
        #self.durations.image()
        self.oscore._send(self.durations.image())
        self.oscore._send(self.durations.get_x())
        self.oscore._send(self.durations.get_y())
        self.oscore._send(self.durations.scale_element())
        self.oscore._send(self.durations.watch_mouse_down())
        #self.oscore._send(self.durations.watch_mouse_enter())

    def make_instructions(self):
        #self.instructions.image()
        self.oscore._send(self.instructions.image())
        self.oscore._send(self.instructions.get_x())
        self.oscore._send(self.instructions.get_y())
        self.oscore._send(self.instructions.scale_element())
        self.oscore._send(self.mood.watch_mouse_down())
        #self.oscore._send(self.instructions.watch_mouse_enter())

    def make_jtexts(self):
        #self.jtexts.image()
        self.oscore._send(self.jtexts.image())
        self.oscore._send(self.jtexts.get_x())
        self.oscore._send(self.jtexts.get_y())
        self.oscore._send(self.jtexts.scale_element())
        self.oscore._send(self.jtexts.watch_mouse_down())
        #self.oscore._send(self.jtexts.watch_mouse_enter())

    def make_poems(self):
        #self.poems.image()
        self.oscore._send(self.poems.image())
        self.oscore._send(self.poems.get_x())
        self.oscore._send(self.poems.get_y())
        self.oscore._send(self.poems.scale_element())
        self.oscore._send(self.poems.watch_mouse_down())
        #self.oscore._send(self.poems.watch_mouse_enter())

    def change_recitation(self):
        self.recitation.number = 4
        self.oscore._send(self.recitation.image())

    def set_score_page(self):
        self.instructions.number = self.instructions.stack_sequence[self.current_instructions]
        self.mood.number = self.mood.stack_sequence[self.current_mood]
        self.recitation.number = self.recitation.stack_sequence[self.current_recitation]
        self.durations.number = self.durations.stack_sequence[self.current_durations]
        self.glissandis.number = self.glissandis.stack_sequence[self.current_glissandis]
        self.interactions.number = self.interactions.stack_sequence[self.current_interactions]
        self.envelopes.number = self.envelopes.stack_sequence[self.current_envelopes]
        self.melos.number = self.melos.stack_sequence[self.current_melos]
        self.rhythms.number = self.rhythms.stack_sequence[self.current_rhythms]
        self.poems.number = self.poems.stack_sequence[self.current_poems]
        self.jtexts.number = self.poems.number
        self.etexts.nyumber = self.poems.number
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
