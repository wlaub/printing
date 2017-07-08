from solid import *
from solid.utils import *
import numbers

def arc(r, off=(0,0), a1 = 0, a=2*3.14, N=32):
    a = float(a)
    angles = [ a1+a*x/N for x in range(N+1)]
    return [[r*cos(x)+off[0], r*sin(x)+off[1]] for x in angles]


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
            idx += 1:
        except:
            raise KeyError('index {} is not a number'.format(idx))

        d = self.verts

        if idx in d.keys():
            if not extend: raise KeyError('index {} already exists'.format(idx))
            d[idx].extend(verts)
        else:
            d[idx] = verts


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

    def __init__(self, outline, cutouts):
        """
        Outline is a single Outline object, cutouts is an
        array of Outline objects.
        """
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
            N = +l

        return polygon(verts, points)



