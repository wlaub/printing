#!/usr/bin/python
import sys, os, time
import math
from solid import *
from solid.utils import *

import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

project = '000-010'

def hex_shape(w):
    o = Outline()
    r = w/(3**0.5)

    verts = [
        [r*math.cos(2*math.pi*(i/6.)), r*math.sin(2*math.pi*(i/6.))]
        for i in range(6)
        ]

    o.add_verts(verts)

    return Poly(o).render()


t = 0.25*25.4

tcap = 0.25*25.4

hscrew = 18.6
dscrew = 4.76+0.6
hnut = 3.1+0.2
wnut = 9.33+0.2

wslot = 25.4

hslot = hscrew - hnut - tcap

class partA(Model):
    name = project + '-A'

    do = 2.75 * 25.4
    di = do - t*2
    h = 4 * 25.4

    def render(self):
        result = cylinder(d=self.do, h=tcap)

        part = cylinder(d=self.di, h = self.h+1)
        part = translate([0,0,tcap-1])(part)

        result += part

        cut = hex_shape(wslot+0.2)
        cut = linear_extrude(hslot+1)(cut)
        cut = translate([0,0,tcap+self.h-hslot])(cut)

        result -= cut

        cut = hex_shape(wnut)
        cut = linear_extrude(hnut+1)(cut)
        cut = translate([0,0,tcap+self.h-hslot-hnut])(cut)

        result -= cut

        cut = cylinder(d = dscrew, h = hscrew+2)
        cut = translate([0,0,tcap+self.h-hscrew-2])(cut)
        result -= cut

        return result

class partB(partA):
    name = project + '-B'

    def render(self):
        result = cylinder(d=self.do, h=tcap)

        cut = hex_shape(wslot)
        cut = linear_extrude(hslot+1)(cut)
        cut = translate([0,0,tcap-1])(cut)

        result += cut

        cut = cylinder(d = dscrew, h = 100)
        cut = translate([0,0,-1])(cut)
        result -= cut

        return result



class partC(partA):
    name = project + '-C'

    di = (3.6*1.15) * 25.4
    do = di + t*2

class partD(partB):
    name = project + '-D'

    di = partC.di
    do = partC.do

print(partC.di)


parts = filter(lambda x: Model in inspect.getmro(x[1]) and x[0] != 'Model', inspect.getmembers(sys.modules[__name__], inspect.isclass))

base = partA().render()

top = partB().render()
top = rotate([180,0,0])(top)
top = translate([0,0,tcap+partA.h+tcap+hslot])(top)

base += top

base = partC().render()

top = partD().render()
top = rotate([180,0,0])(top)
top = translate([0,0,tcap+partA.h+tcap+hslot])(top)

base += top



scad_render_to_file(base, project+'.scad')

render = False
if len(sys.argv) > 1:
    if 'render' in sys.argv: render=True

if render:
    for p in parts:
        base = p[1]()
        base.write_stl(base.name+'.stl')


