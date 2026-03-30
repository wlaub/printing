#!/usr/bin/python
import sys, os, time, math
from solid import *
from solid.utils import *

import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

project = '000-004'

dx = 3*25.4
dy = 0.75 * 25.4
m = 0.5*25.4
d = 2.75+2

w= 19.2 + 0.6

t = 6

class partA(Model):
    name = project + '-A'

    def render(self):

        o = Outline()

        o.add_verts([
            [0,0],
            [0,100],
            [25.4*3.5, 100],
            [25.4*3.5, 100-25.4*1.5],

            ])

        base = Poly(o).render()
        base = linear_extrude(20)(base)
        base =  translate([-dx, -100+dy,0])(base)

        o = Outline()
        o.add_verts([
            [d*1.5,-w/2],
            [0,-w/2],
            [0,w/2],
            [d*1.5,w/2],
            [100, 200],
            [100,-200]
            ])
        cut = Poly(o).render()
        cut = linear_extrude(100)(cut)

#        cut = box([100,w,100])
        cut = translate([-d,0,-50])(cut)

        a = math.pi/2+math.atan2(dx-m, 24*25.4)
        a *= 0.5*180/math.pi

        cut = rotate([0,0,a])(cut)

        base -= cut


        o = Outline()
        o.add_verts([
            [t,t*2],
            [t,100-t],
            [25.4*2.5-t, 100-t],
            [25.4*2.5-t, 100-25.4*1.5-t*2],
            ])
        cut = Poly(o).render()
        cut = linear_extrude(100)(cut)

#        cut = box([100,w,100])
        cut = translate([-dx,-100+dy,-50])(cut)

        cut2 = box([1000,t,1000])
        cut2 = rotate([0,0,-40])(cut2)
        cut2 = translate([-55,0,0])(cut2)
        cut -= cut2

        base -= cut

        return base


class partB(Model):
    name = project + '-B'

    def render(self):
        size = 3*25.4
        sizex = 2.65*25.4
        sizey = 2.85*25.4
        da = math.atan2(.125, 1.5)
        dab = da*2

        a1 = math.atan2(2,24)
        a1_ = a1+da

        a1b = a1_+dab

        a2 = math.atan2(5,14)
        a2_ = a2-da
        a2b = a2_-dab


        ac = (a1+math.pi/2+a2)/2


        cx = 1.25*25.4
        cy = 1.5*25.4

        dr = 0.6
        r1 = 2.5*25.4/2
        r1_ = r1+dr

        r2 = r1-4

        r3 = 1.05*25.4/2
        r3_ = r3+6

        ar = math.pi*0.25

        print((r1+r1_)*ar/(2))

        o = Outline()

        print(cx- math.tan(a1_)*(size-cy))
        o.add_verts([
            [0,0],
            [0,sizey],
            [cx-math.tan(a1_)*(sizey-cy), sizey],

            [cx-math.sin(a1_)*r1_, cy+r1_*math.cos(a1_)],

            *arc(r1_, (cx, cy), math.pi/2+a1_, ar),
            *(arc(r1, (cx, cy), math.pi/2+a1_, ar)[::-1]),

            *arc(r2, (cx, cy), math.pi/2+a1_, ar),

# pipe clip
#            [cx-r3_*math.sin(a1b), cy+r3_*math.cos(a1b)],
#            *arc(r3, (cx, cy), math.pi/2+a1b, math.pi*2-a1b+a2b-math.pi/2),
#            [cx+r3_*math.cos(a2b), cy+r3_*math.sin(a2b)],

            *arc(r2, (cx, cy), a2_-ar, ar),

            *(arc(r1, (cx, cy), a2_-ar, ar)[::-1]),
            *(arc(r1_, (cx, cy), a2_-ar, ar)),

            [sizex, cy+(sizex-cx)*math.tan(a2_)],

            [sizex,0],
            ])

        base = Poly(o).render()
        base = linear_extrude(22, convexity=10)(base)

        base = translate([-cx,-cy,0])(base)

        cut = box([1000, 20,1000])
        cut = translate([500-d,0,-500])(cut)
        cut = rotate([0,0,ac*180/math.pi])(cut)

        base -= cut

        o = Outline()

        aa = math.pi/2-(a1_+ar)
        ab = -(a2_-ar)

        tx = 6

        vl = cy+(cx-tx)*math.tan(aa) - tx
        hl = cx+(cy-tx)/math.tan(ab) - tx

        alpha = (vl-20*cos(aa))/vl

        off = 20
        o.add_verts([
            [tx,tx],
            [tx,tx+vl*alpha],
            [tx+hl*alpha,tx]
        ])

        cut = Poly(o).render()
        cut = linear_extrude(100)(cut)
        cut = translate([-cx, -cy, -50])(cut)

        base -= cut

        return base


class partC(Model):
    name = project + '-C'

    def render(self):
        rc = 0.6

        dr = 10

#        dr = 4
        r3 = 1.05*25.4/2
        r3_ = r3+dr

        ar = math.pi*(0.6*2)

        wled = 13#+0.2
        hled = 2.5#+0.2
        tslot = 1.54#+0.2
        dslot = r3*0.65

        dhole = 4
        htotal = 160
#        htotal = 30

        o = Outline()

        o.add_verts([
            *arc(r3_, (0, 0), -ar/2, ar, N=100),
            [0.5, wled/2],
            [hled, wled/2],

#            [hled, tslot/2],
            *arc(rc, (hled+rc, tslot/2+rc), math.pi, math.pi/2),

#            [dslot, tslot/2],
            *arc(rc, (dslot-rc*3, tslot/2+rc), 3*math.pi/2, math.pi/2),
            *arc(rc, (dslot-rc, tslot/2+rc), 0, math.pi)[::-1],


            *arc(rc, (dslot-rc, -tslot/2-rc), math.pi, math.pi)[::-1],
            *arc(rc, (dslot-rc*3, -tslot/2-rc), 0, math.pi/2),
#            [dslot, -tslot/2],

#            [hled, -tslot/2],
            *arc(rc, (hled+rc, -tslot/2-rc), math.pi/2, math.pi/2),

            [hled, -wled/2],
            [0.5, -wled/2],

            ])

        base = Poly(o).render()
        base = linear_extrude(htotal, convexity=10)(base)

        cut = cylinder(d=1.75+0.25, h=10+dhole)

        for i in [-1,1]:
            _cut = translate([r3,i*wled/2,htotal-dhole])(cut)
            base -= _cut
            _cut = translate([r3,i*wled/2,-10])(cut)
            base -= _cut

        hflange = 2
        hslope = dr*2


        cut = cylinder(r=r3_+10, h=htotal+20)
        cut_ = cylinder(r=r3, h=htotal+40)
        cut -= translate([0,0,-10])(cut_)

        h_=(hslope*r3_/dr)
        hcone = h_+hflange
        hcone_ = hcone+10
        rcone = dr*hcone_/hslope

        cone = cylinder(r1 = rcone, r2=0, h=hcone_)

        cut -= translate([0,0,-10])(cone)
        cone = rotate([180,0,0])(cone)
        cut -= translate([0,0,htotal+hcone_-hcone])(cone)

        base -= cut

        return base



parts = filter(lambda x: Model in inspect.getmro(x[1]) and x[0] != 'Model', inspect.getmembers(sys.modules[__name__], inspect.isclass))

base = partC()

scad_render_to_file(base.render(), project+'.scad')

render = False
if len(sys.argv) > 1:
    if 'render' in sys.argv: render=True

if render:
    for p in parts:
        base = p[1]()
        base.write_stl(base.name+'.stl')


