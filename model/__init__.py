from solid import *
from solid.utils import *
import time, sys, os
import subprocess
import inspect
import re

def _fill(dname):
    def fill_real(function):
        filler = """ref=dict(self.__class__.__dict__)
ref.update(self.__dict__)
for k in ref.keys():
    exec("{0}=ref['{0}']".format(k))"""
#        filler = filler.replace('DNAME', dname)
        filler = filler.split('\n')
        raw = inspect.getsource(function)
#        print(raw)
        lines = raw.split('\n')
        key = '#~FILL~'
        if key not in lines:
            left = [lines[1]]
            right = lines[2:]
        else:
            idx = lines.index(key)
            left = lines[1:idx]
            right = lines[idx+1:]

        name = re.findall(r'^.*def (.*?)\(', left[0], re.M)[0]
#        print(name)

        ws = re.findall(r'^(\s*)', left[0], re.M)[0]
        ws = len(ws)
        cut = lambda x: x[ws:]
        left = map(cut, left)
        right = map(cut, right)

        ws = re.findall(r'^(\s*)', right[0], re.M)[0]
        filler = map(lambda x: '{}{}'.format(ws, x), filler)
        result = left
        result.extend(filler)
        result.extend(right)
        result = '\n'.join(result)
#        print(result)
        function = compile(result, '<string>', 'exec')
        eval(function)
        f = locals()[name]
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
    return fill_real



def box(dims):
    return translate([-dims[0]/2., -dims[1]/2., 0])(cube(dims))

class Model():
    """
    Model class for rendering automation etc
    """

    fn = 100
    name = 'MODEL'
    do_sub = True
    _skip = False

    def __init__(self):
        pass

    def sub(self, a, b, over = None):
        do_sub = self.do_sub
        if over != None:
            do_sub = over
        if do_sub:
            return a-b
        else:
            return a+b

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
        with open('temp.scad', 'r') as f:
            raw = f.read()
        with open('temp.scad', 'w') as f:
            f.write('$fn={};\n'.format(self.fn))
            f.write(raw)
        filename = self.name+'.stl'
        print('Rendering to file {}'.format(filename))
        subprocess.call(['openscad', '-o', filename, 'temp.scad'])
        end = time.time()
        print('Finished in {}s'.format(end-start))
        

