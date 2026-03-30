#!/usr/bin/python
import sys, os, time
from solid import *
from solid.utils import *

import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

project = '000-009'

lslope = 1.0/10.0

w_page = 8.5*25.4
h_page = 11*25.4

inner = 0.25*25.4
outer = 40

w_inner = w_page - 2*inner
h_inner = h_page - 2*inner

w_outer = w_page + 2*outer
h_outer = h_page + 2*outer

t_inner = 0.5
shadow = t_inner/lslope

steps = [t_inner, 1.0, 2.0]

t_outer = 1.0

rim = t_outer/lslope - shadow + 1.0
print(rim)

margin = 1.0

class partA(Model):
    name = project + '-A'

    def render(self):
        t_outer = max(steps)
        result = box([w_outer,h_outer,t_outer])

        cut = box([w_inner, h_inner, 100])
        cut = translate([0,0,-1])(cut)
        result -= cut

        for t_cut, t_ref in zip(steps[:-1], steps[1:]):

            rim = t_ref/lslope - shadow + 1.0
            print(rim)

            cut = box([w_inner+2*rim, h_inner+2*rim, 100])
            cut = translate([0,0,t_cut])(cut)
            result -= cut

        cut = box([w_outer, h_outer, 100])
        cut = translate([-w_outer/2-margin, -h_outer/2-margin, -2])(cut)

        result *= cut

        return result

class partB(Model):
    name = project + '-B'

    def render(self):
        result = partA().render()
        result = mirror([0,1,0])(result)
        return result


class partC(Model):
    """
    i didn't want to make a new project so i stuck the joystick shroud in here good luck finding it again asshole and yes this like is longer than eighty characters long
    """
    name = project + '-C'

    def render(self):

        shroud_inner_height=12

        rim_height = 1.75
        rim_radius = 5+0.2
        rim_thickness = 0.4
        top_wall_thickness = 0.4

        o = Outline()

        bh = 16.03
        bw = 16.05

#        dyl = 3.33
#        wl = 9.65
#        hl = 3.66

#        dxt = 3.42
#        wt = 9.55
#        ht = 3.76

        wl = 11.9
        dyl = (bh-wl)/2
        hl = 3.66

        wt = 11.9
        dxt = (bw-wt)/2
        ht = 3.76

        wr = 9.61
        dyr = (bh-wr)/2
        hr = 6.07

        wb = 11.27#7
        dxb = (bw-wb)/2
        hb = 0.6

        o.add_verts([
            [0,         0],
            [dxt,      0,],
            [dxt,      ht],
            [dxt+wt,   ht],
            [dxt+wt,   0],

            [bw,       0],
            [bw,       -dyl],
            [bw+hl,    -dyl],
            [bw+hl,    -dyl-wl],
            [bw,       -dyl-wl],

            [bw,       -bh],
            [dxb+wb,   -bh],
            [dxb+wb,   -bh-hb],
            [dxb,      -bh-hb],
            [dxb,      -bh],

            [0,         -bh],
            [0,         -dyr-wr],
            [-hr,        -dyr-wr],
            [-hr,        -dyr],
            [0,         -dyr],
            ])

        ref = Poly(o).render()
        ref = linear_extrude(shroud_inner_height, convexity=10)(ref)

        tbase = 0.2
        tsides = 0.3
        tgap = 0.5

        ref = translate([-bw/2, bh/2, 0])(ref)

        o = Outline()

        bh += tbase
        bw += tbase

        dyl -= tsides-tbase/2
        wl += tsides*2
        hl += tgap-tbase/2

        dxt -= tsides-tbase/2
        wt += tsides*2
        ht += tgap-tbase/2

        dyr -= tsides-tbase/2
        wr += tsides*2
        hr += tgap-tbase/2

        dxb -= tsides-tbase/2
        wb += tsides*2
        hb += tgap-tbase/2



        o.add_verts([
            [0,         0],
            [dxt,      0,],
            [dxt,      ht],
            [dxt+wt,   ht],
            [dxt+wt,   0],

            [bw,       0],
            [bw,       -dyl],
            [bw+hl,    -dyl],
            [bw+hl,    -dyl-wl],
            [bw,       -dyl-wl],

            [bw,       -bh],
            [dxb+wb,   -bh],
            [dxb+wb,   -bh-hb],
            [dxb,      -bh-hb],
            [dxb,      -bh],

            [0,         -bh],
            [0,         -dyr-wr],
            [-hr,        -dyr-wr],
            [-hr,        -dyr],
            [0,         -dyr],
            ])

        cut = Poly(o).render()
        cut = linear_extrude(100, convexity=10)(cut)
        cut = translate([-bw/2, bh/2, 0])(cut)

        tbase = 0.8
        tsides = 0.4
        tgap = 0.4

        o = Outline()

        bh += tbase
        bw += tbase

        dyl -= tsides-tbase/2
        wl += tsides*2
        hl += tgap-tbase/2

        dxt -= tsides-tbase/2
        wt += tsides*2
        ht += tgap-tbase/2

        dyr -= tsides-tbase/2
        wr += tsides*2
        hr += tgap-tbase/2

        dxb -= tsides-tbase/2
        wb += tsides*2
        hb += tgap-tbase/2

        o.add_verts([
            [0,         0],
            [dxt,      0,],
            [dxt,      ht],
            [dxt+wt,   ht],
            [dxt+wt,   0],

            [bw,       0],
            [bw,       -dyl],
            [bw+hl,    -dyl],
            [bw+hl,    -dyl-wl],
            [bw,       -dyl-wl],

            [bw,       -bh],
            [dxb+wb,   -bh],
            [dxb+wb,   -bh-hb],
            [dxb,      -bh-hb],
            [dxb,      -bh],

            [0,         -bh],
            [0,         -dyr-wr],
            [-hr,        -dyr-wr],
            [-hr,        -dyr],
            [0,         -dyr],
            ])


        result = Poly(o).render()
        result = linear_extrude(shroud_inner_height, convexity=10)(result)
        result = translate([-bw/2, bh/2, 0])(result)

        cut = translate([0,0,top_wall_thickness])(cut)
        result -= cut
#        result += ref




        rim = cylinder(r2 = rim_radius+rim_thickness, r1=bw/2-2, h=rim_height-top_wall_thickness/2)

        hole = cylinder(r=rim_radius, h = 100)
        hole = translate([0,0,-50])(hole)

        rim = rotate([180,0,0])(rim)
        rim = translate([0,0,top_wall_thickness/2])(rim)

        result += rim

        result -= hole

        return result


class partD(Model):
    name = project + '-D'

    def render(self):

        rim_height = 1.75
        rim_radius = 5+0.2
        rim_thickness = 0.4
        top_wall_thickness = 0.4
        hole_radius = 11.28/2-.2
        plug_depth = 0.5

        bh = 16.03
        bw = 16.05-2

        rim_radius -= 0.2

        result = rim = cylinder(r2 = rim_radius+rim_thickness, r1=bw/2, h=rim_height-top_wall_thickness/2)

        plug = cylinder(r=hole_radius, h= plug_depth+.1)

        plug = translate([0,0,-plug_depth])(plug)
        result  += plug

        hole = cylinder(r=rim_radius, h = 100)
        hole = translate([0,0,-50])(hole)

        result = rotate([180,0,0])(result)

        result -= hole

        return result

class partE(Model):
    name = project + '-E'

    def render(self):

        w = 9.52+0.4
        d = 6.01+0.4
        h = 9.54+0.6

        td = 0.6
        tw = 1.6
        th = 0.8

        result = box([w+tw,d+td,h+th])

        cut = box([w,100,100])

        cut = translate([0,50-d/2, th])(cut)

        result -= cut

        result = rotate([90,0,0])(result)

        return result




parts = filter(lambda x: Model in inspect.getmro(x[1]) and x[0] != 'Model', inspect.getmembers(sys.modules[__name__], inspect.isclass))

base = partA().render()
base += partB().render()

base = partE().render()

scad_render_to_file(base, project+'.scad')

render = False
if len(sys.argv) > 1:
    if 'render' in sys.argv: render=True

if render:
    for p in parts:
        base = p[1]()
        base.write_stl(base.name+'.stl')


