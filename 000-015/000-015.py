#!/usr/bin/python
import sys, os, time
from solid import *
from solid.utils import *

import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

project = '000-015'

w_rail = 19.2
h_rail = 2.81

th_holder = 2 #below rail
th_holder_side = 4 #on sides
th_holder_top = 2 #between rail and straightener


_h_wire_out = 16.5/2 #from straightener base

h_wire = _h_wire_out + th_holder_top #from top of tail

d_wire = 2 #wire diameter
d_hole = d_wire + 1

w_peg = (25.7+34.02)/2 #space between straightener peg holes
r_peg = 4.2/2

h_straightener = 16.64 #from bottom of straightener

l_holder = 7

l_eye = 10
l_eye_top = 5
l_eye_mid = 1
th_hole = 2

class partA(Model):
    #straightener holder
    name = project + '-A'

    def render(self):

        dw = (w_peg+2*r_peg)/2
        dh = th_holder + th_holder_top + h_rail
        h = dh + h_straightener

        w_p = r_peg*2

        o = Outline()

        verts = [
            [dw,0],
            [dw,h],
            [dw-w_p,h],
            [dw-w_p,dh],
            ]

        o.add_verts(verts)
        o.add_verts([(-x[0], x[1]) for x in verts[::-1]])

        result = Poly(o).render()
        result = linear_extrude(l_holder)(result)

        cut = box([w_p+2, h_straightener+2, l_holder+1])

        hole = cylinder(r=r_peg, h = h_straightener+4)
        hole = rotate([90,0,0])(hole)
        hole = translate([0,h_straightener/2+2,1/2+r_peg/2])(hole)
        cut -= hole

        for i in [-1,1]:
            result -= translate([i*w_peg/2, (h_straightener+2)/2+dh,-1/2])(cut)

        cut = box([w_rail, h_rail, 100])
        cut = translate([0, h_rail/2+th_holder, -1])(cut)
        result -= cut

        notch = box([2,1.6,100])
        notch = translate([0,th_holder+h_rail,-1])(notch)
        result -= notch

        return result

class partB(Model):
    #straightener holder
    name = project + '-B'

    def render(self):

        dh = th_holder + h_rail
        h = dh + h_wire+d_hole/2+th_hole*2
        w = w_rail+th_holder_side*2

        dl = (l_eye_top-l_eye_mid)/2+1
        dr = dl/3

        result = box([w,h, l_eye])

        o = Outline()

        verts = [
            [w/2,0],
            [w/2,dh+th_holder_top],
            [d_hole/2+dr,h],
            ]

        o.add_verts(verts)
        o.add_verts([(-x[0], x[1]) for x in verts[::-1]])

        result = Poly(o).render()
        result = linear_extrude(l_eye)(result)
        result = translate([0,-h/2,0])(result)


        cut = box([w+2, h, l_eye])
        cut = translate([0,dh+th_holder_top,l_eye_top])(cut)
        result -= cut

        o = Outline()

        verts = [
            [d_hole/2,l_eye_mid/2],
            [d_hole/2+dr,dl],
            [0, dl]
            ]

        o.add_verts(verts)
        o.add_verts([(x[0], -x[1]) for x in verts[::-1]])

        hole = Poly(o).render()
        hole = rotate_extrude()(hole)

        hole = translate([0,-h/2+dh+h_wire,dl-1/2])(hole)
        result -= hole

        result= translate([0,h/2, 0])(result)

        cut = box([w_rail, h_rail, 100])
        cut = translate([0, h_rail/2+th_holder, -1])(cut)
        result -= cut

        notch = box([2,1.6,100])
        notch = translate([0,th_holder+h_rail,-1])(notch)
        result -= notch


        return result


parts = filter(lambda x: Model in inspect.getmro(x[1]) and x[0] != 'Model', inspect.getmembers(sys.modules[__name__], inspect.isclass))

a = partA().render()
b = partB().render()

scad_render_to_file(a+b, project+'.scad')

render = False
if len(sys.argv) > 1:
    if 'render' in sys.argv: render=True

if render:
    for p in parts:
        base = p[1]()
        base.write_stl(base.name+'.stl')


