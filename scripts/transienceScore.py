#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Transience
# Copyright (C) 2011 Michal Seta
# All rights reserved.
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
# along with Pyospat.  If not, see <http://www.gnu.org/licenses/>.

"""
Transience executable script.
Calls transience.runner.run()
"""

import os
import sys

SCRIPTS_DIR = "scripts"

def _is_in_devel():
    d = os.path.split(os.path.dirname(os.path.abspath(__file__)))[1]
    return d == SCRIPTS_DIR

if __name__ == "__main__":
    if _is_in_devel():
        d = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
        sys.path.insert(0, d)
        os.environ["PATH"] += ":%s" % (os.path.join(d, SCRIPTS_DIR))
    from transience import runner
    runner.run()
