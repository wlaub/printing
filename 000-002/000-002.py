#!/usr/bin/python
import sys, os, time
from solid import *
from solid.utils import *

import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

project = '000-002'

wbase = 16.0
dbase = 16.0

wcap = 12.0
dcap = 12.0

hcap = 1.5
hmax = 12.25

hbody = 3.3
hplunge = 3.5
#hleg = 3.8
hleg = 2.0
wbody = 6.2

htravel = hplunge-2.9-.2

hbase = hmax-hcap-htravel

hfloor = hmax-hcap-hplunge-hbody-hleg

hseat = hfloor+hleg
print(htravel)
hseat = hmax-hcap-hplunge-hbody
print(hseat)

wrest = 3.5

class partA(Model):
    name = project + '-A'

    def render(self):

        o = Outline()

        verts = [
        [wbase/2,0],
        [wbase/2,hfloor],
        [wrest/2,hfloor],
        [wrest/2,hbase],
        ]

        o.add_verts(verts)
        o.add_verts([ [-x, y] for x,y in verts[::-1]])

        base = Poly(o).render()
        base = linear_extrude(dbase)(base)
        base = rotate([90,0,0])(base)

        cut = box([100, wbody, 100])
        cut = translate([0,-wbase/2,hfloor+hleg])(cut)

        base -= cut

        pillar = box([wrest, wrest, hbase-hfloor/2])
        pillar = translate([0,-wbase/2,hfloor/2])(pillar)

        base += translate([-wbase/2+wrest/2,0,0])(pillar)
        base += translate([wbase/2-wrest/2,0,0])(pillar)


        return base

class partB(Model):
    name = project + '-B'

    def render(self):

        base = box([wcap, dcap, hcap])

        return base




parts = filter(lambda x: Model in inspect.getmro(x[1]) and x[0] != 'Model', inspect.getmembers(sys.modules[__name__], inspect.isclass))

base = partA()

scad_render_to_file(base.render(), project+'.scad')

render = False
if len(sys.argv) > 1:
    if 'render' in sys.argv: render=True

if render:
    for p in parts:
        base = p[1]()
        base.write_stl(base.name+'.stl')


