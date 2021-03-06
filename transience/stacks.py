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
import random
import sys
import time

from twisted.internet import reactor
from txosc import osc

from transience import score
from transience import inscore
from transience import conf_ui
from transience import midi


# These instances are hardcoded based on manual placement
# of these elements.

recitations = score.Element(
    x = 0.0202312,
    y = -0.308,
    URI="recitations",
    path="recitations",
    number=1,
    scale = 1.325)

moods = score.Element(
#    x = 0.989840,
    x = 1.018,
    y = -0.644509,
    URI="moods",
    path="moods",
    number=1,
    scale = 0.95
    )

instructions = score.Element(
    x = -0.852601,
    y = -0.643509,
    URI="instructions",
    path="instructions",
    number=1,
    scale = 1.04
    )

durations = score.Element(
    x = 0.849711,
    y = 0.852601,
    URI="durations",
    path="durations",
    number=1,
    scale = 1
    )

glissandis = score.Element(
    x = -0.713873,
    y = -0.306358,
    URI="glissandis",
    path="glissandis",
    number=1,
    scale = 0.715)

interactions = score.Element(
    x = 0.005,
    y = -0.642628,
    URI="interactions",
    path="interactions",
    number=1,
    scale = 0.87)

envelopes = score.Element(
    x = 0.895954,
    y = -0.308249,
    URI="envelopes",
    path="envelopes",
    number=1,
    scale = 0.755)

melos = score.Element(
    x = 0.164740,
    y = 0.111,
    URI="melos",
    path="melos",
    number=1,
    scale = 0.85)

rhythms = score.Element(
    x = 0.164740,
    y = 0.523121,
    URI="rhythms",
    path="rhythms",
    number=1,
    scale = 0.856)

## blank = score.Element(
##     x = 0.0812772,
##     y = 0.853411,
##     URI="blank",
##     path="blank",
##     number=0,
##     scale = 0.7,
##     show = 1)

poems = score.Element(
    x = -1.32366,
    y = 0.185776,
    URI="poems",
    path="poems",
    number=101,
    scale = 0.6)

# TODO: deal with etexts as well!
jtexts = score.Element(
    x = 0.135838,
    y = 0.852601,
    URI="jtexts",
    path="jtexts",
    number=101,
    scale = 1.,
    show = 1)

etexts = score.Element(
    x = -0.721,
    y = 0.852601,
    URI="etexts",
    path="etexts",
    number=101,
    scale = 1.0,
    show = 1)

page_sequence = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# Shuffle the page sequence every time we start application.
random.shuffle(page_sequence)
print("*** PAGE SEQENCE")
print(page_sequence)

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
        # TODO: does this have to be a class variable?
        self.page_iter = iter(page_sequence)
        self.page = 0
        self.page_count = 0
        self.screen_grab_directory = "/tmp/transience"
        self.elements_list = [
            'recitations',
            'moods',
            'instructions',
            'durations',
            'glissandis',
            'interactions',
            'envelopes',
            'melos',
            'rhythms',
            'etexts',
            'poems',
            'jtexts',
            ]
        # Set up the page layout:
        self.durations = durations
        self.envelopes = envelopes
        self.glissandis = glissandis
        self.instructions = instructions
        self.interactions = interactions
        #self.blank = blank
        self.jtexts = jtexts
        self.etexts = etexts
        self.melos = melos
        self.moods = moods
        self.poems = poems
        self.rhythms = rhythms
        self.recitations = recitations

        # set up the stacks
        self.durations.stack_sequence = self.arrangement['durations']
        self.envelopes.stack_sequence = self.arrangement['envelopes']
        self.glissandis.stack_sequence = self.arrangement['glissandis']
        self.instructions.stack_sequence = self.arrangement['instructions']
        self.interactions.stack_sequence = self.arrangement['interactions']
        #all poems should be the same
        self.jtexts.stack_sequence = self.arrangement['etexts'] 
        self.etexts.stack_sequence = self.arrangement['etexts']
        self.melos.stack_sequence = self.arrangement['melos']
        self.moods.stack_sequence = self.arrangement['moods']
        self.poems.stack_sequence = self.arrangement['etexts']
        self.rhythms.stack_sequence = self.arrangement['rhythms']
        self.recitations.stack_sequence = self.arrangement['recitations']

        self.make_all_stacks()
        self.greet()
        reactor.callLater(12.0, self.set_score_page)
        reactor.callLater(1.0, self.next_page)
        reactor.callLater(0.1, self.set_screen_grab_dir)
        reactor.callLater(14.1, self.grab_screen)

        if self.arrangement['midi'] > -1:
            self.midi_manager = midi.MidiIn(self.arrangement['midi'])
            self.midi_manager.register_callback(self._cb_midi_event)
            try:
                self.midi_manager.start()
            except midi.NotConnectedError, e:
                print("Could not setup MIDI device %d" % ())

        self.oscore.run()
        ## # set stacks to first iteration
        ## self.durations.advance_stack()
        ## self.envelopes.advance_stack()
        ## self.glissandis.advance_stack()
        ## self.instructions.advance_stack()
        ## self.interactions.advance_stack()
        ## self.jtexts.advance_stack()
        ## self.melos.advance_stack()
        ## self.moods.advance_stack()
        ## self.poems.advance_stack()
        ## self.rhythms.advance_stack()
        ## self.recitations.advance_stack()
    
    def _cb_midi_event(self, event):
        """
        Called when a MIDI event occurs
        """
        MIDI_CTRL = 176
        if event[0][0] == MIDI_CTRL:
            if event[0][2] > 0:
                self.handle_page_turn()
                #print("MIDI pedal down")
                #self.set_score_page()
                #reactor.callLater(1.0,self.next_page)
                #reactor.callLater(1.1,self.grab_screen)
                #self.display_count()
                #print("Current page is: ", self.page_count)
                #self.page_count += 1


    def make_all_stacks(self):
        """
        Make all stacks
        """
        self.durations.make_stack()
        self.envelopes.make_stack()
        self.glissandis.make_stack()
        self.instructions.make_stack()
        self.interactions.make_stack()
        self.jtexts.make_stack()
        self.etexts.make_stack()
        self.melos.make_stack()
        self.moods.make_stack()
        self.poems.make_stack()
        self.rhythms.make_stack()
        self.recitations.make_stack()

    def next_page(self):
        """
        This method advances some elements (depending on which 'page' we are on)
        and highlites the elements that have been advanced. The actual switching
        of the images from the 'stack' happens when L{set_score_page} is called.
        """
        if page_sequence[self.page] == 0:
            self.envelopes.advance_stack()
            self.oscore._send(self.envelopes.set_colorize())
            self.glissandis.advance_stack()
            self.oscore._send(self.glissandis.set_colorize())
            self.rhythms.advance_stack()
            self.oscore._send(self.rhythms.set_colorize())
            self.melos.advance_stack()
            self.oscore._send(self.melos.set_colorize())
        elif page_sequence[self.page] == 1:
            # TODO: Japanese/English/None text changes here
            self.recitations.advance_stack()
            self.oscore._send(self.recitations.set_colorize())
            self.moods.advance_stack()
            self.oscore._send(self.moods.set_colorize())
            self.durations.advance_stack()
            self.oscore._send(self.durations.set_colorize())
        elif page_sequence[self.page] == 2:
            # TODO: Japanese/English/None text changes here
            self.envelopes.advance_stack()
            self.glissandis.advance_stack()
            self.moods.advance_stack()
            self.interactions.advance_stack()
            self.jtexts.advance_stack()
            self.etexts.advance_stack()
            self.poems.advance_stack()
            self.rhythms.advance_stack()
#            self.decide_language()
            self.oscore._send(self.envelopes.set_colorize())
            self.oscore._send(self.glissandis.set_colorize())
            self.oscore._send(self.moods.set_colorize())
            self.oscore._send(self.interactions.set_colorize())
            self.oscore._send(self.jtexts.set_colorize())
            self.oscore._send(self.etexts.set_colorize())
            #self.oscore._send(self.poems.set_colorize())
            self.oscore._send(self.rhythms.set_colorize())
        elif page_sequence[self.page] == 3:
            self.envelopes.advance_stack()
            self.glissandis.advance_stack()
            self.moods.advance_stack()
            self.interactions.advance_stack()
            self.durations.advance_stack()
            self.jtexts.advance_stack()
            self.etexts.advance_stack()
            self.poems.advance_stack()
            self.melos.advance_stack()
#            self.decide_language()
            self.oscore._send(self.envelopes.set_colorize())
            self.oscore._send(self.glissandis.set_colorize())
            self.oscore._send(self.moods.set_colorize())
            self.oscore._send(self.interactions.set_colorize())
            self.oscore._send(self.jtexts.set_colorize())
            self.oscore._send(self.etexts.set_colorize())
            #self.oscore._send(self.poems.set_colorize())
            self.oscore._send(self.melos.set_colorize())
        elif page_sequence[self.page] == 4:
            self.recitations.advance_stack()
            self.envelopes.advance_stack()
            self.interactions.advance_stack()
            self.rhythms.advance_stack()
            self.oscore._send(self.recitations.set_colorize())
            self.oscore._send(self.envelopes.set_colorize())
            self.oscore._send(self.interactions.set_colorize())
            self.oscore._send(self.rhythms.set_colorize())
        elif page_sequence[self.page] == 5:
            # TODO: Japanese/English/None text changes here
            self.recitations.advance_stack()
            self.moods.advance_stack()
            self.instructions.advance_stack()
            self.durations.advance_stack()
            self.jtexts.advance_stack()
            self.etexts.advance_stack()
            self.poems.advance_stack()
            self.melos.advance_stack()
            self.oscore._send(self.recitations.set_colorize())
            self.oscore._send(self.moods.set_colorize())
            self.oscore._send(self.instructions.set_colorize())
            self.oscore._send(self.durations.set_colorize())
            self.oscore._send(self.jtexts.set_colorize())
            self.oscore._send(self.etexts.set_colorize())
            #self.oscore._send(self.poems.set_colorize())
            self.oscore._send(self.melos.set_colorize())
        elif page_sequence[self.page] == 6:
            # TODO: Japanese/English/None text changes here
            self.envelopes.advance_stack()
            self.glissandis.advance_stack()
            self.instructions.advance_stack()
            self.interactions.advance_stack()
            self.rhythms.advance_stack()
            self.melos.advance_stack()
#            self.decide_language()
            self.oscore._send(self.envelopes.set_colorize())
            self.oscore._send(self.glissandis.set_colorize())
            self.oscore._send(self.instructions.set_colorize())
            self.oscore._send(self.interactions.set_colorize())
            self.oscore._send(self.rhythms.set_colorize())
            self.oscore._send(self.melos.set_colorize())
            #self.oscore._send(self.poems.set_colorize())
            self.oscore._send(self.etexts.set_colorize())
            self.oscore._send(self.jtexts.set_colorize())
        elif page_sequence[self.page] == 7:
            self.recitations.advance_stack()
            self.envelopes.advance_stack()
            self.moods.advance_stack()
            self.interactions.advance_stack()
            self.durations.advance_stack()
            self.jtexts.advance_stack()
            self.etexts.advance_stack()
            self.poems.advance_stack()
#            self.decide_language()
            self.oscore._send(self.recitations.set_colorize())
            self.oscore._send(self.envelopes.set_colorize())
            self.oscore._send(self.moods.set_colorize())
            self.oscore._send(self.interactions.set_colorize())
            self.oscore._send(self.durations.set_colorize())
            self.oscore._send(self.jtexts.set_colorize())
            self.oscore._send(self.etexts.set_colorize())
        elif page_sequence[self.page] == 8:
            # TODO: Japanese/English/None text changes here
            self.recitations.advance_stack()
            self.glissandis.advance_stack()
            self.moods.advance_stack()
            self.instructions.advance_stack()
            self.durations.advance_stack()
            self.rhythms.advance_stack()
            self.melos.advance_stack()
            self.poems.advance_stack()
            self.jtexts.advance_stack()
            self.etexts.advance_stack()
            self.oscore._send(self.recitations.set_colorize())
            self.oscore._send(self.glissandis.set_colorize())
            self.oscore._send(self.moods.set_colorize())
            self.oscore._send(self.instructions.set_colorize())
            self.oscore._send(self.durations.set_colorize())
            self.oscore._send(self.rhythms.set_colorize())
            self.oscore._send(self.melos.set_colorize())
            #self.oscore._send(self.poems.set_colorize())
            self.oscore._send(self.etexts.set_colorize())
            self.oscore._send(self.jtexts.set_colorize())
                
    def decide_language(self):
        """
        Show English or Japanese text or none, accoridng to random choice.
        If it is to be japanese, show both. Else show either only english or nothing.
        """
        choice = random.randint(1, 2)
        print("The choice is: ", choice)
        if choice == 0:
            self.etexts.show = 0
            self.jtexts.show = 0
        elif choice == 1:
            self.etexts.show = 1
            self.jtexts.show = 0
        else:
            self.etexts.show = 1
            self.jtexts.show = 1

    def display_count(self):
        self.oscore._send(osc.Message("/ITL/scene/count","set", "txt",
                                      "Page: {}".format(self.page_count+1)))
        self.oscore._send(osc.Message("/ITL/scene/count","color", 100, 100, 100))
        self.oscore._send(osc.Message("/ITL/scene/count","x", 1.3))
        self.oscore._send(osc.Message("/ITL/scene/count","y", 0.97))
        self.oscore._send(osc.Message("/ITL/scene/count","scale", 1.8))

    def mouse_handler(self, message, address):
        """
        Handle mouse clicks in visible elements
        """
        self.iterate_page(message)
        if message.getValues()[0] == 'quitB' and message.getValues()[1] == "clicked":
            print("Quit invoked!  Going for sys.exit")
            self.oscore._send(osc.Message("/ITL", "quit"))
            self.oscore.stop()
        if message.getValues()[0] == "conf_ui" and message.getValues()[1] == "clicked":
            # Open the configuration scene
            conf = conf_ui.ConfScreen(self.configuration, self.oscore)

    def iterate_page(self, message):
        if message.getValues()[0] in self.elements_list and message.getValues()[1] == 'clicked':
            self.handle_page_turn()
            
    def handle_page_turn(self):
        if self.page_count == 0:
            self.page = self.page_iter.next()
            self.make_all_stacks()
            #self.set_score_page()
            self.page_iter = iter(page_sequence)
            reactor.callLater(1.0,self.next_page)
        if self.page_count < 8:
            try:
                if self.page_count != 0:
                    self.page = self.page_iter.next()
                self.set_score_page()
                reactor.callLater(1.0,self.next_page)
                reactor.callLater(1.1,self.grab_screen)
                self.display_count()
                print("Current page is: ", self.page_count)
                self.page_count += 1
            except StopIteration:
                print("||||||||| END OF PIECE |||||||||")
                #self.page_count += 1
                #self.display_count()
                #self.oscore._send(osc.Message("/ITL/scene/*","del"))
                #self.page_iter = iter(page_sequence)
                self.page_count = 0
                self.make_all_stacks()
                self.page_iter = iter(page_sequence)
                reactor.callLater(1.0,self.next_page)
        else:
            #self.page = self.page_iter.next()
            self.set_score_page()
            reactor.callLater(1.0,self.next_page)
            reactor.callLater(1.1,self.grab_screen)
            self.display_count()
            self.oscore._send(osc.Message("/ITL/scene/count",
                                "color", 255, 100, 100))
            self.page_count = 0
            self.set_screen_grab_dir()

    def grab_screen(self):
        print("The screen grab dir is: {}".format(self.screen_grab_directory))
        full_screen_grab_path = self.screen_grab_directory + "/page"+str(self.page_count + 1)
        self.oscore._send(osc.Message(
            "/ITL/scene","export",
            "{}.png".format(full_screen_grab_path)))

    def set_screen_grab_dir(self):
        #self.screen_grab_directory = "/tmp/"+time.strftime(
        #                                    "transience-%Y%m%d-%H.%M.%S")
        final_dir = time.strftime("transience-%Y%m%d-%H.%M.%S")
        self.screen_grab_directory = os.path.join("/tmp", final_dir)
        if not os.path.exists(self.screen_grab_directory):
            try:
                os.makedirs(self.screen_grab_directory)
                print("Created a directory: {}".format(self.screen_grab_directory))
            except OSError, e:
                print(e)


    def greet(self):
        print("Entered greet")
        reactor.callLater(0.0,self.oscore._send,
                          osc.Message("/ITL/scene/*","del"))
        reactor.callLater(0.02,self.oscore._send,
                          osc.Message("/ITL/scene","width", 2.64583))
        reactor.callLater(0.02,self.oscore._send,
                          osc.Message("/ITL/scene","height", 1.80990))
        reactor.callLater(0.01,self.oscore._send,
                          osc.Message("/ITL/scene","foreground"))
        t = 0.05
        for i in range(0,100):
            reactor.callLater(
                t,
                self.oscore._send,
                osc.Message("/ITL/scene","color", 100-i, 100-i, 100-i, 255))
            t += 0.05
        reactor.callLater(12.0,self.oscore._send,
                          osc.Message("/ITL/scene/text","del"))
        reactor.callLater(0.01,self._hello)

    def _hello(self):
        self.oscore._send(osc.Message("/ITL/scene/*","del"))
        self.oscore._send(osc.Message("/ITL/scene/text","set","txt","Transience\nby Sandeep Bhagwati"))
        self.oscore._send(osc.Message("/ITL/scene/text", "scale", 4.0))
        self.oscore._send(osc.Message("/ITL/scene/text", "color", 100, 100, 100))
        #def _stop():
        #    reactor.stop()
        #reactor.callLater(20.0,_stop)

    def make_icons(self):
        enter_path = score.MEDIA_PATH+"icons/enter.svg"
        exit_path = score.MEDIA_PATH+"icons/exit.svg"
        self.oscore._send(osc.Message("/ITL/scene/enter", "set", "svgf", enter_path))
        self.oscore._send(osc.Message("/ITL/scene/enter", "x", -1.33237))
        self.oscore._send(osc.Message("/ITL/scene/enter", "y", -0.780347))
        self.oscore._send(osc.Message("/ITL/scene/enter", "scale", 0.4))
        self.oscore._send(osc.Message("/ITL/scene/exit", "set", "svgf", exit_path))
        self.oscore._send(osc.Message("/ITL/scene/exit", "x", 1.32948))
        self.oscore._send(osc.Message("/ITL/scene/exit", "y", 0.843931))
        self.oscore._send(osc.Message("/ITL/scene/exit", "scale", 0.4))

    def make_quit_button(self):
        ## quitbutton = score.Button(x=-1., y=-1., URI="quitB", txt="Quit")
        ## self.oscore._send(quitbutton.doit())
        ## self.oscore._send(quitbutton.watch_mouse_down())
        ## self.oscore._send(quitbutton.set_color(255, 0, 0))
        URI = "/ITL/scene/quitB"
        txt = "QUIT"
        self.oscore._send(osc.Message(URI, "set", "txt", txt))
        self.oscore._send(osc.Message(URI, "x", -1.45123))
        self.oscore._send(osc.Message(URI, "y", -0.947424))
        self.oscore._send(osc.Message(URI, "xorigin", -1))
        self.oscore._send(osc.Message(URI, "yorigin", 1))
        if sys.platform == "darwin":
            self.oscore._send(osc.Message(URI, "scale", 1.0))
        else:
            self.oscore._send(osc.Message(URI, "scale", 2.0))
        self.oscore._send(osc.Message(URI, "color", 100, 100, 100))
        self.oscore._send(osc.Message(URI,"watch","mouseUp","127.0.0.1:7001/mouse", "quitB", "clicked"))

    def make_conf_button(self):
        ## quitbutton = score.Button(x=-1., y=-1., URI="quitB", txt="Quit")
        ## self.oscore._send(quitbutton.doit())
        ## self.oscore._send(quitbutton.watch_mouse_down())
        ## self.oscore._send(quitbutton.set_color(255, 0, 0))
        URI = "/ITL/scene/conf_ui"
        txt = "Configure Score"
        self.oscore._send(osc.Message(URI, "set", "txt", txt))
        self.oscore._send(osc.Message(URI, "x", 1.25123))
        self.oscore._send(osc.Message(URI, "y", -0.977424))
        self.oscore._send(osc.Message(URI, "xorigin", 0))
        self.oscore._send(osc.Message(URI, "yorigin", 0))
        if sys.platform == "darwin":
            self.oscore._send(osc.Message(URI, "scale", 1.0))
        else:
            self.oscore._send(osc.Message(URI, "scale", 2.0))
        self.oscore._send(osc.Message(URI, "color", 100, 100, 100))
        self.oscore._send(osc.Message(URI,"watch","mouseUp",
                                      "127.0.0.1:7001/mouse", "conf_ui", "clicked"))

    def make_moods(self):
        #self.moods.image()
        self.oscore._send(self.moods.image())
        self.oscore._send(self.moods.get_x())
        self.oscore._send(self.moods.get_y())
        self.oscore._send(self.moods.scale_element())
        self.oscore._send(self.moods.watch_mouse_down())
        self.oscore._send(self.moods.reset_colorize())
        #self.oscore._send(self.moods.watch_mouse_enter())

    def make_recitations(self):
        #self.recitations.image()
        self.oscore._send(self.recitations.image())
        self.oscore._send(self.recitations.get_x())
        self.oscore._send(self.recitations.get_y())
        self.oscore._send(self.recitations.scale_element())
        self.oscore._send(self.recitations.watch_mouse_down())
        self.oscore._send(self.recitations.reset_colorize())
        #self.oscore._send(self.recitations.watch_mouse_enter())

    def make_rhythms(self):
        #self.rhythms.image()
        self.oscore._send(self.rhythms.image())
        self.oscore._send(self.rhythms.get_x())
        self.oscore._send(self.rhythms.get_y())
        self.oscore._send(self.rhythms.scale_element())
        self.oscore._send(self.rhythms.watch_mouse_down())
        self.oscore._send(self.rhythms.reset_colorize())
        #self.oscore._send(self.rhythms.watch_mouse_enter())

    def make_melos(self):
        #self.melos.image()
        self.oscore._send(self.melos.image())
        self.oscore._send(self.melos.get_x())
        self.oscore._send(self.melos.get_y())
        self.oscore._send(self.melos.scale_element())
        self.oscore._send(self.melos.watch_mouse_down())
        self.oscore._send(self.melos.reset_colorize())
        #self.oscore._send(self.melos.watch_mouse_enter())

    def make_envelopes(self):
        #self.envelopes.image()
        self.oscore._send(self.envelopes.image())
        self.oscore._send(self.envelopes.get_x())
        self.oscore._send(self.envelopes.get_y())
        #self.oscore._send(self.envelopes.shear(2.0, 1.0))
        self.oscore._send(self.envelopes.scale_element())
        self.oscore._send(self.envelopes.watch_mouse_down())
        self.oscore._send(self.envelopes.reset_colorize())
        #self.oscore._send(self.envelopes.watch_mouse_enter())

    def make_interactions(self):
        #self.interactions.image()
        self.oscore._send(self.interactions.image())
        self.oscore._send(self.interactions.get_x())
        self.oscore._send(self.interactions.get_y())
        self.oscore._send(self.interactions.scale_element())
        self.oscore._send(self.interactions.watch_mouse_down())
        self.oscore._send(self.interactions.reset_colorize())
        #self.oscore._send(self.interactions.watch_mouse_enter())

    def make_glissandis(self):
        #self.glissandis.image()
        self.oscore._send(self.glissandis.image())
        self.oscore._send(self.glissandis.get_x())
        self.oscore._send(self.glissandis.get_y())
        self.oscore._send(self.glissandis.scale_element())
        self.oscore._send(self.glissandis.watch_mouse_down())
        self.oscore._send(self.glissandis.reset_colorize())
        #self.oscore._send(self.glissandis.watch_mouse_enter())

    def make_durations(self):
        #self.durations.image()
        self.oscore._send(self.durations.image())
        self.oscore._send(self.durations.get_x())
        self.oscore._send(self.durations.get_y())
        self.oscore._send(self.durations.scale_element())
        self.oscore._send(self.durations.watch_mouse_down())
        self.oscore._send(self.durations.reset_colorize())
        #self.oscore._send(self.durations.watch_mouse_enter())

    def make_instructions(self):
        #self.instructions.image()
        self.oscore._send(self.instructions.image())
        self.oscore._send(self.instructions.get_x())
        self.oscore._send(self.instructions.get_y())
        self.oscore._send(self.instructions.scale_element())
        self.oscore._send(self.instructions.watch_mouse_down())
        self.oscore._send(self.instructions.reset_colorize())
        #self.oscore._send(self.instructions.watch_mouse_enter())

    def make_jtexts(self):
        #self.jtexts.image()
        self.oscore._send(self.jtexts.image())
        self.oscore._send(self.jtexts.get_x())
        self.oscore._send(self.jtexts.get_y())
        self.oscore._send(self.jtexts.scale_element())
        self.oscore._send(self.jtexts.watch_mouse_down())
        self.oscore._send(self.jtexts.reset_colorize())
        self.oscore._send(self.jtexts.set_show())
        #self.oscore._send(self.jtexts.watch_mouse_enter())

    def make_etexts(self):
        #self.jtexts.image()
        self.oscore._send(self.etexts.image())
        self.oscore._send(self.etexts.get_x())
        self.oscore._send(self.etexts.get_y())
        self.oscore._send(self.etexts.scale_element())
        self.oscore._send(self.etexts.watch_mouse_down())
        self.oscore._send(self.etexts.reset_colorize())
        self.oscore._send(self.etexts.set_show())
        #self.oscore._send(self.etexts.watch_mouse_enter())

    def make_poems(self):
        #self.poems.image()
        self.oscore._send(self.poems.image())
        self.oscore._send(self.poems.get_x())
        self.oscore._send(self.poems.get_y())
        self.oscore._send(self.poems.scale_element())
        self.oscore._send(self.poems.watch_mouse_down())
        self.oscore._send(self.poems.reset_colorize())
        #self.oscore._send(self.poems.watch_mouse_enter())

    def make_blank(self):
        #self.blank.image()
        self.oscore._send(self.blank.image())
        self.oscore._send(self.blank.get_x())
        self.oscore._send(self.blank.get_y())
        self.oscore._send(self.blank.scale_element())
        self.oscore._send(self.blank.watch_mouse_down())
        self.oscore._send(self.blank.reset_colorize())
        #self.oscore._send(self.blank.watch_mouse_enter())

    def change_recitations(self):
        self.recitations.number = 4
        self.oscore._send(self.recitations.image())

    def set_score_page(self):
        """
        This method makes everything happen on the screen. Sends OSC messages
        with page contents to INScore
        """
        print("*** set_score_page goes here")
        ## self.instructions.number = self.instructions.stack_sequence[self.current_instructions]
        ## self.moods.number = self.moods.stack_sequence[self.current_moods]
        ## self.recitations.number = self.recitations.stack_sequence[self.current_recitations]
        ## self.durations.number = self.durations.stack_sequence[self.current_durations]
        ## self.glissandis.number = self.glissandis.stack_sequence[self.current_glissandis]
        ## self.interactions.number = self.interactions.stack_sequence[self.current_interactions]
        ## self.envelopes.number = self.envelopes.stack_sequence[self.current_envelopes]
        ## self.melos.number = self.melos.stack_sequence[self.current_melos]
        ## self.rhythms.number = self.rhythms.stack_sequence[self.current_rhythms]
        ## self.poems.number = self.poems.stack_sequence[self.current_poems]
        ## self.jtexts.number = self.poems.number
        ## self.etexts.nyumber = self.poems.number
        reactor.callLater(0.01, self.make_instructions)
        reactor.callLater(0.01, self.make_glissandis)
        reactor.callLater(0.01, self.make_interactions)
        reactor.callLater(0.01, self.make_moods)
        reactor.callLater(0.01, self.make_envelopes)
        reactor.callLater(0.01, self.make_melos)
        reactor.callLater(0.01, self.make_rhythms)
        #reactor.callLater(0.01, self.make_blank)
        reactor.callLater(0.01, self.make_poems)
        reactor.callLater(0.01, self.make_jtexts)
        reactor.callLater(0.01, self.make_etexts)
        reactor.callLater(0.01, self.make_quit_button)
        reactor.callLater(0.01, self.make_conf_button)
        reactor.callLater(0.01,self.make_recitations)
        reactor.callLater(0.01, self.make_durations)
        reactor.callLater(2.0, self.decide_language)
        reactor.callLater(0.02, self.make_icons)

