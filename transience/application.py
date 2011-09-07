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


class Application(object):
    """
    Starts the transience application
    """
    def __init__(self):
        # TODO: move this one to inscore.py
        #parser = PrefParser()
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
    app = Application()
    app.run()
