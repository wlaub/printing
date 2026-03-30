

import sys, os, time
from solid import *
from solid.utils import *

import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

project = '000-012'

w = 1*25.4
h = 2*25.4

thickness = 0.25*25.4

center_depth  = 0.125*25.4

slot_depth = 0.2*25.4
slot_depth = 6

d_out = 4*25.4


class partA(Model):
    name = project + '-A'

    def render(self):
        o = Outline()

        N = 8

        r_out = 0.5*d_out/cos(pi/N)

        verts = []
        for i in range(N):
            a = 2*pi*(i+0.5)/N
            verts.append((r_out*sin(a), r_out*cos(a)))

        o.add_verts(verts)

        result = Poly(o).render()
        result = linear_extrude(thickness)(result)

        cut = box([w,h,100])
        result -= translate([0,0,thickness-center_depth])(cut)

        cut = translate([0,0,-1])(cut)

        cut = translate([0,h/2+d_out/2-slot_depth,0])(cut)
        for i in range(N):
            a = 2*pi*(i)/N
            result -= rotate([0,0,a*180/pi])(cut)

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


