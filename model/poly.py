from solid import *
from solid.utils import *
import numbers

def arc(r, off=(0,0), a1 = 0, a=2*3.14, N=32):
    a = float(a)
    angles = [ a1+a*x/N for x in range(N+1)]
    return [[r*cos(x)+off[0], r*sin(x)+off[1]] for x in angles]

def bumped_circle(N, r1, r2, rx=0, inv=False):
    """
    Returns vertices for a circle of radius r1 with N equally spaced
    semi-circular bumps of radius r2 centered at radius r1+rx. If Inv
    is true, instead makes them detents.
    """
    result = []
    a = 2*math.asin(r2/r1)
    
    inc = 2*3.14/N
    for i in range(N):
        result.extend(arc(r1, (0,0), a/2+i*inc, inc-a) )
        ax = (i+1)*inc
        off = ((r1+rx)*math.cos(ax), (r1+rx)*math.sin(ax))
        if not inv:
            result.extend(arc(r2, off, 1.5*3.14+ax, 3.14))
        else:
            result.extend(arc(r2, off, .5*3.14+ax, 3.14)[::-1])

    return result


class Outline():
    """
    Lower level polygon editor class. Tracks arrays of
    vertices and renders them into a single array and
    and length to be combined by Poly class into a valid
    polygon
    """

    def __init__(self):
        self.verts = {}

    def add_verts(self, verts, idx = None, extend = False):
        """
        Add the given array of verts at the given index. If
        the idx already exists, raise a KeyError unless
        extend is True. otherwise extends the verts at the
        given index. idx must be a number of none. if none,
        uses the largest index + 1 or 0 if there are no idx
        """
        if idx == None:
            if len(self.verts.keys()) == 0:
                idx = 0
            else:
                idx = max(self.verts.keys()) + 1

        try:
            idx + 1
        except:
            raise KeyError('index {} is not a number'.format(idx))

        d = self.verts

        if idx in d.keys():
            if not extend: raise KeyError('index {} already exists'.format(idx))
            d[idx].extend(verts)
        else:
            d[idx] = verts

        return idx


    def render(self):
        """
        Return a polygon object
        """
        idx = sorted(self.verts.keys())
        outline = []
        points = []
        N = 0
        for i in idx:
            outline.extend(self.verts[i])
        N = len(outline)
        points.append(range(N))

        return outline, N
            

class Poly():
    """
    Class for combining multiple outlines into a polygon
    """

    def __init__(self, outline, cutouts = None):
        """
        Outline is a single Outline object, cutouts is an
        array of Outline objects.
        """
        if cutouts == None: cutouts = []
        self.outline = outline
        self.cutouts = cutouts

    def render(self):
        """
        Returns the polygon represented by Poly's outline
        and cutouts
        """
        verts = []
        points = []
        o, N = self.outline.render()
        verts.extend(o)
        points.append(range(N))

        for c in self.cutouts:
            o, l = c.render()
            verts.extend(o)
            points.append(range(N,N+l))
            N += l

        return polygon(verts, points)


class Tube():
    """
    Class for handling tubes with circular cross sections, creating
    polygons, and running simulations using wiat
    """
    name = "Tube"

    def __init__(self):
        """
        Points is a list of the form [[r1, h1], ...]
        """
        self.points = []

    def add(self, r, h):
        """
        Add a single layer.
        """
        self.points.append([r,h])

    def add_points(self, points):
        self.points.extend(points)

    def from_verts(self, verts):
        """
        Generate native points format from vert array of the form
        [[x1, y1], [x2, y2], ...] ->
        [[x1, y2-y1], [x2, y3-y2], ...]
        Requires that the y points be monotonic
        """
        result = []
        for i, ((xb, yb), (xt, yt)) in enumerate(zip(verts, verts[1:])):
            assert(yt>yb)
            result.append([xb, yt-yb])
        return result

    def verts(self):
        """
        Returns the polygon vertices for self
        """
        verts = [[0,0]]
        hcum = 0
        for r,h in self.points:
            verts.append([r, hcum])
            hcum += h
        verts.append([0, verts[-1][1]])
        return verts

    def render(self):
        """
        Returns an object of self
        """
        o = Outline()
        o.add_verts(self.verts())
        result = Poly(o).render()
        result = rotate_extrude()(result)
        return result

    def instrument(self):
        """
        Generate and return a wiat instrument
        """
        import wiat
        from wiat.TM import Cone, Cylinder, Instrument
        from wiat.TM import FlangedOpenEnd, UnflangedOpenEnd
        cones = []
        verts = []

        hcum = 0
        for r,h in self.points:
            verts.append([hcum, r])
            hcum += h
 
        """
        for (rb,hb),(rt,ht) in zip(self.points, self.points[1:]):
            print([rb/1000, rt/1000, hb/1000])
            if rb != rt:
                cones.append(Cone(rb/1000, rt/1000, hb/1000))
            else:
                cones.append(Cylinder(rb/1000, hb/1000))
        """
        end = UnflangedOpenEnd(self.points[-1][0]/1000)

        cones = wiat.TM.CreateCylindersAndConesFromList(verts)

        return Instrument(self.name, cones, end)


    def plot(self, fmin = 20., fmax = 2000., df = 1.):
        """
        Plot impedance over the specified range of frequencies.
        Also returns frequencies and impedance as f, Z
        """
        import numpy
        from matplotlib import pyplot as plt
        from wiat.TM import CalculateImpedance       
 
        f = numpy.arange(fmin, fmax, df)
        T = 20.
        I = self.instrument()
        Z = CalculateImpedance(I, f, T)
        plt.plot(f, numpy.abs(Z))
        plt.show()
        return f, Z


