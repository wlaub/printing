#!/usr/bin/python
import sys, os, time
import math
from solid import *
from solid.utils import *

import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

project = '000-013'

height = 49
dy = 3


back = 3
back_width = 7
front = 10.75
front_top = front+1.5

hback  = 21.5

cham = 5/2

gap = 22.06

width = 21.5

d = 10

bot = 5

depth = 21
dbase = 5

#hinge center
cy = 8.42/2+22.06#26.49
cx = 4.41

tscreen = 8.52
tb = .72+cx
tf = tscreen-tb

#af =
ab = math.pi/2-math.atan2(height-hback, back)
#af =

"""
should be like x = atan2(
y = height-cy+tf*sin(x),
x = front-cx-tf*cos(x)
)
but let's just do like
height-ct+0
front-cx-tf
"""
af = math.pi/2-atan2(height-cy, front-cx-tf)


class partA(Model):
    name = project + '-A'

    def render(self):
        o = Outline()

        """
        o.add_verts([
            [,],
            [,],
            [,],
            [,],
            [,],
            [,],
            [,],
            [,],
            ])
        """

        dxf = dy*math.tan(af)
        dxb = dy*math.tan(ab)

        print(ab*180/math.pi, dxb)
        print(af*180/math.pi, dxf)


        o.add_verts([
            [0,-bot],
#            [back-cham,cham],
            ])
        o.add_verts(arc(cham, (back_width-cham, cham-bot), 1.5*math.pi, math.pi/2))

        o.add_verts([
            [back,height],
            [back-dxb,height-dy],
            [-front_top+dxf,height-dy],
            [-front_top,height],
            [-width,gap],
#            [-width+cham,cham],
            ])

        o.add_verts(arc(cham, (-width+cham, cham-bot), math.pi, math.pi/2))

        base = Poly(o).render()

        result = linear_extrude(depth+dbase)(base)

        o = Outline()

        o.add_verts([
            [0,hback],
            [back-dxb,height-dy],
            [back-dxb,height+d],
            [-front_top+dxf,height+d],
            [-front_top+dxf,height-dy],
            [-front,gap],
            [-width-d,gap],
            [-width-d,0],
            [0,0],
            ])
        base = Poly(o).render()

        cut = linear_extrude(depth+dbase, convexity =10)(base)
        cut = translate([0,0,-dbase])(cut)

        result -= cut


        result = rotate([180,0,0])(result)
        return result


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


