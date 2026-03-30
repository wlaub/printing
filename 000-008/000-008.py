#!/usr/bin/python
import sys, os, time
from solid import *
from solid.utils import *

import math
import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

project = '000-008'

rmax = 40.
roffset = 1

aburr = 0.2
dburr = 5.
#dburr = 4.
tgap = 1.4

rhole = 1.8/2

hbase = 5.
tbase = 1.5

tclear = 0.5
tslide = 0.25

tclear = 0.35
tslide = 0.15

hhold = 7.
hpeg = 4.

tlid = 2

lid_depth = 2.5
lid_width = 2.5

N = floor(rmax/(dburr+tgap))

class partA(Model):
    name = project + '-A'

    def render(self):

        wburr = dburr
        a = aburr*math.pi
        hburr = math.tan(a)*wburr

        o = Outline()
        o.add_verts([
            [-wburr/2, 0],
            [0, hburr/2],
            [wburr/2, 0],
            [0, -hburr/2],
            ])
        burr = Poly(o).render()
        burr = linear_extrude(hbase+tbase/2)(burr)
        burr = translate([0,0,tbase/2])(burr)

        result = box([(wburr+tgap)*4+tbase*2,(hburr+tgap)*6,tbase+hbase+tclear])

        cut = box([(wburr+tgap)*4,(hburr+tgap)*6+2,tbase+hbase+tclear])
        cut = translate([0,0,tbase])(cut)


        for i in [-2,0,2]:
            for j in range(-2,3):
                cut -= translate([i*(wburr+tgap),j*(hburr+tgap),0])(burr)

        result -= cut

        return result


class partB(Model):
    name = project + '-B'

    def render(self):

        wburr = dburr
        a = aburr*math.pi
        hburr = math.tan(a)*wburr

        o = Outline()
        o.add_verts([
            [-wburr/2, 0],
            [0, hburr/2],
            [wburr/2, 0],
            [0, -hburr/2],
            ])
        burr = Poly(o).render()
        burr = linear_extrude(hbase+tbase/2)(burr)
        burr = translate([0,0,tbase/2])(burr)

        result = box([(wburr+tgap)*4+tbase*2+tbase*2+tclear*2,(hburr+tgap)*6,tbase+hbase+tclear])

        cut = box([(wburr+tgap)*4+tbase*2+tclear*2,(hburr+tgap)*6+2,tbase+hbase+tclear])
        cut = translate([0,0,tbase])(cut)


        for i in [-1,1]:
            for j in range(-2,3):
                cut -= translate([i*(wburr+tgap),j*(hburr+tgap),0])(burr)

        result -= cut

        return result



class partC(Model):
    name = project + '-C'

    inner = True
    phase = 1


    def get_base_cylinder(self):
        rextra = 0
        if not self.inner:
            rextra = tbase+tslide

        base_r = self.base_r = N*(dburr+tgap)+(tbase-tgap+tslide)

        hextra = tlid
        if not self.inner:
            hextra = hhold

        result = cylinder(r = base_r+tbase+rextra, h=tbase+tclear+hbase+hextra)
        result = translate([0,0,-hextra])(result)
        return result, base_r, rextra, hextra

    def get_lid_socket_cuts(self, base_r, rextra, minus=False):
        w_effective = lid_width
        if minus:
            w_effective -= 0.1
        hole = box([lid_depth*2, w_effective, 1000])
        hole = translate([0,0,-1000])(hole)
        offset = base_r+rextra+tbase
        sub_hole = translate([offset,0,0])(hole)

        M = int(offset*2*math.pi/(lid_width*2))

        socket_cut = translate([0,0,0])(sub_hole)
        for ma in range(1,M):
            a = 360*ma/M
            socket_cut += rotate([0,0,a])(sub_hole)
        return socket_cut

    def render(self):

        if self.inner:
            self.phase = 0
        else:
            self.phase = 1

        wburr = dburr
        a = aburr*math.pi
        hburr = math.tan(a)*wburr

        o = Outline()
        o.add_verts([
            [-wburr/2, 0],
            [0, hburr/2],
            [wburr/2, 0],
            [0, -hburr/2],
            ])
        burr = Poly(o).render()
        burr = linear_extrude(hbase+tbase/2)(burr)
        burr = translate([wburr/2,0,tbase/2])(burr)

        result, base_r, rextra, hextra = self.get_base_cylinder()

        cut = cylinder(r = base_r+rextra, h=tbase+tclear+hbase)

        print(2*(base_r+rextra+tbase))

#        cut = box([(wburr+tgap)*4,(hburr+tgap)*6+2,tbase+hbase+tclear])
        cut = translate([0,0,tbase])(cut)

#        result += burr

#        hole = cylinder(r=rhole, h=tbase*2)
#        hole = box([rhole*2, rhole*2, tbase*2])
#        hole = translate([0,0,-tbase*2+tbase+tclear])(hole)
        hole = box([rhole*2, rhole*2, 1000])
        hole = translate([0,0,-500])(hole)

        for nr in range(N)[self.phase::2]:
            r = nr*(dburr+tgap)+roffset
            circ = 2*math.pi*(r+dburr/2)
            M = int(circ/(hburr+tgap))

            sub_burr = translate([r,0,0])(burr)
            sub_hole = translate([r-rhole,0,0])(hole)
            sub_hole2 = translate([r+dburr+rhole,0,0])(hole)
            for ma in range(M):
                a = 360*ma/M
                cut -= rotate([0,0,a])(sub_burr)
                if self.inner:
                    if nr != 0:
                        cut += rotate([0,0,a])(sub_hole)
                    if nr < N-1:
                        cut += rotate([0,0,a])(sub_hole2)

        #lid socket
        if self.inner:
            socket_cut = self.get_lid_socket_cuts(base_r, rextra)

            cut += socket_cut

        #inner ring
        if not self.inner and False:
            r_ring = base_r-dburr/4-tbase/2
            ring = cylinder(r=r_ring, h=hbase+tbase/2)
            ring_hole = cylinder(r = r_ring-tbase-tclear, h= 1000)
            ring_hole = translate([0,0,-1])(ring_hole)
            ring -= ring_hole
            ring = translate([0,0,tbase/2])(ring)
            cut -= ring

        #crank socket
        if not self.inner:
            r_sock = dburr
            o = Outline()
            verts = []
            for i in range(8):
                a = i*math.pi/4
                verts.append([r_sock*math.cos(a), r_sock*math.sin(a)])
            o.add_verts(verts)

            sock = Poly(o).render()
            sock = linear_extrude(1000)(sock)
            sock = translate([0,0,-1000+tbase-hpeg])(sock)
            cut += sock

        #center peg socket
        if not self.inner:
            peg = cylinder(r=dburr+tslide, h=hbase+tbase/2+hpeg)
            peg = translate([0,0,tbase-hpeg-2])(peg)
            cut += peg

        #finger holes
        if not self.inner:
            peg = cylinder(r=3.5, h =100)
            peg = translate([0,0,-100-hextra+3])(peg)
            peg = translate([r-tbase*2,0,0])(peg)
            for i in range(7):
                cut += rotate([0,0,360*i/7])(peg)


        hole = box([rhole, rhole*2, 100])
        if not self.inner:
            sub_hole = translate([base_r+rextra,0,tbase-1])(hole)
            cut += sub_hole
        else:
            sub_hole = translate([base_r+rextra+tbase,0,-50])(hole)
            cut += sub_hole

#        for i in [-2,0,2]:
#            for j in range(-2,3):
#                result += translate([i*(wburr+tgap),j*(hburr+tgap),0])(burr)

        result -= cut

        #center peg
        if self.inner:
            peg = cylinder(r=dburr, h=hbase+tbase/2+hpeg)
            peg = translate([0,0,tbase/2])(peg)
            result += peg


        return result

class partD(partC):
    name = project + '-D'

    inner = False
    phase = 0


class partE(partC):
    name = project + '-E'

    def render(self):
        result, base_r, rextra, hextra = self.get_base_cylinder()
        socket_cut = self.get_lid_socket_cuts(base_r, rextra, minus=True)
        result -= socket_cut
        result = rotate([180,0,0])(result)
        r = (N-1)*(dburr+tgap)+roffset +rhole+2#+ dburr+rhole
        r = base_r +rextra+tbase-lid_depth+1
        top = cylinder(r=r, h=100)
        top = translate([0,0,tbase+tclear])(top)

        result +=  top

        return result


parts = filter(lambda x: Model in inspect.getmro(x[1]) and x[0] != 'Model', inspect.getmembers(sys.modules[__name__], inspect.isclass))

base = partE()

view = base.render()
base2 = partD().render()
#base2 = rotate([180,0,0])(base2)
#base2 = translate([0,0,tbase+hbase+tbase+tclear])(base2)
#base2 = translate([0,0,-tbase])(base2)
#view+=base2
view += translate([base.base_r*2+5,0,0])(base2)

scad_render_to_file(view, project+'.scad')

render = False
if len(sys.argv) > 1:
    if 'render' in sys.argv: render=True

if render:
    for p in parts:
        base = p[1]()
        base.write_stl(base.name+'.stl')


