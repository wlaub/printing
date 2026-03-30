#!/usr/bin/python
import sys, os, time, math
from solid import *
from solid.utils import *

import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

project = '000-001'

#actual
rrod = 4.0
rbear = 11.0
rarm = 30.0

ledge = 40.0
hedge = 16.0
sedge = 80.0

z = 25.4/2

width = 550

hhinge = 25

N = 7

#real
if False:
    rrod = 1.6
    rbear = 1.6
    rarm = 10.0

    ledge = 20.0
    hedge = 6.0
    sedge = 0.0

    z = 8.0



hledge = max(sedge,ledge+hedge*2)

class partA(Model):
    # arm
    name = project + '-A'

    def render(self):
        o = Outline()

        verts = []
        
        verts.extend(arc(rarm, (0,0), 0, math.pi))

        h = hledge * N

        for i in range(N):
            tverts = [
                [0,0],
                [0,hedge],
                [ledge, hedge+ledge], 
                [ledge, hedge*2+ledge],
                [0, hedge*2+ledge],
                ]
            verts.extend([[-x-rarm, -y-i*hledge] for x,y in tverts])

        verts.extend(arc(rarm, (0,-h), math.pi, math.pi))

        o.add_verts(verts)
        result =  Poly(o).render()

        result = linear_extrude(z, convexity=10)(result)

        cut = cylinder(r=rrod, h=1000)
        result -= translate([0,-h,-10])(cut)

        cut = cylinder(r=rbear, h=1000)
        result -= translate([0,0,-10])(cut)

        result = color([1,0,0])(result)

        return result

class partB(Model):
    # Hinge
    name = project + '-B'

    def render(self):
        o = Outline()

        verts = []
        
        verts.extend(arc(rarm, (0,0), 0, math.pi)[::-1])

        verts.extend(arc(rarm, (width,0), 0, math.pi)[::-1])

        verts.extend([
            [width+rarm, -rarm-hhinge],
            [-rarm, -rarm-hhinge], 
            ])

        o.add_verts(verts)
        result =  Poly(o).render()

        result = linear_extrude(z)(result)

        cut = cylinder(r=rrod, h=1000)
        result -= translate([0,0,-10])(cut)
        result -= translate([width,0,-10])(cut)

        result = color([0,1,0])(result)

        return result

class partC(Model):
    # Platform
    name = project + '-C'

    def render(self):
        o = Outline()

        verts = []
        
        iw = width-rarm*2

        verts.extend([
            [0,0],
            [-rarm, 0],
            [-rarm, iw],
            [0, iw],
            [0, iw+z],
            [iw, iw+z],
            [iw, iw],
            [iw+rarm, iw],
            [iw+rarm, 0],
            [iw, 0],
            [iw, -z],
            [0, -z],
            ])

        o.add_verts(verts)
        result =  Poly(o).render()

        result = linear_extrude(z)(result)

        result = color([0,0,1])(result)

        return result




parts = filter(lambda x: Model in inspect.getmro(x[1]) and x[0] != 'Model', inspect.getmembers(sys.modules[__name__], inspect.isclass))

base = partC().render()

base = translate([rarm,0,0])(base)

arm = partA().render()

arm = rotate([-90,0,180])(arm)
arm = translate([0,0,-hledge+z])(arm)

base += arm
base += translate([0, width-rarm*2+z,0])(arm)

arm = rotate([0,0,180])(arm)

base += translate([width,-z,0])(arm)
base += translate([width, width-rarm*2,0])(arm)

hinge = partB().render()

hinge = rotate([90,0,0])(hinge)
hinge = translate([0,-z,-hledge+z])(hinge)

base += hinge
base += translate([0,z*2,0])(hinge)

base += translate([0,width-rarm*2+z,0])(hinge)
base += translate([0,width-rarm*2+3*z,0])(hinge)

lrod = width-2*rarm+4*z+z
lrod = 600.
rod = cylinder(r=rrod, h=lrod)
rod = rotate([90,0,0])(rod)
rod = translate([0,lrod/2+width/2-rarm,-hledge+z])(rod)

base += rod
base += translate([width,0,0])(rod)
base += translate([width,0,hledge*N])(rod)
base += translate([0,0,hledge*N])(rod)

plat = partC().render()

base += translate([rarm,0,hledge*5])(plat)

base = translate([0,0,hledge-z+hhinge+rarm])(base)

base += translate([0,-100,0])(rotate([0,0,90])(partA().render()))
base += translate([0,-220,0])(rotate([0,0,0])(partB().render()))
base += translate([0,-300-width,0])(rotate([0,0,0])(partC().render()))



scad_render_to_file(base, project+'.scad')

render = False
if len(sys.argv) > 1:
    if 'render' in sys.argv: render=True

if render:
    for p in parts:
        base = p[1]()
        base.write_stl(base.name+'.stl')


