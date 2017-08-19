from solid import *
from solid.utils import *
import time, sys, os
import subprocess

def box(dims):
    return translate([-dims[0]/2., -dims[1]/2., 0])(cube(dims))

class Model():
    """
    Model class for rendering automation etc
    """

    fn = 100
    name = 'MODEL'
    _skip = False

    def __init__(self):
        pass


    def render(self):
        """
        Returns the completed
        """
        return box([1,1,1])


    def write_stl(self, filename):
        if self._skip:
            print('Skipping part {}'.format(self.name))
            return
        print('Rendering part {}'.format(self.name))
        start = time.time()
        scad_render_to_file(self.render(), 'temp.scad')
        with open('temp.scad', 'a') as f:
            f.write('$fn={};\n'.format(self.fn))
        filename = self.name+'.stl'
        print('Rendering to file {}'.format(filename))
        subprocess.call(['openscad', '-o', filename, 'temp.scad'])
        end = time.time()
        print('Finished in {}s'.format(end-start))
        

