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
The matrix configuration class.
This class represents the matrix configuration possibilities.
This really is just a collection of possible 'paths' through the matrix.
There are finite possiblities for each of the elements, we need to lay them
down only once.

The images are arranged in the order as per matrices in the instructions:

    4
  2   7
1   5   9
  3   8
    6

Therefore there are only 12 possible paths (*2, their reversed versions)
"""

paths = [
    [1, 2, 4, 7, 9],
    [1, 2, 5, 7, 9],
    [1, 2, 5, 8, 9],
    [1, 3, 5, 7, 9],
    [1, 3, 5, 8, 9],
    [1, 3, 6, 8, 9],
    [4, 7, 9, 8, 6],
    [4, 7, 5, 8, 6],
    [4, 7, 5, 3, 6],
    [4, 2, 5, 8, 6],
    [4, 2, 5, 3, 6],
    [4, 2, 1, 3, 6],
    ]

class ConfMatrix(object):
    """
    Does some basic operations on the 'matrix'.
    """
    def __init__(self):
        """
        TODO: do we need to init anything?
        """
        pass

    def reversePath(self, path):
        """
        Reverses the path
        @param path: a list
        @rtype: list
        """
        return list(reversed(path))
        

    def isValidPath(self, path):
        """
        Compare path to 
        """

        valid = False
        for i in paths:
            if i == path:
                valid = True
                break
            else:
                valid = False
        return valid

    
