

import sys, os, time
import math
from solid import *
from solid.utils import *

import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

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

    if loud:
#        print([_*180/math.pi for _ in (a1, a2, da, al, aa, sa, ea, eao)])
        print([_*180/math.pi for _ in (aa, sa, ea, a1, a2)])

    inc = 1
    if aa < 0:
        inc = -1
        sa = ea
        aa*= -1
    result.extend(arc(r, (cx, cy), sa, aa)[::inc])

    return result


project = '000-011'

t = 1.628+0.2

r = 7
rint = 7-t/2

tbar = r

l = 20

depth = 3

margin = 7

clamp = 40

class partA(Model):
    name = project + '-A'

    def render(self):

        def pegs(N):
            w = rint*2+l*2
            h = rint*2*N+t*(N) + tbar

            bar = box([w, tbar, t*3+1])
            bar = translate([0,tbar/2,depth-1])(bar)
            result = bar

            for i in range(N):
                ypos = tbar+t+rint+i*(2*rint+t)
                pin = cylinder(r=rint, h=t*3+1)
                pin = translate([0,ypos,depth-1])(pin)
                result += pin

                sidebar = cube([l-t, rint*2, t*2+1])
                if i%2 == 0:
                    xpos = rint+t
                    nx = r
                else:
                    nx = -r
                    xpos = -rint-l
                sidebar = translate([xpos,ypos-rint,depth-1])(sidebar)
                result += sidebar

                notch = box([t+2, 2, t*4])
                notch = translate([nx, ypos, depth-1])(notch)
                result -= notch

            return result, w, h

        top, tw, th = pegs(1)
        bot, bw, bh = pegs(2)

        w_outer = tw + margin*2
        h_outer = th+bh+clamp + margin*2

        result = box([w_outer, h_outer, depth])

        top = translate([0,h_outer/2-margin-th,0])(top)
        result += top

        bot = rotate([0,0,180])(bot)
        bot = translate([0, -h_outer/2+margin+bh, 0])(bot)
        result += bot

#        w_outer = w + margin*2
#        h_outer = h + margin*2+clamp
#
#        result = box([w_outer,h_outer,depth])
#        result = translate([0,-clamp/2, 0])(result)
#
#        bounds = box([w,h,2])
#        bounds = translate([0,0,depth-1])(bounds)
##        result+=bounds
#        result = translate([0,h/2,0])(result)



        return result


class partB(Model):
    """
    stake winder form
    """
    name = project + '-B'

    @extract
    def parameters(self):

        _r_wire = 2
        r_wire = _r_wire

    @inject(parameters)
    def render(self):

        print(r_wire, _r_wire)

        t = 2
        tx = t+0.4

        r_emitter = 20.3/2
        r_drip = 7.15/2
        r_min = 6

        r1 = r_emitter
        r3 = r_drip+tx/2
        r2 = 9 #?
        r5 = r_min
        r4 = r_emitter-r5/2

        h = r5*2+tx*4

        a3 = (math.asin((r2-r4)/(r2+r4)))*180/pi

        c2 = 2*sqrt(r1*r2)
        c3 = c2 + 2*sqrt(r2*r3)

        result = cylinder(r=r1-tx/2, h=h-tx)
        result = translate([-r1,0,])(result)

        peg = cylinder(r=r2-tx/2, h=h+t-tx)
        peg = translate([-r2,c2,0])(peg)

        result += peg

        #notch
        a1 = math.asin((r2-r1)/(r2+r1))*180/pi
        cut = box([3, t+4, h+10])
        cut = translate([0,r1,-1])(cut)
        cut = rotate([0,0,a1])(cut)

        cut = translate([-r1,0,0])(cut)
        result -= cut

        #moving on
        print(a3)
        rx = r5-tx/2
        peg = cylinder(r=rx, h=r1*2+r2*2)
        peg = rotate([90,0,-a3])(peg)
        peg = translate([
                    r5-r4,
                    c2+r2+tx*2,
                    h-r5-t*2])(peg)

        result += peg

#        hook = cube([r5+tx, 2, tx*2])
#        hook = translate([-r2-tx/2,c2+r2-tx/2+tx,h/2-tx])(hook)
#        result += hook

        a = r1*2+tx+r5
#        b = c2+r1-tx/2+tx
        b = c2+r1+tx+r2+tx*2+1
        plate = cube([a,b,rx*2])
##        plate = translate([-a+r5,-r1-tx,h-t*2-rx*2-tx/2])(plate)
        plate = translate([-a+r5,-r1-tx,h-t*2-rx*2-tx/2])(plate)

        cut = cube([100,100,100])
        cut = translate([-100-tx/2,c2,0])(cut)
        plate-= cut

        result+= plate

        cut = box([100,100,100])
        cut = translate([0,0,-100+h/2])(cut)
        result -= cut

        result = translate([0,0,-h/2])(result)

        cut = cylinder(d=1.8, h=r5)
        cut = translate([0,0,-1])(cut)

        #holes
        result -= translate([-r1,0,0])(cut)
        result -= translate([-r2,c2,0])(cut)
        result -= translate([0,-r1/2,0])(cut)


        a1 = 3*pi/2 - math.asin((r2-r1)/(r2+r1))
        a2 = math.acos((r2-r1)/(r2+r1))
        a3 = pi/2 - math.asin((r2-r4)/(r2+r4))

        print(a1*180/pi)
        print(a2*180/pi)
        print(a3*180/pi)

        length = 2*(a1*r1+(a2+a3)*r2+r5*pi/2 + c2 + r2 + 100)
        print(length)
        print(length/25.4)





        return result

class partC(Model):
    """
    collar form
    """
    name = project + '-C'

    def render(self):

        L = 201.6
        H = 75

        N = 6

        r = 15

        Le = 1

        R = (L+Le-2*math.pi*r)/(2*(N+1)*math.sin(math.pi/N)) + r*math.cos(math.pi/N)

        circ = 2*(N+1)*math.sin(math.pi/N)*(R-r*math.cos(math.pi/N)) + 2*math.pi*r

        t_actual = 0.22
        t = 0.22
        t = 0

        sleeve_margin = 0.2
        H_sleeve = 25.
        t_sleeve = 5.

        #seam indent
        ridt = 1.2
        idt_off = 3


        #sleeve notch
        wn = 7
        dn = 2
        rn = 1.2


        verts = []

        for i in range(N+1):
            Reff = R+t*(i)/N
            Rl = R+t*(i-1)/N
            Rr = R+t*(i+1)/N

            a = math.pi*2*(i)/N
            al = math.pi*2*(i-1)/N
            ar = math.pi*2*(i+1)/N

            left = [Rl*math.sin(al), Rl*math.cos(al)]
            right = [Rr*math.sin(ar), Rr*math.cos(ar)]
            c = [Reff*math.sin(a), Reff*math.cos(a)]

            tverts = cham(r, left, c, right)
            if i != 0:
                verts.extend(tverts)
            else:
                p = tverts[-1]
                verts.extend([p])

            if i == 1:
                p = tverts[-1]
                p2 = [p[0], p[1]-ridt-idt_off]
                p3 = [p[0]-2*ridt, p[1]-ridt-idt_off]
                p4 = [p[0]-2*ridt, p[1]-3*ridt-idt_off]
                p5 = [p[0], p[1]-3*ridt-idt_off]
                p6 = [p[0], p[1]-4*ridt-idt_off]


                verts.extend(cham(ridt, p, p2, p3))
                verts.extend(cham(ridt, p2, p3, p4))
                verts.extend(cham(ridt, p3, p4, p5))
                verts.extend(cham(ridt, p4, p5, p6))


#                verts.extend([p, p2, p3, p4])



        o = Outline()

        o.add_verts(verts)

        result = Poly(o).render()

        result = linear_extrude(H)(result)

        #sleeve
        verts = []
        outer_verts = []

        for i in range(N):
            Reff = R+t_actual+sleeve_margin

            a = math.pi*2*(i)/N
            al = math.pi*2*(i-1)/N
            ar = math.pi*2*(i+1)/N

            left = [Reff*math.sin(al), Reff*math.cos(al)]
            right = [Reff*math.sin(ar), Reff*math.cos(ar)]
            c = [Reff*math.sin(a), Reff*math.cos(a)]

            tverts = cham(r, left, c, right)
            verts.extend(tverts)

            if i == 1:
                p = tverts[-1]
                p2 = [p[0], wn/2]
                p3 = [p[0]+dn, wn/2]
                p4 = [p[0]+dn,-wn/2]
                p5 = [p[0], -wn/2]
                p6 = [p[0], -wn/2-1]


                verts.extend(cham(ridt, p, p2, p3))
                verts.extend(cham(ridt, p2, p3, p4))
                verts.extend(cham(ridt, p3, p4, p5))
                verts.extend(cham(ridt, p4, p5, p6))




            Reff = R+t_actual+sleeve_margin+t_sleeve
            left = [Reff*math.sin(al), Reff*math.cos(al)]
            right = [Reff*math.sin(ar), Reff*math.cos(ar)]
            c = [Reff*math.sin(a), Reff*math.cos(a)]

            tverts = cham(r, left, c, right)
            outer_verts.extend(tverts)


        o = Outline()
        co = Outline()

        o.add_verts(outer_verts)
        co.add_verts(verts)

        sleeve = Poly(o, [co]).render()

        sleeve = linear_extrude(H_sleeve)(sleeve)

        return [result, sleeve]

    def write_stl(self, filename):
        if self._skip:
            print('Skipping part {}'.format(self.name))
            return
        print('Rendering part {}'.format(self.name))
        parts = self.render()

        for idx, part in enumerate(parts):
            start = time.time()
            scad_render_to_file(part, 'temp.scad')
            with open('temp.scad', 'r') as f:
                raw = f.read()
            with open('temp.scad', 'w') as f:
                f.write('$fn={};\n'.format(self.fn))
                f.write(raw)
            filename = self.name+str(idx)+'.stl'
            print('Rendering to file {}'.format(filename))
            subprocess.call(['openscad', '-o', filename, 'temp.scad'])
            end = time.time()
            print('Finished in {}s'.format(end-start))



class partD(Model):
    """
    removable wire clamp for stake winder form
    U-shape that wraps outer body of jig with arc around peg 2
    slides onto peg 2 from above
    """
    name = project + '-D'

    def render(self):

        t = 2
        tx = t + 0.4

        r_emitter = 20.3 / 2
        r_drip = 7.15 / 2
        r_min = 6

        r1 = r_emitter
        r2 = 9
        r5 = r_min
        r4 = r_emitter - r5 / 2

        rx = r5 - tx / 2  # peg 1 radius = 4.8
        c2 = 2 * sqrt(r1 * r2)

        r_wire = 2.0 / 2

#        cl = 0.3
        cl = 0
        side = 3
        top_h = 5

        a3 = math.asin((r2 - r4) / (r2 + r4))

        # peg centers
        p2x = -r2
        p2y = c2

        p1x = r5 - r4
        p1y = c2 + r2 + tx * 2

        # actual peg 2 clearance radius
        r2_actual = r2 - tx / 2
        r2_cl = r2_actual + cl

        # jig body bounds
        a_val = r1 * 2 + tx + r5
        x_left = -a_val + r5
        x_right = r5

        inner_left = x_left - cl
        inner_right = x_right + cl
        outer_left = inner_left - side
        outer_right = inner_right + side

        # top of plate in original coords
        plate_top = c2 + r2 + tx * 2 + 1

        u_top = plate_top + top_h
        u_bot = p2y - r2_cl - side
        u_bot = -r1-tx
        inner_top = plate_top

        # --- peg 1 axis in XY projection ---
        # peg 1 is rotated by rotate([90,0,-a3_deg]) in partB
        # where a3_deg = math.asin((r2-r4)/(r2+r4))*180/pi
        # OpenSCAD rotate([a,b,c]) applies Rx(a) then Ry(b) then Rz(c)
        # cylinder axis (0,0,1):
        #   after Rx(90): (0, -1, 0)
        #   after Rz(-a3_deg): (-(-1)*sin(-a3), (-1)*cos(-a3), 0) = (-sin(a3), -cos(a3), 0)
        # wait: Rz(theta) * (x,y) = (x*cos(theta)-y*sin(theta), x*sin(theta)+y*cos(theta))
        # Rz(-a3) * (0, -1) = (0*cos(-a3)-(-1)*sin(-a3), 0*sin(-a3)+(-1)*cos(-a3))
        #                    = (-sin(a3), -cos(a3))
        p1_axis_x = -math.sin(a3)
        p1_axis_y = -math.cos(a3)

        # perpendicular to peg 1 axis, pointing toward peg 2
        p1_perp_x = p1_axis_y   # = -cos(a3)
        p1_perp_y = -p1_axis_x  # = sin(a3)
        # check direction toward peg 2
        to_p2_x = p2x - p1x
        to_p2_y = p2y - p1y
        if p1_perp_x * to_p2_x + p1_perp_y * to_p2_y < 0:
            p1_perp_x = -p1_perp_x
            p1_perp_y = -p1_perp_y

        # --- wire center ---
        # intersection of:
        # line: through (p1x + (rx+r_wire)*perp_x, p1y + (rx+r_wire)*perp_y) along p1_axis
        # circle: center (p2x, p2y), radius r2_actual + r_wire
        lx = p1x + (rx + r_wire+cl) * p1_perp_x
        ly = p1y + (rx + r_wire+cl) * p1_perp_y

        r_contact = r2_actual + r_wire +cl
        dx = lx - p2x
        dy = ly - p2y

        qa = p1_axis_x**2 + p1_axis_y**2
        qb = 2 * (dx * p1_axis_x + dy * p1_axis_y)
        qc = dx**2 + dy**2 - r_contact**2

        disc = qb**2 - 4 * qa * qc
        if disc < 0:
            disc = 0

        # two solutions - pick the one between the pegs (closer to both)
        t1 = (-qb + math.sqrt(disc)) / (2 * qa)
        t2 = (-qb - math.sqrt(disc)) / (2 * qa)

        w1x = lx + t1 * p1_axis_x
        w1y = ly + t1 * p1_axis_y
        w2x = lx + t2 * p1_axis_x
        w2y = ly + t2 * p1_axis_y

        # pick solution between pegs (y between p2y and p1y)
        if abs(w1y - (p1y + p2y) / 2) < abs(w2y - (p1y + p2y) / 2):
            wire_cx, wire_cy = w1x, w1y
        else:
            wire_cx, wire_cy = w2x, w2y

        wire_cl = r_wire + cl

        print("wire center:", wire_cx, wire_cy)
        print("peg 1 center:", p1x, p1y)
        print("peg 2 center:", p2x, p2y)

        # --- wire arc ---
        # from peg 1 face side to peg 2 side
        wire_arc_sa = math.atan2(-p1_perp_y, -p1_perp_x)
        wire_arc_ea = math.atan2(p2y - wire_cy, p2x - wire_cx)
        wire_arc_span = wire_arc_ea - wire_arc_sa
        if wire_arc_span < 0:
            wire_arc_span += 2 * math.pi

        print("wire arc sa:", wire_arc_sa * 180 / math.pi, "ea:", wire_arc_ea * 180 / math.pi, "span:", wire_arc_span * 180 / math.pi)

        # --- peg 2 arc (unchanged from working version) ---
        # start at pi/2, sweep pi/2 to pi
        # will be updated later to connect to wire arc

        # --- build outline ---
        verts = []

        # outer boundary
        verts.append([outer_left, u_bot])
        verts.append([outer_left, u_top])
        verts.append([outer_right, u_top])
        verts.append([outer_right, u_bot])

        # inner right leg
        verts.append([inner_right, u_bot])

        # up right wall to inner top
        verts.append([inner_right, inner_top])

        # WIRE ARC
        wire_arc_pts = arc(wire_cl, (wire_cx, wire_cy), wire_arc_sa, wire_arc_span)


        _x, _y = wire_arc_pts[0]
        t_int = (inner_top - _y) / p1_axis_y
        int_x = _x + t_int * p1_axis_x

        # across to above peg 2
        verts.append([int_x, inner_top])



        #add wire arc
        wire_arc_pts = arc(wire_cl, (wire_cx, wire_cy), math.pi/2, math.pi/2)
        __x, __y = wire_arc_pts[0]
        t_int = (__y - _y) / p1_axis_y
        int_x = _x + t_int * p1_axis_x
        verts.append([int_x, __y])


        verts.extend(wire_arc_pts)

        # peg 2 arc: from top (pi/2), quarter circle to left (pi)
        peg2_arc_pts = arc(r2_cl, (p2x, p2y), math.pi / 2, math.pi / 2)
        verts.extend(peg2_arc_pts)

        # horizontal from arc end to left wall
        verts.append([inner_left, p2y])

        # inner left leg
        verts.append([inner_left, u_bot])

        o = Outline()
        o.add_verts(verts)
        profile = Poly(o).render()

        h = r5*2+tx*4
        clamp_h = 2*((rx*2+(h-t*2-rx*2-tx/2))-h/2) -1


        result = linear_extrude(clamp_h)(profile)

        return result


class partE(Model):
    #another clamp
    name = project + '-E'

    def render(self):

        t = 2
        tx = t + 0.4

        r_emitter = 20.3 / 2
        r_drip = 7.15 / 2
        r_min = 6

        r1 = r_emitter
        r2 = 9
        r5 = r_min
        r4 = r_emitter - r5 / 2

        rx = r5 - tx / 2  # peg 1 radius = 4.8
        c2 = 2 * sqrt(r1 * r2)

        r_wire = 2.0 / 2

        rx = r2-tx/2

        sth = 7 #side thickness
        w = 7 #width
        d = 4 #depth
        dhook = 4*r_wire + 0.8 #hook depth

        result = box([2*(rx+2*r_wire+sth), w, d+dhook])

        cut1 = cylinder(r=rx, h=100)
        cut1 = translate([0,0,d])(cut1)

        result -= cut1

        cut2 = cylinder(r=rx+2*r_wire-0.4, h=100)
        cut2 = translate([0,0,d+dhook-r_wire])(cut2)

        cut3 = cylinder(r=rx+r_wire, h=100)
        cut3 = translate([0,0,d])(cut3)

        cut2+=cut3

        wire_cut = circle(r=r_wire)
        wire_cut = translate([rx+r_wire,0,0])(wire_cut)
        wire_cut = rotate_extrude()(wire_cut)
        wire_cut = translate([0,0,d+dhook-r_wire])(wire_cut)

        cut2 += wire_cut


        _cut = cube([100,100,120])
        _cut = translate([0,-50,0])(_cut)
        cut2-=_cut


        result -= cut2

        return result


parts = filter(lambda x: Model in inspect.getmro(x[1]) and x[0] != 'Model', inspect.getmembers(sys.modules[__name__], inspect.isclass))

#base = partB()

#a,b = base.render()

#scad_render_to_file(a+b, project+'.scad')

base = partE().render()

b = partB().render()
#b = mirror([1,0,0])(b)
#b = translate([0,0,-10])(b)

#base=b
#base+=color([0,0,0])(b)

b = rotate([0,180,0])(b)
b = translate([-9,-19,15])(b)
#base+=color([128,0,0])(b)
base += b

scad_render_to_file(base, project+'.scad')

render = False
if len(sys.argv) > 1:
    if 'render' in sys.argv: render=True

if render:
    for p in parts:
        base = p[1]()
        base.write_stl(base.name+'.stl')


