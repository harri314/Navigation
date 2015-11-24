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

# Rust diagram

from math import *
from pylab import *

font_size = 5

clf()

class FormatRev(Formatter):
    def __init__(self,):
        pass

    def __call__(self, x, pos=None):
        if x % 10 == 0:
            return '%d' % (90-x)
        else:
            return ''

class FormatNone(Formatter):
    def __init__(self,):
        pass

    def __call__(self, x, pos=None):
        return ''

class FormatTens(Formatter):
    def __init__(self,):
        pass

    def __call__(self, x, pos=None):
        if x % 10 == 0:
            return '%d' % x
        else:
            return ''


def transform_angle(angle):
    # from http://matplotlib.org/examples/pylab_examples/text_rotation_relative_to_line.html
    dummy = array((0,0))
    trans_angle = gca().transData.transform_angles(array((angle,)),
                                               dummy.reshape((1,2)))[0]
    return trans_angle


def curve(d,style):
    r1 = 10
    r2 = 20
    if d%10==0:
        t0 = 0
    elif d%5==0:
        t0 = r1/sqrt(1+cos(radians(d))**2)
    else:
        t0 = r2/sqrt(1+cos(radians(d))**2)
    t=linspace(t0,90,120)
    y=90*cos(radians(d))*sin(radians(t))
    plot(t,y,style)

    if d%5==0:
        i=73-int(round(d/1.75))
        t1=i
        y1=90*cos(radians(d))*sin(radians(t1))
        t2=i+1
        y2=90*cos(radians(d))*sin(radians(t2))
        slope=(y2-y1)/(t2-t1)
        angle=degrees(atan(slope))*.9
        angle_screen = transform_angle(angle)
        text(.5*(t1+t2),.5*(y1+y2), '%d'%d, 
             horizontalalignment='center',
             verticalalignment='center',
             fontsize=font_size,
             color=style,
#             bbox=dict(facecolor='white',edgecolor='white',pad=0),
             rotation=angle_screen)
        plot([t1,t2],[y1,y2],'w-',linewidth=5)
        plot([t1,t2],[y1-.5,y2-.5],'w-',linewidth=5)


curve(0,'r')
curve(5,'0.3')
curve(10,'r')
curve(12.5,'0.7')
curve(15,'0.3')
curve(17.5,'0.7')
D=range(20,90,1)
for d in D:
    if d % 5 == 0:
        style = '0.3'
    else:
        style = '0.7'
    if d % 10 == 0:
        style = 'r'
    curve(d,style)

#curve(.995,'0.7')
#curve(.001,'0.7')
#curve(.999,'0.7')


ax=gca()
ax.set_aspect(0.7)

ax.xaxis.set_major_locator(MultipleLocator(5))
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.xaxis.set_major_formatter(FormatTens())

ax.yaxis.set_major_locator(MultipleLocator(10))
ax.yaxis.set_minor_locator(MultipleLocator(1))
ax.yaxis.set_major_formatter(FormatNone())

ax.xaxis.set_tick_params(which='both',direction='outward',labelsize=7)
ax.yaxis.set_tick_params(which='both',direction='outward',labelsize=7)

for x in range(0,95,5):
    if x % 10 == 0:
        y = 1
    else:
        y = .5
    plot([x, x],[0, y],'k')
    plot([x, x],[90, 90-y],'k')
    plot([0, y],[x, x],'k')
    plot([90, 90-y],[x, x],'k')
    if x > 0:
        text(x, 3+90*sin(radians(x)), '%d'%x,
             horizontalalignment='center',
             verticalalignment='center',
             fontsize=font_size,
             color='0.0',
             bbox=dict(facecolor='white',edgecolor='white'))

#plot(range(0,95,5),0*array(range(0,95,5)),'r.')
#plot(range(0,95,5),90+0*array(range(0,95,5)),'r.')
#plot(0*array(range(0,95,5)),range(0,95,5),'r.')
#plot(90+0*array(range(0,95,5)),range(0,95,5),'r.')
grid()
#tick_params(labeltop=True)


# simplified diagram for an insert:
if False:
    figure()

    D=range(0,90,10)
    for d in D:
        curve(d,'k')


savefig('/home/harri/mac/_rust_diagram.svg', bbox_inches='tight', pad_inches=0.0)
savefig('/home/harri/mac/_rust_diagram.pdf', bbox_inches='tight', pad_inches=0.0)
