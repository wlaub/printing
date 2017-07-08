#!/usr/bin/python
import sys, os, time
from solid import *
from solid.utils import *

import subprocess


project = 'NAME'

def box(dims):
    return translate([-dims[0]/2., -dims[1]/2., 0])(cube(dims))


def main():
    base = box([1,1,1])
    return base

base = main()

scad_render_to_file(base, project+'.scad')

objects={ project+'.stl':main()
        }

def obj_to_stl(obj, filename):
    start = time.time()
    scad_render_to_file(obj, 'temp.scad')
    with open('temp.scad', 'a') as f:
        f.write('$fn=100;\n')
    subprocess.call(['openscad', '-o', filename, 'temp.scad'])
    end = time.time()
    print('Finished in {}s'.format(end-start))

render = False
if len(sys.argv) > 1:
    if 'render' in sys.argv: render=True

if render:
    for k,v in objects.iteritems():
        print('Rendering {}'.format(k))
        obj_to_stl(v, k)


