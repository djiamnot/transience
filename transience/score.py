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
from txosc import osc

import os


ABS_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))
MEDIA_PATH = ABS_PATH[0]+"/media/"


# TODO: write the score

class Element(object):
    """
    This the instance of the Transience score element.  
    """

    def __init__(self, x=0.0, y=0.0, URI="", path = "", number=1, scale=1.):
        """
        Initialize.
        @param x, y: x, y position (between 0 and 1)
        @param URI: OSC address (without /ITL/scene part) of the element
        @param path: relative path to the folder containing element's images
        @param number: number (as part of the file name.  Files in form n.png)

        The x, y position will used to place the element on screen.  The URI
        will be used to identify the element within INScore scene.  This class
        will in fact prepend "/ITL/scene/" to the path variable and the resulting
        string will be the OSC address of the element.

        The path will be mangled as well to use absolute path relative to script's
        directory and let INSCore use the absolute path for loading images.
        Therefore the path provided here will be:
        /absolute/path/to/transience/media/<path>/<number>.png
        """

        self.x = x
        self.y = y
        self.URI = URI
        self.path = MEDIA_PATH+path
        self.number = number
        self.scale = scale

    def delete(self):
        """
        Delete the element from INScore scene
        """
        return osc.Message(URI, "del")

    def makeURI(self):
        """
        Cook the OSC address of the component relative to /ITL/scene
        """
        return "/ITL/scene/"+self.URI

    def makePath(self):
        """
        Cook the path to the image file
        """
        return self.path + "/" + str(self.number) + ".png"

    def image(self):
        """
        Cook the OSC message to create an image in INSCore
        """
        URI = self.makeURI()
        path = self.makePath()
        return osc.Message(URI, "set", "img", path)

    def scale_element(self):
        """
        Scale the element
        """
        return osc.Message(self.makeURI(), "scale", self.scale)

    def get_x(self):
        """
        cook position message
        """
        return osc.Message(self.makeURI(), "x", self.x)

    def get_y(self):
        """
        cook position message
        """
        return osc.Message(self.makeURI(), "y", self.y)

    def watch_mouse_enter(self):
        return osc.Message(self.makeURI(), "watch", "mouseEnter", "127.0.0.1:7001/mouse", "mouse entered!")

    def watch_mouse_down(self):
        return osc.Message(self.makeURI(),"watch","mouseDown","127.0.0.1:7001/mouse","clicked")
