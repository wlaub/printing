#!/usr/bin/python
import sys, os, time
from solid import *
from solid.utils import *

import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

project = '000-003'

h = 70.0
d = 50.0

t = 4.0
w = d

class partA(Model):
    name = project + '-A'

    def render(self):
        result = box([w+t*2,h+t*2,t+d/2])

        cut = box([w*2, h, d])

        cut = translate([0,0,t])(cut)
        result -= cut

        cut = box([w, h*2, d])
        result -= translate([w/2+t*2,0,t])(cut)
        result -= translate([-w/2-t*2,0,t])(cut)


        notch = cylinder(h=h*2, d=0.6)
        notch = rotate([90,0,0])(notch)
        notch = translate([0,h,t+d/2])(notch)

        result -= notch

        result -= translate([0,0,-t])(notch)



        return result

class partB(Model):
    name = project + '-B'

    def render(self):
        bt = 2.2
        gap = 0.8
        tt = bt

        depth = 5.0
        length = 30.
        offset = length/2-4.0

        verts = [
            [0,0],
            [length, 0],
            [length, bt],
            [offset, bt],
            [offset, bt+gap],
            [length, bt+gap],
            [length, bt+gap+tt],
            [0,bt+gap+tt]
        ]

        o = Outline()
        o.add_verts(verts)

        result = Poly(o).render()
        result = linear_extrude(depth)(result)

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


