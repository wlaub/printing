#!/usr/bin/python
import sys, os, time
from solid import *
from solid.utils import *

import subprocess, inspect
sys.path.append('../')
from model import *
from model.poly import *

project = 'NAME'

class partA(Model):
    name = project + '-A'

    def render(self):
        result = box([1,1,1])
        return result


parts = filter(lambda x: Model in inspect.getmro(x[1]) and x[0] != 'Model', inspect.getmembers(sys.modules[__name__], inspect.isclass))

base = partA()

scad_render_to_file(base.render(), project+'.scad')

render = False
if len(sys.argv) > 1:
    if 'render' in sys.argv: render=True

if render:
    for p in parts:
        base = p[1]()
        base.write_stl(base.name+'.stl')


