# vzexcept.py
# veusz exceptions

#    Copyright (C) 2004 Jeremy S. Sanders
#    Email: Jeremy Sanders <jeremy@jeremysanders.net>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##############################################################################

# $Id$

"""Veusz-specific exceptions."""

class VeuszException(Exception):
    """Veusz-specific exception."""
    
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class DistanceError(VeuszException):
    """Exception thrown if can't convert distance."""
    pass

class PreferenceError(VeuszException):
    """Exception thrown due to preferences."""
    pass

class GraphError(VeuszException):
    """Exception thrown to a graph-related error."""
    pass
