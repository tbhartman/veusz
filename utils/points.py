# points.py - functions to plot points

#    Copyright (C) 2003 Jeremy S. Sanders
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
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
###############################################################################

# $Id$

from itertools import izip

import veusz.qtall as qt4
import numpy as N

"""This is the symbol plotting part of Veusz

There are actually several different ways symbols are plotted.
We choose the most appropriate one for the shape:

QPainterPath symbols plotted with _plotPathSymbols
line symbols are plotted with _plotLineSymbols
ploygon symbols are plotted wiht _plotPolygonSymbols

Many of these are implemented as paths internally, and drawn using
QPainterPaths
"""

#######################################################################
## draw symbols which are sets of line segments

linesymbols = {
    'asterisk': ( ((-0.707, -0.707), (0.707,  0.707)),
                  ((-0.707,  0.707), (0.707, -0.707)),
                  ((-1, 0), (1, 0)), ((0, -1), (0, 1)) ),
    'lineplus': ( ((-1, 0), (1, 0)), ((0, -1), (0, 1)) ),
    'linecross': ( ((-0.707, -0.707), (0.707,  0.707)),
                   ((-0.707,  0.707), (0.707, -0.707)) ),
    'linehorz': ( ((-1, 0), (1, 0)), ),
    'linevert': ( ((0, -1), (0, 1)), ),
    'arrowleft': ( ((1, -1), (0, 0), (1, 1)), ((2, 0), (0, 0)) ),
    'arrowleftaway': ( ((-1, -1), (-2, 0), (-1, 1)), ((-2, 0), (0, 0)) ),
    'arrowright': ( ((-1, -1), (0, 0), (-1, 1)), ((-2, 0), (0, 0)) ),
    'arrowrightaway': ( ((1, -1), (2, 0), (1, 1)), ((2, 0), (0, 0)) ),
    'arrowup': ( ((-1, 1), (0, 0), (1, 1)), ((0, 2), (0, 0)) ),
    'arrowupaway': ( ((-1, -1), (0, -2), (1, -1)), ((0, 0), (0, -2)) ),
    'arrowdown': ( ((-1, -1), (0, 0), (1, -1)), ((0, -2), (0, 0)) ),
    'arrowdownaway': ( ((-1, 1), (0, 2), (1, 1)), ((0, 0), (0, 2)) ),
    'limitlower': ( ((-1, -1), (0, 0), (1, -1)), ((0, -2), (0, 0)),
                    ((-1, 0), (1, 0)) ),
    'limitupper': ( ((-1, 1), (0, 0), (1, 1)), ((0, 2), (0, 0)),
                    ((-1, 0), (1, 0)) ),
    'limitleft': ( ((1, -1), (0, 0), (1, 1)), ((2, 0), (0, 0)),
                   ((0, -1), (0, 1)) ),
    'limitright': ( ((-1, -1), (0, 0), (-1, 1)), ((-2, 0), (0, 0)),
                    ((0, -1), (0, 1)) ),
    'limitupperaway': ( ((-1, -1), (0, -2), (1, -1)), ((0, 0), (0, -2)),
                        ((-1, 0), (1, 0)) ),
    'limitloweraway': ( ((-1, 1), (0, 2), (1, 1)), ((0, 0), (0, 2)),
                        ((-1, 0), (1, 0)) ),
    'limitleftaway': ( ((-1, -1), (-2, 0), (-1, 1)), ((-2, 0), (0, 0)),
                       ((0, -1), (0, 1)) ),
    'limitrightaway': ( ((1, -1), (2, 0), (1, 1)), ((2, 0), (0, 0)),
                        ((0, -1), (0, 1)) ),

    # for arrows
    '_linearrow': ( ((-1.8, -1), (0, 0), (-1.8, 1)), ),
    '_linearrowreverse': ( ((1.8, -1), (0, 0), (1.8, 1)), ),
    }

def getLinePainterPath(name, size):
    """Get a painter path for line like objects."""
    path = qt4.QPainterPath()
    for lines in linesymbols[name]:
        path.moveTo(lines[0][0]*size, lines[0][1]*size)
        for x, y in lines[1:]:
            path.lineTo(x*size, y*size)
    return path

#######################################################################
## draw symbols which are polygons

# X and Y pts for corners of polygons
polygons = {
    # make the diamond the same area as the square
    'diamond': ( (0., 1.414), (1.414, 0.), (0., -1.414), (-1.414, 0.) ),
    'barhorz': ( (-1, -0.5), (1, -0.5), (1, 0.5), (-1, 0.5) ),
    'barvert': ( (-0.5, -1), (0.5, -1), (0.5, 1), (-0.5, 1) ),
    'plus': ( (0.4, 1), (0.4, 0.4), (1, 0.4), (1, -0.4),
              (0.4, -0.4), (0.4, -1), (-0.4, -1), (-0.4, -0.4),
              (-1, -0.4), (-1, 0.4), (-0.4, 0.4), (-0.4, 1) ),
    'octogon': ( (0.414, 1), (1, 0.414), (1, -0.414), (0.414, -1),
                 (-0.414, -1), (-1, -0.414), (-1, 0.414), (-0.414, 1) ),
    'triangle': ( (0, -1.2), (1.0392, 0.6), (-1.0392, 0.6) ),
    'triangledown': ( (0, 1.2), (1.0392, -0.6), (-1.0392, -0.6) ),
    'triangleleft': ( (-1.2, 0), (0.6, 1.0392), (0.6, -1.0392) ),
    'triangleright': ( (1.2, 0), (-0.6, 1.0392), (-0.6, -1.0392) ),
    'cross': ( (-0.594, 1.1028), (0, 0.5088), (0.594, 1.1028),
               (1.1028, 0.594), (0.5088, -0), (1.1028, -0.594),
               (0.594, -1.1028), (-0, -0.5088), (-0.594, -1.1028),
               (-1.1028, -0.594), (-0.5088, 0), (-1.1028, 0.594) ),
    'star': ( (0, -1.2), (-0.27, -0.3708), (-1.1412, -0.3708),
              (-0.4356, 0.1416), (-0.7056, 0.9708), (-0, 0.4584),
              (0.7056, 0.9708), (0.4356, 0.1416), (1.1412, -0.3708),
              (0.27, -0.3708) ),
    'pentagon': ((0, -1.2), (1.1412, -0.3708), (0.6936, 0.9708),
                 (-0.6936, 0.9708), (-1.1412, -0.3708)),
    'tievert': ( (-1, -1), (1, -1), (-1, 1), (1, 1) ),
    'tiehorz': ( (-1, -1), (-1, 1), (1, -1), (1, 1) ),
    'lozengehorz': ( (0, 0.707), (1.414, 0), (0, -0.707), (-1.414, 0) ),
    'lozengevert': ( (0, 1.414), (0.707, 0), (0, -1.414), (-0.707, 0) ),

    # special arrow symbols
    '_arrow': ( (0, 0), (-1.8, 1), (-1.4, 0), (-1.8, -1) ),
    '_arrowtriangle': ( (0, 0), (-1.8, 1), (-1.8, -1) ),
    '_arrownarrow': ( (0, 0), (-1.8, 0.5), (-1.8, -0.5) ),
    '_arrowreverse': ( (0, 0), (1.8, 1), (1.4, 0), (1.8, -1) ),
    }

def addPolyPath(path, vals):
    """Add a polygon with the list of x,y pts as tuples in vals."""
    poly = qt4.QPolygonF()
    for x, y in vals:
        poly.append( qt4.QPointF(x, y) )
    path.addPolygon(poly)
    path.closeSubpath()

def getPolygonPainterPath(name, size):
    """Create a poly path for a polygon."""
    path = qt4.QPainterPath()
    addPolyPath(path, N.array(polygons[name])*size)
    return path

#######################################################################
## draw symbols using a QPainterPath

def squarePath(painter, path, size):
    """Square path of size given."""
    path.addRect( qt4.QRectF(-size, -size, size*2, size*2) )

def circlePath(painter, path, size):
    """Circle path of size given."""
    path.addEllipse( qt4.QRectF(-size, -size, size*2, size*2) )

def ellipseHorzPath(painter, path, size):
    """Horizontal ellipse path."""
    path.addEllipse( qt4.QRectF(-size, -size*0.5, size*2, size) )

def ellipseVertPath(painter, path, size):
    """Vertical ellipse path."""
    path.addEllipse( qt4.QRectF(-size*0.5, -size, size, size*2) )

def circleHolePath(painter, path, size):
    """Circle with centre missing."""
    circlePath(painter, path, size)
    circlePath(painter, path, size*0.5)

def squareHolePath(painter, path, size):
    """Square with centre missing."""
    path.addRect( qt4.QRectF(-size, -size, size*2, size*2) )
    path.addRect( qt4.QRectF(-size*0.5, -size*0.5, size, size) )

def diamondHolePath(painter, path, size):
    """Diamond with centre missing."""
    pts = N.array(polygons['diamond'])*size
    addPolyPath(path, pts)
    addPolyPath(path, pts*0.5)

def pentagonHolePath(painter, path, size):
    """Pentagon with centre missing."""
    pts = N.array(polygons['pentagon'])*size
    addPolyPath(path, pts)
    addPolyPath(path, pts*0.5)

def squareRoundedPath(painter, path, size):
    """A square with rounded corners."""
    path.addRoundRect( qt4.QRectF(-size, -size, size*2, size*2), 50, 50 )

def dotPath(painter, path, size):
    """Draw a dot."""
    w = painter.pen().widthF()
    path.addEllipse( qt4.QRectF(-w*0.5, -w*0.5, w, w) )

def bullseyePath(painter, path, size):
    """A filled circle inside a filled circle."""
    path.setFillRule(qt4.Qt.WindingFill)
    circlePath(painter, path, size)
    circlePath(painter, path, size*0.5)

def circleDotPath(painter, path, size):
    """A dot inside a circle."""
    path.setFillRule(qt4.Qt.WindingFill)
    circlePath(painter, path, size)
    dotPath(painter, path, size)

pathsymbols = {
    'square': squarePath,
    'circle': circlePath,
    'ellipsehorz': ellipseHorzPath,
    'ellipsevert': ellipseVertPath,
    'circlehole': circleHolePath,
    'squarehole': squareHolePath,
    'diamondhole': diamondHolePath,
    'pentagonhole': pentagonHolePath,
    'squarerounded': squareRoundedPath,
    'dot': dotPath,
    'bullseye': bullseyePath,
    'circledot': circleDotPath,
    }

def getSymbolPainterPath(painter, name, size):
    """Get a painter path for a symbol shape."""
    path = qt4.QPainterPath()
    pathsymbols[name](painter, path, size)
    return path

def getPainterPath(painter, name, size):
    """Return a painter path for the name and size.

    Returns (painterpath, enablefill)."""
    if name in linesymbols:
        return getLinePainterPath(name, size), False
    elif name in polygons:
        return getPolygonPainterPath(name, size), True
    elif name in pathsymbols:
        return getSymbolPainterPath(painter, name, size), True
    elif name == 'none':
        return qt4.QPainterPath(), True
    else:
        raise ValueError, "Invalid marker name %s" % name

#######################################################################
## external interfaces

# list of codes supported
MarkerCodes = (
    'none',
    'circle', 'diamond', 'square',
    'cross', 'plus', 'star',
    'barhorz', 'barvert',
    'octogon', 'pentagon', 'tievert', 'tiehorz',
    'triangle', 'triangledown', 'triangleleft', 'triangleright',
    'dot', 'circledot', 'bullseye',
    'circlehole', 'squarehole', 'diamondhole', 'pentagonhole',
    'squarerounded',
    'ellipsehorz', 'ellipsevert',
    'lozengehorz', 'lozengevert',
    'asterisk',
    'lineplus', 'linecross',
    'linevert', 'linehorz',
    'arrowleft', 'arrowright', 'arrowup', 'arrowdown',
    'arrowleftaway', 'arrowrightaway',
    'arrowupaway', 'arrowdownaway',
    'limitupper', 'limitlower', 'limitleft', 'limitright',
    'limitupperaway', 'limitloweraway',
    'limitleftaway', 'limitrightaway',
    )

def plotMarkers(painter, xpos, ypos, markername, markersize, scaling=None):
    """Funtion to plot an array of markers on a painter.

    painter: QPainter
    xpos, ypos: iterable item of positions
    markername: name of marker from MarkerCodes
    markersize: size of marker to plot
    scaling: scale size of markers by array, or don't in None
    """

    # minor optimization
    if markername == 'none':
        return
    
    painter.save()

    # get path to draw and whether to fill
    path, fill = getPainterPath(painter, markername, markersize)
    if not fill:
        # turn off brush
        painter.setBrush( qt4.QBrush() )

    # optimize loop
    t = painter.translate
    d = painter.drawPath
    r = painter.resetTransform

    # split up into two loops as this is a critical path
    if scaling is None:
        # actually plot the markers (with no scaling)
        for x, y in izip(xpos, ypos):
            t(x, y)
            d(path)
            r()
    else:
        # plot markers, scaling each one
        s = painter.scale
        for x, y, sc in izip(xpos, ypos, scaling):
            t(x, y)
            s(sc, sc)
            d(path)
            r()
    
    painter.restore()

def plotMarker(painter, xpos, ypos, markername, markersize):
    """Function to plot a marker on a painter, posn xpos, ypos, type and size
    """
    plotMarkers(painter, (xpos,), (ypos,), markername, markersize)

# translate arrow shapes to point types (we reuse them)
arrow_translate = {
    'none': 'none',
    'arrow': '_arrow',
    'arrownarrow': '_arrownarrow',
    'arrowtriangle': '_arrowtriangle',
    'arrowreverse': '_arrowreverse',
    'linearrow': '_linearrow',
    'linearrowreverse': '_linearrowreverse',
    'bar': 'linevert',
    'linecross': 'linecross',
    'asterisk': 'asterisk',
    'circle': 'circle',
    'square': 'square',
    'diamond': 'diamond',
}

# codes of allowable arrows
ArrowCodes = ( 'none', 'arrow', 'arrownarrow',
               'arrowtriangle',
               'arrowreverse',
               'linearrow', 'linearrowreverse',
               'bar', 'linecross',
               'asterisk',
               'circle', 'square', 'diamond',
               )

def plotLineArrow(painter, xpos, ypos, length, angle,
                  arrowsize=0,
                  arrowleft='none', arrowright='none'):
    """Plot a line or arrow.
    
    xpos, ypos is the starting point of the line
    angle is the angle to the horizontal (degrees)
    arrowleft and arrowright are arrow codes."""

    painter.save()
    painter.translate(xpos, ypos)
    painter.rotate(angle)

    # draw line between points
    painter.drawLine( qt4.QPointF(0., 0.),
                      qt4.QPointF(length, 0.) )

    # plot marker at one end of line
    plotMarker(painter, length, 0., 
               arrow_translate[arrowright], arrowsize)

    # plot reversed marker at other end
    painter.scale(-1, 1)
    plotMarker(painter, 0., 0., 
               arrow_translate[arrowleft], arrowsize)

    painter.restore()
