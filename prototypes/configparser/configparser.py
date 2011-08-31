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
Configuration parser.
Configuration consists mainly of content to be displayed on each "page"
of the score.
"""
import time
import os
import sys
from ConfigParser import SafeConfigParser
import random

class PrefParser(object):
    """
    Parses ~/.transiencerc and extracts the elements needed for display(s)
    """
    def __init__(self, file_name=None):
        """
        @throw IOError if file not found
        """
        if file_name is None:
            file_name = os.path.expanduser("~/.transiencerc")
        self._file_name = file_name
        self._parse()

    def _parse(self):
        if not os.path.exists(self._file_name):
            self._default()
        parser = SafeConfigParser()
        parser.read(self._file_name)
        for section_name in parser.sections():
            print("Section: {}".format(section_name))
            print("   Options: {}".format(parser.options(section_name)))
            for name, value in parser.items(section_name):
                print ("      {} : {}".format(name, value))

    def _default(self):
        """
        write a default configuration file
        """
        # TODO: replace the random for something more meaningful
        config_file = os.path.expanduser("~/.transiencerc")
        parser = SafeConfigParser()
        for i in range (9):
            page = "page {}".format(i)
            parser.add_section(page)
            parser.set(page, "recitation", "{}".format(random.randint(0,9)))
            parser.set(page, "mood", "{}".format(random.randint(0,9)))
            parser.set(page, "instructions", "{}".format(random.randint(0,9)))
            parser.set(page, "durations", "{}".format(random.randint(0,9)))
            parser.set(page, "glissandis", "{}".format(random.randint(0,9)))
            parser.set(page, "interactions", "{}".format(random.randint(0,9)))
            parser.set(page, "envelopes", "{}".format(random.randint(0,9)))
            parser.set(page, "melos", "{}".format(random.randint(0,9)))
            parser.set(page, "rhythms", "{}".format(random.randint(0,9)))
            parser.set(page, "poems", "{}".format(random.randint(0,9)))

        with open(config_file,"w") as f:
            parser.write(f)

class TransienceServer(object):
    """
    Starts the transience application
    """
    def __init__(self):
        parser = PrefParser()
        self._running = False

    def run(self):
        """
        Runs blocking mainloop
        """
        self._running = True
        try:
            while self._running:
                time.sleep(0.1)
        except KeyboardInterrupt, e:
            print("Interrupted")

    def stop(self):
        """
        Stops the main loop
        """
        self._running = False

if __name__ == "__main__":
    server = TransienceServer()
    server.run()
