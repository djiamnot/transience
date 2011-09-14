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
Transience score 
"""
import inscore

class ScoreElement(object):
    """
    Main container for a INSCore element.  This class (and its derived classes)
    is meant to provide the proper OSC messages to be used by INScore engine.
    """
    def __init__(self, URI, x=0.0, y=0.0):
        self.show = 1
        self.x = x
        self.y = y
        self.scale = 1.0
        self.URI = URI

    def del(self):
        """
        Delete an element
        """
        return [self.URI, "del"]

    def x(self, xpos):
        self.x = xpos
        return [self.URI, "x", xpos]

    def y(self, ypos):
        self.y = ypos
        return [self.URI, "y", ypos]

    def scale(self, factor):
        self.scale = factor
        return [self.URI, "scale", factor]

class ImageElement(ScoreElement):
    """
    Container for images in INSCore
    """
    def __init__(self, URI, x=0.0, y=0.0, imgPath):
        self.imgPath = imgPath
        

# TODO: write the score

class Transience(object):
    def __init__(self):
        parser = PrefParser()
        
