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
The Configuration class.
"""
import random
import os
import shutil
import time

from ConfigParser import SafeConfigParser

import conf_matrix

def save_conf(dict):
    config_file = os.path.expanduser("~/.transiencerc")
    parser = SafeConfigParser()
    for key in dict:
        parser.add_section(key)
        parser.set(key, 'sequence', "{}".format(dict[key]))
    with open(config_file,"w") as f:
        parser.write(f)

def save_backup_conf(directory="/var/tmp/transcience"):
    file_name = time.strftime("transiencerc-%Y%m%d-%H:%M:%S")
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError, e:
            print(e)
    full_path = os.path.join(directory, file_name)
    try:
        shutil.copy2(os.path.expanduser("~/.transiencerc"), full_path)
    except Error, e:
        print(e)
        
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
        self.elements = {}
        self._parse()
        

    def _parse(self):
        if not os.path.exists(self._file_name):
            self._default()
        parser = SafeConfigParser()
        parser.read(self._file_name)
        element = {}
        for section_name in parser.sections():
            print("Section: {}".format(section_name))
            #print("   Options: {}".format(parser.options(section_name)))
            for name, value in parser.items(section_name):
                print ("      {} : {}".format(name, value))
                if section_name == 'midi':
                    element[section_name] = int(value)
                else:
                    element[section_name] = self.read_sequence(value)
            print("Element is %s: "%(element))
            self.elements = element
        print("Contents of elements: ", self.elements)
        
    def read_sequence(self, elems):
        """
        Read a python list formatted as string and turn it into a real
        python list
        @param elems: string in the form of [1, 2, 3 ...]
        @return: list of chars
        """
        my_list = elems[1:-1]
        my_list = my_list.split(",")
        # Aww...  let's strip some whitespace...
        # TODO: COnfigParser/writer seems to be inserting whitespace... check.
        new_list = []
        for s in my_list:
            new_list.append(s.replace(' ',''))
        my_list = new_list
        return my_list

    def _default(self):
        """
        write a default configuration file
        """
        path = conf_matrix.paths
        config_file = os.path.expanduser("~/.transiencerc")
        parser = SafeConfigParser()
        elements = [
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
        for element in elements:
            parser.add_section(element)
            parser.set(element, 'sequence', "{}".format(path[random.randint(0,4)]))
        parser.add_section('midi')
        parser.set('midi', 'device', '-1')
        with open(config_file,"w") as f:
            parser.write(f)

class Configuration(object):
    """
    Configuration for the application.
    """
    def __init__(self):
        self.verbose = False
        self.osc_send_port = 7000
        self.parser = PrefParser()

