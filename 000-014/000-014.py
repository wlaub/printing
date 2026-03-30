#!/usr/bin/python
import sys, os, time, math
from solid import *
from solid.utils import *

import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

project = '000-014'

fdist = 1000 #focal distance
foff = 250 #focal offset

"""
1350 px/m^2
100: 2473 -> 1.83 m^2, rect = 2.34 m^2      78.2%
500: 5669*2 -> 8.4 m^2, rect = 11.6 m^2     72.4%
1000: 9800*2 -> 14.5 m^2, rect = 22.5 m^2   64.4%
1500: 12482*2 -> 18.5 m^2, rect = 31 m^2    59.7%
2000: 12947*2 -> 19.2 m^2, rect = 36.5 m^2  52.6%
"""

#fdist = 2000
#foff = 1000

size = 100

res = 10

base_height = 3

class partA(Model):
    name = project + '-A'

    def render(self):

        return box([1,1,1])

        o = Outline()

        curve = lambda x: x*x/(4*fdist)

        left = foff-size*.707-10
        right = left+size*1.41+20
        if left < 0:
            left = 0

        left = 1
        right = 10000

        N = math.ceil((right-left)/res)
        dx = (right-left)/(N-1)

        print(left, right, N, dx, res)

        voff = min(curve(left), curve(right))

        verts = []
        for i in range(N):
            x = left + i*dx
            y = curve(x)-voff
            verts.append((x,y))

        o.add_verts(verts)

        o.add_verts([
            [right,-base_height],
            [left,-base_height],
            ])

        result = Poly(o).render()
#        result = rotate([90,0,0])(result)

        result = rotate_extrude()(result)

        parabola = result = translate([0,0,-fdist])(result)

        rmax = 3000
        hcyl = 3*fdist
        cut = cylinder(r=rmax, h = hcyl)
        cut = translate([0,0,-hcyl/2])(cut)
        cut = rotate([90,0,0])(cut)

        result *= cut


        amin = 45
        amax = 90

        s = 100000/4
        cut = box([s,s,s])
        cut = translate([0,0,-s])(cut)
        result -=rotate([0,amin,0])(cut)

        result = rotate([0,-amax,0])(result)
        result -= cut
        result = rotate([0,amax,0])(result)

        result -= translate([0,0,-10])(parabola)

#        cut = box([size, size, 1000])
#        cut = translate([foff, 0,-100])(cut)

#        result *= cut

#        result =  translate([-foff,0,0])(result)

#        result = rotate([0,-45,0])(result)

        return result


W = 40/2
margin = 5

class partB(Model):
    name = project + '-B'

    def render(self):

        #need to carve out stair case by subtracting polygonal extrusions

        o = Outline()

        a = 1/(4*fdist)

        prev = 0
        for N in range(1,20):
            xN = 2*W*N
            xl = xN - W+margin
            xr = xN + W-margin

            yl = a*xN*xl
            yr = a*xN*xr

            o.add_verts([
                [xl, prev],
                [xl, yl],
                #teeth?
                [xr, yl],
                [xr, yr],
                ])
            prev = yr

        o.add_verts([[xr, 0]])

        result = Poly(o).render()

        result = rotate_extrude()(result)

        size = 150
        foff = int(500/(2*W))*2*W

        cut = box([size, size, 1000])
        cut = translate([foff, 0,-100])(cut)

        result *= cut

        result = translate([-foff,0,0])(result)


        result = translate([0,0,-20])(result)
        cut = box([size*2, size*2, 1000])
        cut = translate([0,0,-1000])(cut)

        result -= cut

        return result


class partC(Model):
    name = project + '-C'

    def render(self):

        thickness = 7.
        thickness = 2.4
        f_thick = 2.4
        height = 70
        dbar = 12.7+0.3
        support_height = 25

        o = Outline()
        o_cut = Outline()
        o_speed_holes = Outline()

        curve = lambda x: x*x/(4*fdist)

        left = 1200
        right = left+200

        N = math.ceil((right-left)/res)
        dx = (right-left)/(N-1)

        print(left, right, N, dx, res)

        voff = min(curve(left), curve(right))

        verts = []
        for i in range(N):
            x = left + i*dx
            y = curve(x)-voff
            verts.append((x,y))

        right_height = y

        o.add_verts(verts)

        # bottom curve
        verts = []
        for i in range(N+2):
            i = N-1-i+1
            x = left + i*dx
            y = curve(x)-voff
            verts.append((x,y-thickness))

        o_cut.add_verts(verts)
#        o.add_verts(verts)

        #speed holes
        verts = []
        dx = (right-left-f_thick*2)/(N-1)
        for i in range(N):
            x = left +f_thick + i*dx
            y = curve(x)-voff
            verts.append((x,y-thickness-f_thick))
        o_speed_holes.add_verts(verts)


        ybase = min(right_height-20, curve(left)-voff-thickness-f_thick-3)
        o.add_verts([
            [right, ybase],
            [left, ybase],
            ])
        o_cut.add_verts([[left, ybase-1],[right, ybase-1]])
        o_speed_holes.add_verts([
            [right-f_thick, ybase+f_thick],
            [left+f_thick, ybase+f_thick],
            ])

        result = Poly(o).render()

        result = linear_extrude(height+dbar)(result)

        cut = Poly(o_cut).render()
        cut = linear_extrude(height+dbar)(cut)
        cut = translate([0,0,support_height])(cut)

        result -= cut

        cut = Poly(o_speed_holes).render()
        cut = linear_extrude(height+dbar+10)(cut)
        cut_speed_hole = translate([0,voff,-5])(cut)

        result = translate([0,voff,0])(result)

        x = (left+right)/2
        a = math.atan2(curve(x)-fdist, x)
        a *= 180/math.pi
        print(a)


        bar = cylinder(d=dbar, h=2000)

        bar = rotate([-a,90,0])(bar)

#        bar = translate([0,fdist,height+dbar/2])(bar)
        bar = translate([0,fdist,dbar/2])(bar)
        bar2 = translate([0,0,-100])(bar)

        bar = hull()(bar, bar2)

        result -= bar

        bar_wrapper = minkowski()(bar, sphere(r=f_thick))
        cut_speed_hole -= bar_wrapper

        result -= cut_speed_hole




#        result =  translate([-left,0,0])(result)

#        handle = box([20,20, height])
#        handle = translate([right-foff-10,right_height-10-thickness/2,0])(handle)
#        result += handle

#        cut = box([size, size, 1000])
#        cut = translate([foff, 0,-100])(cut)

#        result *= cut


        return result

def cham(r, p1, c, p2, loud = False):

    x1,y1 = p1
    x2,y2 = p2
    xc,yc = c

    dx1 = x1-xc
    dy1 = y1-yc
    dx2 = x2-xc
    dy2 = y2-yc

    D1 = (dx1**2+dy1**2)**0.5
    D2 = (dx2**2+dy2**2)**0.5

    a1 = math.atan2(dy1, dx1)
    a2 = math.atan2(dy2, dx2)

    da = a2-a1
    if da < 0: da+=math.pi*2
    if da > math.pi*2: da-=math.pi*2

    if da > math.pi:
        da = 2*math.pi - da

    da /= 2

    dxc = (dx1/D1+dx2/D2)/2
    dyc = (dy1/D1+dy2/D2)/2
    al = math.atan2(dyc, dxc)
#    al = da+a1

    D = r/math.sin(da)
    L = r/math.tan(da)

    cx = xc + D*math.cos(al)
    cy = yc + D*math.sin(al)

    tx1 = xc+L*math.cos(a1)
    ty1 = yc+L*math.sin(a1)

    tx2 = xc+L*math.cos(a2)
    ty2 = yc+L*math.sin(a2)

    tdx1 = tx1-cx
    tdy1 = ty1-cy

    tdx2 = tx2-cx
    tdy2 = ty2-cy


    sa = math.atan2(tdy1, tdx1)
    ea = math.atan2(tdy2, tdx2)

    if sa < 0: sa+=2*math.pi
    if ea < 0: ea+=2*math.pi

    result = []
#    result.append([x1,y1])

    a1n = a1
    a2n = a2
    if a1n < 0: a1n += math.pi*2
    if a2n < 0: a2n += math.pi*2



    aa = math.pi-da*2

    aa = ea-sa

    if aa < -math.pi:
        aa += 2*math.pi
    if aa > math.pi:
        aa -= 2*math.pi

#    aa=1.68

    if loud:
#        print([_*180/math.pi for _ in (a1, a2, da, al, aa, sa, ea, eao)])
        print([_*180/math.pi for _ in (aa, sa, ea, a1, a2)])

#    result.append([tx1, ty1])
#    result.append([cx, cy])
#    result.append([tx2, ty2])

#    result.append([xc, yc])



    inc = 1
    if aa < 0:
        inc = -1
        sa = ea
        aa*= -1
#        print(sa, aa, inc)
    result.extend(arc(r, (cx, cy), sa, aa)[::inc])

#    result.append([x2,y2])
    return result

def cap(r, x1, x2):
    pass

def plug(x,y,r,h,d,t, sx = 1, sy = 1, order = 1, r2=None):

    if r2 is None:
        r2 = r

    corners = [
        [0, h/2+4*r],
        [0, h/2+2*r],
        [t+r*2, h/2+2*r],
        [t+r*2, h/2],
        [-d, h/2],
        [-d, -h/2],
        [t+r*2, -h/2],
        [t+r*2, -h/2-2*r],
        [0, -h/2-2*r],
        [0, -h/2-4*r],
        ]
    rads = [0,r2,r,r,r2,r2,r,r,r2,0]

    chamed = []
    for i in range(1, len(corners)-1):
        x1 = corners[i-1]
        c = corners[i]
        x2 = corners[i+1]

        chamed.extend(cham(rads[i], x1, c, x2))

    result = chamed
    result = [[x+a*sx, y+sy*b] for a,b in result[::order]]

    return result

    result = []
    result.extend(arc(r, (r, h/2+3*r), math.pi, math.pi/2))
    result.extend(arc(r, (r+t, h/2+r), math.pi*1.5, math.pi)[::-1])

    result.extend(arc(r, (-d+r, h/2-r), math.pi/2, math.pi/2))

    result.extend(arc(r, (-d+r, -h/2+r), math.pi, math.pi/2))

    result.extend(arc(r, (r+t, -h/2-r), math.pi*1.5, math.pi)[::-1])
    result.extend(arc(r, (r, -h/2-3*r), math.pi/2, math.pi/2))

    result = [[x+a*sx, y+sy*b] for a,b in result[::order]]

    return result

def socket(x,y,r,h,d,t, sx = 1, sy = 1, order = 1, pinch = 0, r2=None):
    if r2 is None:
        r2 = r

    hp = h-pinch

    corners = [
        [0, -hp/2-r],
        [0, -hp/2],
        [-d+2*r, -h/2],
        [-d+2*r, -h/2-t-r*2],
        [-d, -h/2-t-r*2],
        [-d, h/2+t+r*2],
        [-d+2*r, h/2+t+r*2],
        [-d+2*r, h/2],
        [0, hp/2],
        [0, hp/2+r],
        ]
    rads = [0,r2,r2,r,r,r,r,r2,r2,0]

    chamed = []
    for i in range(1, len(corners)-1):
        x1 = corners[i-1]
        c = corners[i]
        x2 = corners[i+1]

        chamed.extend(cham(rads[i], x1, c, x2, loud=True))

    result = chamed
    result = [[x+a*sx, y+sy*b] for a,b in result[::order]]

    return result


    result = []

    hp = h-pinch

    result.extend(arc(r, (-r, -hp/2-r), 0, math.pi/2))
    result.extend(arc(r, (-d+3*r, -h/2-r), math.pi/2, math.pi/2))

    result.extend(arc(r, (-d+r, -h/2-r-t), math.pi, math.pi)[::-1])

    result.extend(arc(r, (-d+r, +h/2+r+t), 0, math.pi)[::-1])

    result.extend(arc(r, (-d+3*r, +h/2+r), math.pi, math.pi/2))
    result.extend(arc(r, (-r, +hp/2+r), math.pi*1.5, math.pi/2))

    result = [[x+a*sx, y+sy*b] for a,b in result[::order]]

    return result

class partD(Model):
    name = project + '-D'

    def render(self):

        o = Outline()

        W = 10
        H = 25
        D = 20

        r = .8
        r2 = 1.2
        h = r*10
        d = r*10
        t = r

        W = r*20
        H = r*50

        print(f'{W+2*d} x {H}')

        o.add_verts(arc(r, (r, H-r), math.pi/2, math.pi/2))

        o.add_verts(socket(0, 3*H/4, r,h,d,t, sx=-1,order=-1, pinch = .3, r2=r2))
        o.add_verts(plug(0, H/4, r, h, d, t, r2=r2))

        verts = [
            [0,         H*0.75],
            [-H*0.25,   H*0.75],
            [-H*0.25,   H*0.67],
            [0,         H*0.67],
            [0,         H*0.33],
            [-H*0.25,   H*0.43],
            [-H*0.125,   H*0.25],
            [0,         H*0.25],
            ]
        rads = [0,1,2,1,3,1,4,0]

        chamed = []
        chamed.append(verts[0])
        for i in range(1, len(verts)-1):
            x1 = verts[i-1]
            c = verts[i]
            x2 = verts[i+1]

            chamed.extend(cham(rads[i], x1, c, x2))
        chamed.append(verts[-1])

#        o.add_verts(chamed)

        x1 = (0, H*0.75)
        c = (-H*0.25, H*0.75)
        x2 = (-H*0.25, H*0.25)
#        o.add_verts([x1])
#        o.add_verts(cham(1,x1,c,x2))


        x1 = c
        c = (-H*0.25,H*0.67)
        x2 = (0, H*0.67)
#        o.add_verts(cham(1,x1,c,x2))

        x1 = c
        c = x2
        x2 = (0, H*0.33)
#        o.add_verts(cham(1,x1,c,x2))
#        o.add_verts([x2])


        x1 = c
        c = x2
        x2 = (0, H*0.25)
#        o.add_verts(cham(1,x1,c,x2))
#        o.add_verts([x2])

        o.add_verts(arc(r, (r, r), math.pi, math.pi/2))
        o.add_verts(arc(r, (W-r, r), math.pi*1.5, math.pi/2))

#        o.add_verts([
#            [0,0],
#            [s/2,0],
#            ])

        o.add_verts(socket(W, H/4, r,h,d,t, pinch = .3, r2=r2))
        o.add_verts(plug(W, 3*H/4, r,h,d,t, sx = -1, order=-1, r2=r2))

        o.add_verts(arc(r, (W-r, H-r), 0, math.pi/2))

        result = Poly(o).render()

        result = linear_extrude(D)(result)


        return result

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



