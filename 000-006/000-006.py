#!/usr/bin/python
import sys, os, time
import math
from solid import *
from solid.utils import *

import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

project = '000-006'

s = 15.5
h = 3.2
w_wire = 1.0

class partA(Model):
    name = project + '-A'

    def render(self):

        result = box([s,s,h])

        tbot = 0.2

        #center peg
        cut = cylinder(d=3.2, h=100)
        cut = translate([0,0,tbot])(cut)
        result -= cut

        #side pegs
        cut = cylinder(d=1.8, h=100)
        cut = translate([0,0,tbot])(cut)
        for i in [-1,1]:
            result -= translate([i*5.22,0,0])(cut)

        #pin cutout
        cut = box([100,100,100])
        cut = translate([50,50, -10])(cut)
        cut = translate([-2.0,3.0,0])(cut)
        result -= cut

        #wire channel
#        cut = box([w_wire,100,100])
#        cut = translate([5.22/2,0,h-2.0])(cut)
#        result -= cut

        o = Outline()
        ro = 5.22/2 + w_wire/2
        ri = 5.22/2 - w_wire/2
        a = 3.14/4
        a = 3.14*.35
        xoff = -2
        dx = ro*math.cos(a)+100*math.cos(a)
        dy = ro*math.sin(a) - 100*math.sin(a)
        dx2 = ri*math.cos(a)+100*math.cos(a)
        dy2 = ri*math.sin(a) - 100*math.sin(a)
        o.add_verts([
            [ro, 100],
            *arc(ro, (0,xoff), -a, a)[::-1],
            [dy, -dx+xoff],
            [dy2, -dx2+xoff],
            *arc(ri, (0,xoff), -a, a),
        ])

        cut = Poly(o).render()
        cut = linear_extrude(100)(cut)
        cut = translate([0,0,h-2.0])(cut)
        result -= cut

        return result

class partB(Model):
    name = project + 'B'

    def render(self):

        #connector
        ch = 5.15
        cw = 5.5
        cd = 17.22
        cbod = 8.6

        cwx = 5.1
        cwd = cw-cwx

        #bottom/top thickness
        tbot = 1
        ttop = 1

        #margin bot/top
        mbot = 1.5
        mtop = 2

        sidechan = 3.75

        #part bounds
        pw = 14
        ph = ch + tbot + ttop
        pd = cd + mbot + mtop

        print(f'{pw}x{pd}x{ph}')

        result = box([pw, pd, ph])

        o = Outline()
        o.add_verts([
            [0,0],
            [100,0],
            [100,sidechan],
            [cw,sidechan],
            [cw, sidechan+cbod],
            [cw-cwd/2, sidechan+cbod],
            [cw-cwd/2, 100],
            [0, 100],
            [cwd/2, sidechan+cbod],
            [0, sidechan+cbod],
            ])

        cut = Poly(o).render()
        cut = linear_extrude(ph)(cut)
        cut = translate([-cw/2,-pd/2+mbot,tbot])(cut)

        result -= cut

        #
        dy = 2
        dx = mbot+sidechan+0.5
        a = math.atan2(dy, dx)
        a_ = a * 180/math.pi

        cut = box([100,100,100])
        cut = rotate([a_,0,0])(cut)
        cut = translate([0,-pd/2+dx,ph])(cut)
        result -= cut

        #
        dy = 2
        dx = (pw-cw)/2-1
        a = math.atan2(dy, dx)
        a_ = a * 180/math.pi

        cut = box([100,100,100])
        cut = rotate([0,a_,0])(cut)
        cut = translate([pw/2-dx,0,ph])(cut)
        result -= cut

        #
        dy = 2
        dx = (pw-cw)/2-1
        a = math.atan2(dy, dx)
        a_ = a * 180/math.pi

        cut = box([100,100,100])
        cut = rotate([0,-a_,0])(cut)
        cut = translate([-(pw/2-dx),0,ph])(cut)
        result -= cut



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


