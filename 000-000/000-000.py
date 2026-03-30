#!/usr/bin/python
import sys, os, time, math
from solid import *
from solid.utils import *

import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

project = '000-000'

d = 26.57+.3+.2+.2
a = 6.28*.375
z = 15.0+2
h = 52.5+2


t = 6.0
xoff = 30.

class partA(Model):
    name = project + '-A'

    def render(self):
        o = Outline()

        r = d/2

        cx = (r+t/2)*math.cos(a/2)
        cy = (r+t/2)*math.sin(a/2)

        verts = []

        verts.extend(arc(t/2, (cx, cy), math.pi+a/2, math.pi)[::-1])

        verts.extend(arc(r, (0,0), a/2, math.pi*2-a, N=128))

        verts.extend(arc(t/2, (cx, -cy), -a/2, math.pi)[::-1])

        verts.extend(arc(r+t, (0,0), 3.14, (2*math.pi-a)/2, N=128)[::-1])

        xedge = max(xoff, r+t)
        verts.extend([
            [min(-r-t, r+t-h), xedge],
            [r+t, xedge]
            ])


        o.add_verts(verts)

        result = Poly(o).render()
        result = linear_extrude(z)(result)

        return result

class partA2(Model):
    name = project + '-A2'

    def render(self):

        d = 27.3+.6

        voff = d/2 + 20.

        tback = 4.0

        o = Outline()

        r = d/2

        cx = (r+t/2)*math.cos(a/2)
        cy = (r+t/2)*math.sin(a/2)

        ax = math.atan2(h/2, voff) + math.acos((r+t)/math.sqrt(h*h/4 + voff*voff)) - math.pi/2

        verts = []

        verts.extend(arc(t/2, (cx, cy), math.pi+a/2, math.pi)[::-1])

        verts.extend(arc(r, (0,0), a/2, math.pi*2-a, N=128))

        verts.extend(arc(t/2, (cx, -cy), -a/2, math.pi)[::-1])

        verts.extend(arc(r+t, (0,0), math.pi*1.5+ax, (math.pi-a)/2-ax, N=128)[::-1])

        xedge = max(xoff, r+t)
        verts.extend([
            [-voff, -h/2],
            [-voff, h/2]
            ])

        verts.extend(arc(r+t, (0,0), a/2, (math.pi-a)/2-ax, N=128)[::-1])

        o.add_verts(verts)

        result = Poly(o).render()
        result = linear_extrude(z)(result)

        slot = box([2,33,100])
        slot = translate([-voff+1+tback,0,-1])(slot)
        result -= slot

        dslot = 11.0
        cut = cylinder(d=dslot, h = voff)
        cut = rotate([0,90,0])(cut)
        cut = translate([-voff+tback+.1,0,z/2])(cut)

        result -= cut

        dguide = 0.13125*7

        cut = cylinder(d=dguide, h = 1000)
        cut = rotate([0,90,0])(cut)
        cut = translate([-500,0,z/2])(cut)

        result -= cut



        return result




class partB(Model):
    #this is just a wedge i didn't wanna make a new project
    name = project + '-B'

    def render(self):
        return box([100,100,100])

        o = Outline()

        L = 42.0
        a = 55*math.pi/180

        W = math.tan(a)*L

        H = 20.
        print(f'{W=}, {L=}')

        o.add_verts([
            [0,0],
            [W/2-1, 0],
            [W/2-1, 1],
            [W/2+1, 1],
            [W/2+1, 0],
            [W,0],
            [W,L],
        ])

        result = Poly(o).render()
        result = linear_extrude(H)(result)

        return result

class partC(Model):
    #a drill guide for pvc holes
    name = project + '-C'

    def render(self):
        ID = 20.25-.3
        OD = d+4.

        ID2 = ID-4.

        hole = 3.175+.6
        offset= 0.3*25.4

        margin = 3.
        cap = 2.

        result = cylinder(d= OD, h = offset + hole/2+margin+cap)
        
        
        pipe = cylinder(d=d, h = 1000)
        cut = cylinder(d=ID, h = 10000)
        pipe -= translate([0,0,-1])(cut)

        result -= translate([0,0,cap])(pipe)

        cut = cylinder(d=ID2, h = 1000)
        result -= translate([0,0,-1])(cut)

        o = Outline()
        o.add_verts(arc(hole/2, (0,0), 0, math.pi))

        o.add_verts([[-hole/2, -50],[hole/2, -50]])

        cut = Poly(o).render()
        cut = linear_extrude([0,0,OD*2])(cut)

        cut = rotate([-90,0,0])(cut)
        cut = translate([0,-25,hole/2+cap+offset])(cut)

        for a in [0,45,90, 135]:
            result -= rotate([0,0,a])(cut)

        return result


class partD(Model):
    #a drill guide for ceiling holes
    name = project + '-D'

    def render(self):
        o = Outline()

        h = 15.0
        d = 25.4*5/16 + .8
        td = 3.
        wshaft = d+2*td-4.

        offset = 1.5*25.4

        wbase = 50.
        tbase = 4.

        harm = h+35.

        a = math.asin(wshaft/(d+td*2))

        o.add_verts([
            [-tbase, -wshaft/2],
            [-tbase, -wbase/2],
            [0,-wbase/2],
            [0,wbase/2],
            [-tbase, wbase/2],
            [-tbase, wshaft/2],
            ])
        o.add_verts(arc((d+2*td)/2, (-offset, 0), a, 2*math.pi-2*a))

        result = Poly(o).render()
        result = linear_extrude(harm)(result) 

        cut = cylinder(d=d, h=100)
        cut = translate([-offset, 0,-20])(cut)
        result -= cut

        cut = box([1000,1000,1000])
        cut = translate([-500, 0, h])(cut)

        result -= translate([-tbase, 0, 0])(cut)
        result -= translate([1, 500+wshaft/2, 0])(cut)
        result -= translate([1, -500-wshaft/2, 0])(cut)

        return result

class partEi(Model):
    #inner pvc clip
    name = project + '-Ei'

    d = 21.75+0.2
    t = 2.0
    a = 6.28*.3
    z = 10.

    def render(self):
        o = Outline()

        d = self.d
        r = d/2

        t = self.t
        a = self.a

        z = self.z

        cx = (r+t/2)*math.cos(a/2)
        cy = (r+t/2)*math.sin(a/2)

        verts = []

        verts.extend(arc(t/2, (cx, cy), math.pi+a/2, math.pi)[::-1])

        verts.extend(arc(r, (0,0), a/2, math.pi*2-a, N=128))

        verts.extend(arc(t/2, (cx, -cy), -a/2, math.pi)[::-1])

        verts.extend(arc(r+t, (0,0), a/2, (2*math.pi-a), N=128)[::-1])

        o.add_verts(verts)

        result = Poly(o).render()
        result = linear_extrude(z)(result)

        return result

class partEo(partEi):
    name = project + '-Eo'

    d = 25.0
    t = 4.0
    a = 6.25*.375
    z = 12.5

class partF(Model):
    #an alignment guide for orthogonalizing clips
    name = project + '-F'

    def render(self):
        o = Outline()

        h = 10.0
        gap = 16.7+.4
        wback = 50.   

        tbase = 1.0
        tbaseinner = 4.0
        tarm = 1.0
        larm = 28.0 

        o.add_verts([
            [-wback/2, 0],
            [-wback/2, tbase],
#            [-gap/2-tarm, tbase],
            [-gap/2-tarm, larm+tbase],
            [-gap/2, larm+tbase],
            [-gap/2, tbaseinner],

            [gap/2, tbaseinner],
            [gap/2, larm+tbase],
            [gap/2+tarm, larm+tbase],
#            [gap/2+tarm, tbase],
            [wback/2, tbase],
            [wback/2, 0],
            ])



        result = Poly(o).render()
        result = linear_extrude(h)(result) 

        return result



parts = filter(lambda x: Model in inspect.getmro(x[1]) and x[0] != 'Model', inspect.getmembers(sys.modules[__name__], inspect.isclass))

base = partEo()

scad_render_to_file(base.render(), project+'.scad')

render = False
if len(sys.argv) > 1:
    if 'render' in sys.argv: render=True

if render:
    for p in parts:
        base = p[1]()
        base.write_stl(base.name+'.stl')


