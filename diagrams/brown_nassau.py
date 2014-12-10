# Copyright 2014 Harri Ojanen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# brown_nassau.py
#
# Creates diagrams of the base and two rotors of a Brown-Nassau
# spherical computer.
#
# Required:
# python
# matplotlib
#
# Tested with python 2.7.6, matplotlib 1.3.1 on ubuntu 14.04.1
#
# The Brown-Nassau Spherical Computer is a device for graphically
# solving the astronomical triangle, i.e., for transforming from
# azimuthal coordinates to equatorial coordinates. It can be used for
# star identification or sight planning and reduction in celestial
# navigation, among others.
#
# Descriptions of it can be found in the following:
#
# O. E. Brown and J. J. Nassau, A Navigation Computer, The American
# Mathematical Monthly, Vol. 54, No. 8 (Oct., 1947), pp. 453-458.
#
# John Lyukx, The Brown-Nassau Spherical Computer, Navigator's
# Newsletter, issue 62, 1998-1999, pp. 12-15. (available online at
# http://www.starpath.com/foundation/newsletter.htm)
#
# The Smithsonian Institution has an example with a photograph at
# http://collections.si.edu/search/results.htm?q=record_ID%3Anasm_A19700379000&repo=DPLA


#############################################################################

from math import *
from pylab import *
import datetime
import os.path

font_size=5


#############################################################################
# Brown-Nassau grid formulae
#
# y = sin d, x = cos d cos t
#
# d = const: lines parallel to x-axis
# t = const: ellipses
#
# transformation r' = asin r

def brown_nassau(d, t, flipped):
    y = sin(d)*ones(shape(t))
    x = cos(d)*cos(t)
    r = sqrt(x**2 + y**2)
    rp = arcsin(r)
    s = (rp + 1e-20) / (r + 1e-20)
    xp = s*x
    yp = s*y
    if flipped:
        return (yp,xp)
    else:
        return (xp,yp)

def curve(d,t,k, styles, flipped):
    xp, yp = brown_nassau(d, t, flipped)
    if k % blk_step == 0:
        s = 0
    else:
        s = 1
    marker = styles[s]['marker']
    clr = styles[s]['color']
    w = styles[s]['width']
    sz = styles[s]['size']

    plot(degrees(xp),degrees(yp),marker,color=clr,linewidth=w,markersize=sz)



#############################################################################
# draw the brown nassau grid

def draw_grid(styles, step, blk_step, flipped):
    is_line_diagram = styles[0]['marker'] == '-'

    # -----------------------------------------------------------------------
    # equal azimuth ellipses
    T0 = range(0,90+step,step)
    d = radians(range(0,90+1))
    for t0 in T0:
        t = radians(t0)
        if t0 % 10 == 0:
            d = radians(range(0,90+1))
        elif t0 % 5 == 0:
            d = radians(range(0,85+1))
        elif t0 % 5 == 2:
            d = radians(range(0,80+1))
        else:
            d = radians(range(0,70+1))
        curve(d,t,t0, styles, flipped)

    # -----------------------------------------------------------------------
    # equal altitude "lines"
    D0 = range(0,90+step,step)
    t = radians(range(0,90+1))
    for d0 in D0:
        d = radians(d0)
        if not is_line_diagram and d0 >= 80:
            t = radians(range(0,90+1,5))
        curve(d,t,d0, styles, flipped)


#############################################################################
# tick marks, labels and verniers for arc

def tick(angle, r1, r2, clr, w=.1):
    x1 = r1*cos(angle)
    y1 = r1*sin(angle)
    x2 = r2*cos(angle)
    y2 = r2*sin(angle)
    plot([x1,x2],[y1,y2],color=clr,linewidth=w)

def verniers(clr,flipped):
    for offset in [0,90]:
        if offset == 0:
            sgn = 1
        else:
            sgn = -1

        for i in range(31):
            d0 = .5*i*29/30.
            d = sgn*d0+offset
            if i % 10 == 0:
                r = 0
                if flipped:
                    ii=i
                else:
                    ii=30-i
                if i > 0:
                    text(90.5*cos(radians(d)), 90.5*sin(radians(d)),
                         '%d'%ii,
                         rotation=d-90,
                         fontsize=font_size*2/3.,
                         horizontalalignment='center',
                         verticalalignment='center',
                         color=clr)
            elif i % 5 == 0:
                r = .5
            else:
                r = 1
            tick(radians(d),    91+r,93,clr)

        tick(radians(offset),90.5,91,clr,1)

        d = offset - sgn*.5
        if flipped and offset==0:
            vernier = 'A'
        elif flipped and offset==90:
            vernier = 'X'
        elif not flipped and offset==0:
            vernier = 'B'
        elif not flipped and offset==90:
            vernier = 'Y'

        text(90.5*cos(radians(d)), 90.5*sin(radians(d)),
             vernier,
             rotation=d-90,
             fontsize=font_size,
             horizontalalignment='center',
             verticalalignment='center',
             color=clr)


def outer_ticks(clr):
    D0 = range(0,91)
    for d0 in D0:
        d1 = radians(d0)
        tick(d1,93.,94.,clr)
        if d0 < 90:
            tick(radians(d0+.5),93.,93.5,clr)

def draw_ticks(outside_ticks, flipped, styles):
    is_line_diagram = styles[0]['marker'] == '-'

    color=styles[0]['color']
    if outside_ticks:
        verniers(color,flipped)
    else:
        outer_ticks(color)

    D0 = range(0,blk_step+90,blk_step)
    h = 1e-3
    for d0 in D0:
        d1 = radians(d0)
        dx = cos(d1)
        dy = sin(d1)
        xp = 90*dx
        yp = 90*dy

        if d0 % (1*blk_step) == 0:
            # position and angle for text label
            xtxt = xp + 6*dx
            ytxt = yp + 6*dy
            a = d0-90
            if flipped:
                d0 = 90-d0

            if is_line_diagram:
                txt = '%d'%d0
            else:
                txt = '%d\n%d'%(90-d0,d0)

            text(xtxt,ytxt,txt,
                 horizontalalignment='center',
                 verticalalignment='center',
                 fontsize=font_size,
                 color=color,
                 rotation=a)


#############################################################################
# horizontal axis
def hor_axis(flipped,styles):
    color=styles[0]['color']
    T = range(0,90+5,5)
    for t in T:
        if flipped:
            t1 = 90-t
        else:
            t1 = t
        if t==90:
            txt='%d'%t1
        else:
            txt='%d\n%d'%(t1,180-t1)
        text(90-t,-4,txt,
             horizontalalignment='center',
             verticalalignment='center',
             multialignment='center',
             fontsize=font_size,
             bbox=dict(facecolor=(1,1,1,.5),edgecolor=(1,1,1,.5),pad=0),
             color=color)
        if t % 10 == 0:
            y = -2
        else:
            y = -1
        plot([t,t],[0,y],color=color,linewidth=.1)


#############################################################################
# vertical axis
def ver_axis(flipped,styles):
    color=styles[0]['color']
    T = range(0,90+5,5)
    for t in T:
        if flipped:
            t1 = 90-t
        else:
            t1 = t
        txt='%d'%t1
        text(-4,t,txt,
             horizontalalignment='center',
             verticalalignment='center',
             multialignment='center',
             fontsize=font_size,
             bbox=dict(facecolor=(1,1,1,.5),edgecolor=(1,1,1,.5),pad=0),
             color=color)
        if t % 10 == 0:
            x = -2
        else:
            x = -1
        plot([x,0],[t,t],color=color,linewidth=.1)


#############################################################################
# Format axes
def format_axes(flipped):
    ax = gca()
    ax.set_aspect(1.)

    axis((-4,98,-4,98))

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)


#############################################################################
# title, date, comments
def comments(styles):
    txt = ('Brown-Nassau\nSpherical Computer\n' +
           datetime.date.today().isoformat() + ' HJO')
    text(80,80,txt,
         horizontalalignment='center',
         verticalalignment='center',
         multialignment='center',
         fontsize=font_size,
         color=styles[0]['color'])


#############################################################################
# save
def save_diagram(styles, flipped):
    if styles[0]['marker'] == '-':
        name = 'lines'
    else:
        name = 'dots'

    if flipped:
        name = name + '2'
    else:
        name = name + '1'

    file_name = '_brown_nassau_' + name
    print file_name

    dire = os.path.expanduser("~")
    savefig(os.path.join(dire, file_name + '.svg'),
            bbox_inches='tight', pad_inches=0.0)
    savefig(os.path.join(dire, file_name + '.pdf'),
            bbox_inches='tight', pad_inches=0.0)


#############################################################################
# create and save whole diagram
def create(styles, step, blk_step, flipped):
    clf()
    draw_grid(styles, step, blk_step, flipped)
    draw_ticks(styles[0]['marker'] == '-', flipped, styles)
    hor_axis(flipped, styles)
    ver_axis(flipped, styles)
    comments(styles)
    format_axes(flipped)
    save_diagram(styles, flipped)


#############################################################################
# Lines or dots on 'step' intervals, those on 'blk_step' intervals
# are made darker or thicker
step=1
blk_step=5

#############################################################################
# two line diagrams, original and flipped
styles = [
    {'marker':'-', 'color': (0,0,0), 'width':.5, 'size':2},
    {'marker':'-', 'color': (0,0,0), 'width':.2, 'size':.25}
]
create(styles, step, blk_step, False)
create(styles, step, blk_step, True)


#############################################################################
# dot diagram
styles = [
    {'marker':'.', 'color': (0,0,0), 'width':.5, 'size':2},
    {'marker':'.', 'color': (0,0,0), 'width':.2, 'size':.25}
]
create(styles, step, blk_step, False)
