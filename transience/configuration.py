#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Transience
# Copyright (C) 2011 Alexandre Quessy
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
The Configuration class.
"""

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
        inscore_port = parser.add_section("inscore_port")
        parser.set(inscore_port("7000"))
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

class Configuration(object):
    """
    Configuration for the application.
    """
    def __init__(self):
        self.verbose = False
        self.osc_send_port = 7000

