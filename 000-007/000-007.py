#!/usr/bin/python
import sys, os, time
import math
from solid import *
from solid.utils import *

import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

project = '000-007'

leg = 18.9
leg_max = 19.0
leg_min = 18.4
angle = math.atan2(12.5, 15.25)

wbar = 19.1+.1
tbar = 2.85+.1

tclamp = 25.
tbase = 4
dbase = tbar + 2*tbase
tleg = 8
tside = wbar + 2*tleg
hpart = 75

class partA(Model):
    name = project + '-A'

    def render(self):
        result = box([tside,hpart,tclamp+dbase])

        #leg slot

        o = Outline()
        o.add_verts([
            [-leg_max/2, 0],
            [leg_max/2, 0],
            [leg_min/2, tclamp+2],
            [-leg_min/2, tclamp+2],
            ])

        cut = Poly(o).render()
        cut = linear_extrude(1000)(cut)
        cut = rotate([90,0,0])(cut)
        cut = translate([0,500,dbase])(cut)

        result -= cut

#        cut = box([leg, 1000, 1000])
#        cut = translate([0,0,dbase])(cut)
#        result -= cut

        #bar slot
        print(angle*180/math.pi)
        cut = box([1000, wbar, tbar])
        cut = rotate([0,0,angle*180/math.pi])(cut)
#        cut = rotate([0,0,10])(cut)
        cut = translate([0,0,tbase])(cut)

        result -= cut

        return result

class partB(Model):
    name = project + '-B'

    def render(self):

        drim = 101.65
        hpot = 100

        tsize = tbar+8
        tsupp = 8
        tlight = 13
        tspoke = tlight
        tcut = 4.
        tdepth = 10.0

        wbase = drim + 4.

        rlight = drim
        hbase = hpot

        o = Outline()
        o.add_verts([
            [-wbase/2-wbar-4,0],
            [-wbase/2-wbar-4, tsize],
            [-rlight/2-tsupp, tsize],
            [-rlight/2-tsupp, hbase],

            ])

        o.add_verts(arc(rlight/2+tspoke, (0, hbase), 0, math.pi)[::-1])

        o.add_verts([
            [rlight/2+tsupp, hbase],
            [rlight/2+tsupp, tsize],
            [wbase/2+wbar+4,tsize],
            [wbase/2+wbar+4, 0],
            ])

        result = Poly(o).render()
        result = linear_extrude(tdepth)(result)

        o = Outline()
        o.add_verts([
            [-rlight/2, tsize],

            ])

        o.add_verts(arc(rlight/2, (0, hbase), 0, math.pi)[::-1])

        o.add_verts([
            [rlight/2, tsize],

            ])

        cut = Poly(o).render()
        cut = linear_extrude(1000)(cut)
        cut = translate([0,0,-10])(cut)

        result -= cut


        cut = box([tlight, 100, 100])
        cut = translate([0,50+rlight/2+tcut,-10])(cut)

        for a in (-30, -60, 30, 60):
            _cut = rotate([0,0,a])(cut)
            _cut = translate([0,hbase,0])(_cut)
            result -= _cut

        #bars
        cut = box([wbar, tbar, 1000])
        cut = translate([0,tsize/2,-10])(cut)
        for i in (-1,1):
            result -= translate([i*(wbase/2+wbar/2),0,0])(cut)

        return result



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


