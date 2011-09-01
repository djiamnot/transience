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
The Runner function.
"""
from optparse import OptionParser
from transience import __version__
#from transience import server
from transience import application
from transience import configuration
import os
import sys
import time

DESCRIPTION = "Python control application for Transience score"

def run():
    """
    Runs the application.
    """
    parser = OptionParser(usage="%prog [options]", version="%prog " + __version__, description=DESCRIPTION)
    parser.add_option("-v", "--verbose", action="store_true", help="Makes the output verbose.")
    parser.add_option("-p", "--osc-send-port", type="int", default=7000, help="UDP port to send OSC to INScore.  Default is 7000")
    (options, args) = parser.parse_args()
    config = configuration.Configuration()
    if options.verbose:
        config.verbose = True
    if options.osc_send_port:
        config.osc_send_port = options.osc_send_port

    app = application.Application()

