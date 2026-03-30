#!/usr/bin/python
import sys, os, time
import math
from solid import *
from solid.utils import *

import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

project = '000-005'

# Part Measurements
ri = 20.39/2 #min value
ro = 26.72/2 #max value
tshroud = 2.884 #average value
wshroud = 25.4 #nominal, not measured (not yet built)

wled = 13 #strip width - in sheath
hled = 2.5 #strip base to center of led - in sheath

tslot = 1.53-0.05 #thickness of straight edge

dpeg = 1.75-0.05 #diamter of filament peg hole

#strip length between caps = 970

# Defined dimensions

rc = 0.6 #corner rounding radius

#Part A
hinsert = 97.0 # length of pipe insert part (part A)
hpeg = 4.0 # depth of filament peg hole
dslot = 7.5 #depth of straight edge slot
pegyoff = 5.5 # offset of peg

#Part B
yoff = 24*25.4              # y offset of the light center from the ceiling
xoff = 30.0                 # x offset of the light center from the wall
spread = 6*12*25.4          # minimum light spreading distance on the ceiling

spread_max = 10*12*25.4     # maximum light spreading distance on the ceiling
yoff_min = 12*25.4          # adjustment range of light striking wall from ceiling

hbracket = 20.0


circum_margin = 0.4 # circumferential margin at pipe radius
da = circum_margin/ro #angular margin at pipe radius

#forward angles
af = math.atan2(yoff, spread)
afm = math.atan2(yoff, spread_max)
afm_ = afm - da

#upward angles
au = math.pi - math.atan2(yoff, xoff)
aum = math.pi - math.atan2(yoff_min, xoff)
aum_ = aum + da

#additonal angles
ast = math.pi/4 # top shroud angle
asf = math.pi/4 # front shroud angle

rst = ro + 5.0 #top shroud tangent radius
rsf = ro + 5.0 #front should tangent radius

class partA(Model):
    name = project + '-A'

    def render(self):

        r3_ = ri-0.1

        ar = math.pi*(0.55*2)


        o = Outline()

        o.add_verts([
            *arc(r3_, (0, 0), -ar/2, ar, N=100),
            [0.5, wled/2],
            [hled, wled/2],

#            [hled, tslot/2],
            *arc(rc, (hled+rc, tslot/2+rc), math.pi, math.pi/2),

#            [dslot, tslot/2],
            *arc(rc, (dslot-rc*3, tslot/2+rc), 3*math.pi/2, math.pi/2),
            *arc(rc, (dslot-rc, tslot/2+rc), 0, math.pi)[::-1],


            *arc(rc, (dslot-rc, -tslot/2-rc), math.pi, math.pi)[::-1],
            *arc(rc, (dslot-rc*3, -tslot/2-rc), 0, math.pi/2),
#            [dslot, -tslot/2],

#            [hled, -tslot/2],
            *arc(rc, (hled+rc, -tslot/2-rc), math.pi/2, math.pi/2),

            [hled, -wled/2],
            [0.5, -wled/2],

            ])

        base = Poly(o).render()
        base = linear_extrude(hinsert, convexity=10)(base)

        cut = cylinder(d=dpeg, h=10+hpeg)

        rpeg = r3_-dpeg
        apeg = math.pi/4
        for i in [-1,1]:
            yoff = rpeg*math.sin(apeg)
            xoff = i*rpeg*math.cos(apeg)
            yoff = pegyoff
            xoff = i*(wled/2-dpeg/2)
            _cut = translate([yoff,xoff,hinsert-hpeg])(cut)
            base -= _cut
            _cut = translate([yoff,xoff,-10])(cut)
            base -= _cut

        return base

class partB(Model):
    name = project + '-B'

    def render(self):

#        aum_ = 3*math.pi/4
#        afm_ = 0

        r = ro + 0.1

        #height of part from center
        ytop = (rst+tshroud)*math.sin(math.pi-aum_)/math.cos(math.pi/2-aum_+ast)
        #top right corner x offset
        xtc = ytop/math.tan(math.pi-aum_)

        #highest point that needs to be blocked
        yvis = (rst)*math.sin(math.pi-au)/math.cos(math.pi/2-au+ast)
        yvis_ = yvis + 0.5

        xend = yvis_/math.tan(afm_)
        print(f'Width = {xend+xoff}')

        o = Outline()

        o.add_verts([
            [-xoff, ytop],
            [-xtc, ytop],

            *arc(r, (0,0), aum_, 2*math.pi+afm_-aum_),

            [xend, yvis_],
            [xend+15, yvis_],

            [100, -100],
            [-xoff, -100]
            ])

        base = Poly(o).render()
        base = linear_extrude(hbracket, convexity=10)(base)

        return base



parts = filter(lambda x: Model in inspect.getmro(x[1]) and x[0] != 'Model', inspect.getmembers(sys.modules[__name__], inspect.isclass))

base = partB()

scad_render_to_file(base.render(), project+'.scad')

render = False
if len(sys.argv) > 1:
    if 'render' in sys.argv: render=True

if render:
    for p in parts:
        base = p[1]()
        base.write_stl(base.name+'.stl')


