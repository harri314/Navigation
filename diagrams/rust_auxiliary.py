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

# Rust auxiliary diagram

from math import *
from pylab import *

clf()

def transform_angle(angle):
    # from http://matplotlib.org/examples/pylab_examples/text_rotation_relative_to_line.html
    dummy = array((0,0))
    trans_angle = gca().transData.transform_angles(array((angle,)),
                                               dummy.reshape((1,2)))[0]
    return trans_angle


ax=gca()
ax.set_aspect(0.7)

lat_step = .01
lat = arange(0,90+lat_step,lat_step)
dec = arange(0,90+1)
lat = lat[1:-1]/180.*pi
dec = dec[:-1]

for d in dec:
    cos_lha = tan(d/180.*pi) / tan(lat)
    cos_lha[abs(cos_lha)>1] = nan
    lha = 180./pi*arccos(cos_lha)

    if mod(d,10)==0:
        clr = (1,0,0)
        w = 1.25

    elif mod(d,5)==0:
        clr = (0,0,0)
        w = 1.25

    elif mod(d,2) == 1:
        clr = (0,0,0)
        w = .5

    else:
        clr = (.5,.5,.5)
        w = .5

    if mod(d,5)!=0:
        R0 = 10

    elif mod(d,10)!=0:
        R0 = 3

    else:
        R0 = 0

    r = sqrt((lat/pi*180.-90.)**2 + (lha-90.)**2)
    lha[r<R0] = nan;

    plot(lat/pi*180.,lha,color=clr,linewidth=w)
    if d==1 or mod(d,5)==0:
        lat_txt = (d+10.)/1.111
        lha_txt = 180./pi*arccos(tan(d/180.*pi)/tan(lat_txt/180.*pi))
        lat_txt1 = lat_txt+.0001
        lha_txt1 = 180./pi*arccos(tan(d/180.*pi)/tan(lat_txt1/180.*pi))
        slope = (lha_txt1-lha_txt)/(lat_txt1-lat_txt)
        rot = 180./pi*arctan(slope);
        angle_screen = transform_angle(rot)
        text(lat_txt,lha_txt,'%d'%d,
                 horizontalalignment='center',
                 verticalalignment='center',
                 fontsize=7,
                 color='k',
                 rotation=angle_screen,
                 bbox=dict(facecolor='white',edgecolor='white',pad=0))
grid()

xlabel('latitude on x-axis, declination is curve parameter',fontsize=9)
ylabel('LHA on prime vertical',fontsize=9)

ax.xaxis.set_major_locator(MultipleLocator(5))
ax.xaxis.set_minor_locator(MultipleLocator(1))

ax.yaxis.set_major_locator(MultipleLocator(5))
ax.yaxis.set_minor_locator(MultipleLocator(1))

ax.xaxis.set_tick_params(which='both',direction='outward',labelsize=7,labeltop='on')
ax.yaxis.set_tick_params(which='both',direction='outward',labelsize=7,labelright='on')


savefig('/home/harri/mac/_rust_auxiliary.svg', bbox_inches='tight', pad_inches=0.0)
savefig('/home/harri/mac/_rust_auxiliary.pdf', bbox_inches='tight', pad_inches=0.0)
