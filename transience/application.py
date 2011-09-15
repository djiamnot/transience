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
from twisted.internet import reactor
from txosc import osc
import time
import os
import sys

"""
Application
Sets up and controls the score
"""
recitation = score.Element(
                x = -0.99,
                y = -0.85,
                URI="recitation",
                path="recitation",
                number=1)

mood = score.Element(
                x = -0.30,
                y = -0.85,
                URI="mood",
                path="mood",
                number=1)

instructions = score.Element(
                x = -0.30,
                y = -0.85,
                URI="instructions",
                path="instructions",
                number=1)

durations = score.Element(
                x = -0.30,
                y = -0.85,
                URI="durations",
                path="durations",
                number=1)

glissandis = score.Element(
                x = -0.30,
                y = -0.85,
                URI="glissandis",
                path="glissandis",
                number=1)

interactions = score.Element(
                x = -0.30,
                y = -0.85,
                URI="interactions",
                path="interactions",
                number=1)

envelopes = score.Element(
                x = -0.30,
                y = -0.85,
                URI="envelopes",
                path="envelopes",
                number=1)

melos = score.Element(
                x = -0.30,
                y = -0.85,
                URI="melos",
                path="melos",
                number=1)

rhythms = score.Element(
                x = -0.30,
                y = -0.85,
                URI="rhythms",
                path="rhythms",
                number=1)

poems = score.Element(
                x = -0.30,
                y = -0.85,
                URI="poems",
                path="poems",
                number=101)

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
        self.recitation = recitation
        self.mood = mood
        self.instructions = instructions
        self.durations = durations
        self.glissandis = glissandis
        self.interactions = interactions
        self.envelopes = envelopes
        self.melos = melos
        self.rhythms = rhythms
        self.poems = poems
        reactor.callLater(0.1,self.recitation.watch_mouse_enter)
        reactor.callLater(0.0,self.oscore._send, osc.Message("/ITL/scene/*","del"))
        reactor.callLater(0.01,self.oscore._send, osc.Message("/ITL/scene","fullscreen", 1))
        reactor.callLater(0.01,self.oscore._send, osc.Message("/ITL/scene","foreground"))
        t = 0.05
        for i in range(0,150):
            reactor.callLater(t,self.oscore._send, osc.Message("/ITL/scene","color", 255-i,255-i, 255-i))
            t += 0.05
        reactor.callLater(12.0,self.oscore._send, osc.Message("/ITL/scene/text","del"))
        reactor.callLater(2.0,self.greet)
        reactor.callLater(14.0,self.make_recitation)
        reactor.callLater(14.0, self.make_mood)
        reactor.callLater(14.0, self.make_instructions)
        reactor.callLater(14.0, self.make_durations)
        reactor.callLater(14.0, self.make_glissandis)
        reactor.callLater(14.0, self.make_interactions)
        reactor.callLater(14.0, self.make_envelopes)
        reactor.callLater(14.0, self.make_melos)
        reactor.callLater(14.0, self.make_rhythms)
        reactor.callLater(14.0, self.make_poems)
        self.oscore.run()
        # move to INSCore's __init__?
   
    def greet(self):
        print("Entered greet")
        reactor.callLater(0.1,self._hello)
        print("Called callLater?")

    def _hello(self):
        print("Entered _hello")
        self.oscore._send(osc.Message("/ITL/scene/*","del"))
        self.oscore._send(osc.Message("/ITL/scene/text","set","txt","Welcome to Transience\nby Sandeep Bhagwati"))
        self.oscore._send(osc.Message("/ITL/scene/text", "scale", 4.0))
        #def _stop():
        #    reactor.stop()
        #reactor.callLater(20.0,_stop)

    def make_mood(self):
        #self.mood.image()
        self.oscore._send(self.mood.image())
        self.oscore._send(self.mood.get_x())
        self.oscore._send(self.mood.get_y())
        #self.oscore._send(self.mood.watch_mouse_enter())

    def make_recitation(self):
        #self.recitation.image()
        self.oscore._send(self.recitation.image())
        self.oscore._send(self.recitation.get_x())
        self.oscore._send(self.recitation.get_y())
        self.oscore._send(self.recitation.watch_mouse_enter())

    def make_poems(self):
        #self.poems.image()
        self.oscore._send(self.poems.image())
        self.oscore._send(self.poems.get_x())
        self.oscore._send(self.poems.get_y())
        #self.oscore._send(self.poems.watch_mouse_enter())

    def make_rhythms(self):
        #self.rhythms.image()
        self.oscore._send(self.rhythms.image())
        self.oscore._send(self.rhythms.get_x())
        self.oscore._send(self.rhythms.get_y())
        #self.oscore._send(self.rhythms.watch_mouse_enter())

    def make_melos(self):
        #self.melos.image()
        self.oscore._send(self.melos.image())
        self.oscore._send(self.melos.get_x())
        self.oscore._send(self.melos.get_y())
        #self.oscore._send(self.melos.watch_mouse_enter())

    def make_envelopes(self):
        #self.envelopes.image()
        self.oscore._send(self.envelopes.image())
        self.oscore._send(self.envelopes.get_x())
        self.oscore._send(self.envelopes.get_y())
        #self.oscore._send(self.envelopes.watch_mouse_enter())

    def make_interactions(self):
        #self.interactions.image()
        self.oscore._send(self.interactions.image())
        self.oscore._send(self.interactions.get_x())
        self.oscore._send(self.interactions.get_y())
        #self.oscore._send(self.interactions.watch_mouse_enter())

    def make_glissandis(self):
        #self.glissandis.image()
        self.oscore._send(self.glissandis.image())
        self.oscore._send(self.glissandis.get_x())
        self.oscore._send(self.glissandis.get_y())
        #self.oscore._send(self.glissandis.watch_mouse_enter())

    def make_durations(self):
        #self.durations.image()
        self.oscore._send(self.durations.image())
        self.oscore._send(self.durations.get_x())
        self.oscore._send(self.durations.get_y())
        #self.oscore._send(self.durations.watch_mouse_enter())

    def make_instructions(self):
        #self.instructions.image()
        self.oscore._send(self.instructions.image())
        self.oscore._send(self.instructions.get_x())
        self.oscore._send(self.instructions.get_y())
        #self.oscore._send(self.instructions.watch_mouse_enter())

    def change_recitation(self):
        self.recitation.number = 4
        self.oscore._send(self.recitation.image())


## if __name__ == "__main__":
##     app = Application()
##     print("will run application!")
##     app.run()
