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

# brown_nassau_semi.py
#
# Creates semi-circle variants of the diagrams for the base and a single 
# rotor of a Brown-Nassau spherical computer.
#
# The base and rotor are larger than in the original computer, but
# there are fewer cases to consider ("same name" or not ...)
#

from math import *
from pylab import *
import datetime

font_size=3

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

def curve(d,t,k, blk_step, styles, flipped):
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
    for t0 in T0:
        t = radians(t0)
        if t0 % 10 == 0:
            d = radians(range(-90,90+1))
        elif t0 % 5 == 0:
            d = radians(range(-85,85+1))
        elif t0 % 5 == 2:
            d = radians(range(-80+1,80+0*1))
        else:
            d = radians(range(-70,70+1))
        curve(d,t,t0, blk_step, styles, flipped)

    # -----------------------------------------------------------------------
    # equal altitude "lines"
    D0 = range(-90,90+step,step)
    t1 = radians(range(0,90+1))
    t5 = radians(range(0,90+1,5))
    for d0 in D0:
        d = radians(d0)
        if not is_line_diagram and abs(d0) >= 80:
            t = t5
        else:
            t = t1
        curve(d,t,d0, blk_step, styles, flipped)


#############################################################################
# tick marks, labels and verniers for arc
def tick(angle, r1, r2, clr, w=.1):
    x1 = r1*cos(angle)
    y1 = r1*sin(angle)
    x2 = r2*cos(angle)
    y2 = r2*sin(angle)
    plot([x1,x2],[y1,y2],clr,linewidth=w)

def verniers(clr):
    for offset in [0,90,-90]:
        for sgn in [-1,1]:
            for i in range(31):
                d0 = .5*i*29/30.
                d = sgn*d0+offset
                if i % 10 == 0:
                    r = 0
                    if i > 0:
                        text(90.5*cos(radians(d)), 90.5*sin(radians(d)), '%d'%i,
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

def outer_ticks(clr):
    D0 = range(-90,91)
    for d0 in D0:
        d1 = radians(d0)
        tick(d1,93.,94.,clr)
        if d0 < 90:
            tick(radians(d0+.5),93.,93.5,clr)

def draw_ticks(outside_ticks, flipped):
    if outside_ticks:
        outer_ticks('w')
        verniers('k')
    else:
        outer_ticks('k')
        verniers('w')

    D0 = range(-90,blk_step+90,blk_step)
    h = 1e-3
    for d0 in D0:
        d1 = radians(d0)
        dx = cos(d1)
        dy = sin(d1)
        xp = 90*dx
        yp = 90*dy

        if d0 % (1*blk_step) == 0:
            # position and angle for text label
            xtxt = xp + 5*dx
            ytxt = yp + 5*dy
            a = d0-90
            if flipped:
                a = 180+a

            text(xtxt,ytxt,'%d'%d0,
                 horizontalalignment='center',
                 verticalalignment='center',
                 fontsize=font_size,
                 color='k',
                 rotation=a)


#############################################################################
# horizontal axis
def hor_axis():
    T = range(0,90,10)
    for t in T:
        if t%90==0:
            txt='%d'%t
        else:
            txt='%d\n%d'%(t,180-t)
        text(90-t,0,txt,
             horizontalalignment='center',
             verticalalignment='center',
             multialignment='center',
             fontsize=font_size,
             bbox=dict(facecolor=(1,1,1,.5),edgecolor=(1,1,1,.5),pad=0),
             color='k')

#############################################################################
# vertical axis
def ver_axis():
    T = range(-90,90+5,5)
    for t in T:
        txt='%d'%t
        text(-4,t,txt,
             horizontalalignment='center',
             verticalalignment='center',
             multialignment='center',
             fontsize=font_size,
             bbox=dict(facecolor=(1,1,1,.5),edgecolor=(1,1,1,.5),pad=0),
             color='k')
        if t % 10 == 0:
            x = -2
        else:
            x = -1
        plot([x,0],[t,t],'k',linewidth=.1)


#############################################################################
# Format axes
def format_axes():
    ax = gca()
    ax.set_aspect(1.)

    axis((-25,94,-94,94))

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)


#############################################################################
# title, date, comments
def comments():
    txt = ('Brown-Nassau\nSpherical Computer\n' +
           datetime.date.today().isoformat() + ' HJO')
    text(80,80,txt,
         horizontalalignment='center',
         verticalalignment='center',
         multialignment='center',
         fontsize=font_size,
         color='k')



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

    file_name = '_brown_nassau_semi_' + name
    print file_name

    dire = '/home/harri/mac/'

    savefig(dire + file_name + '.svg', bbox_inches='tight', pad_inches=0.0)
    savefig(dire + file_name + '.pdf', bbox_inches='tight', pad_inches=0.0)


#############################################################################
# create and save whole diagram
def create(styles, step, blk_step, flipped):
    clf()
    draw_grid(styles, step, blk_step, flipped)
    draw_ticks(styles[0]['marker'] == '-', flipped)
    hor_axis()
    ver_axis()
    comments()
    format_axes()
    save_diagram(styles, flipped)


#############################################################################
# Lines or dots on 'step' intervals, those on 'blk_step' intervals
# are made darker or thicker or whatever depending on the above styles
step=1
blk_step=5


#############################################################################
# Alternative styles

# ------------------------------------------------------------------
# lines
if True:
    styles = [
        {'marker':'-', 'color': (0,0,1), 'width':.25, 'size':1},
        {'marker':'-', 'color': (0,0,1), 'width':.1, 'size':.125}
    ]
    create(styles, step, blk_step, False)

# ------------------------------------------------------------------
# dots
if True:
    styles = [
        {'marker':'.', 'color': (0,0,0), 'width':.25, 'size':1},
        {'marker':'.', 'color': (0,0,0), 'width':.1, 'size':.125}
    ]
    create(styles, step, blk_step, False)
