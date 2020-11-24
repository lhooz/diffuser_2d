"""script for calculating diffuser geo parameters"""
import os

import numpy as np

w1 = 0.11
theta = 25
l_w1 = 2
hmesh_no = 100
vmesh_no = 100

#----------------------------------------------------
xin = 0
yinu = 0.5 * w1
yinl = -yinu
xout = l_w1 * w1
youtu = 0.5 * w1 + np.sin(theta * np.pi / 180) * xout
youtl = -youtu

vane_angleu = theta / 1.45
vane_anglel = -theta / 1.45
wu = 0.3 * w1
wl = -0.3 * w1

cwd = os.getcwd()
save_file_par = os.path.join(cwd, 'system', 'meshParameters')
save_file_sh = os.path.join(cwd, 'transform_stl.sh')
with open(save_file_par, 'w') as f:
    f.write(
        '%s\n' %
        '/*--------------------------------*- C++ -*----------------------------------*\\'
    )
    f.write(
        '%s\n' %
        r'\*---------------------------------------------------------------------------*/'
    )
    f.write('%s%s;\n' % (r'xin   ', '{0:.3g}'.format(xin)))
    f.write('%s%s;\n' % (r'yinl   ', '{0:.3g}'.format(yinl)))
    f.write('%s%s;\n' % (r'yinu   ', '{0:.3g}'.format(yinu)))
    f.write('%s%s;\n' % (r'xout   ', '{0:.3g}'.format(xout)))
    f.write('%s%s;\n' % (r'youtl   ', '{0:.3g}'.format(youtl)))
    f.write('%s%s;\n' % (r'youtu   ', '{0:.3g}'.format(youtu)))
    f.write('%s%s;\n' % (r'hm   ', '{0:.3g}'.format(hmesh_no)))
    f.write('%s%s;\n' % (r'vm   ', '{0:.3g}'.format(vmesh_no)))

with open(save_file_sh, 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('cd constant\n')
    f.write('cd triSurface\n')
    f.write(
        'surfaceTransformPoints -scale \'(%s %s 1)\' basic_vane.stl single_vanem.stl\n'
        % ('{0:.3g}'.format(w1), '{0:.3g}'.format(w1)))
    f.write(
        'surfaceTransformPoints -rollPitchYaw \'(0 0 %s)\' single_vanem.stl single_vaneu.stl\n'
        % '{0:.3g}'.format(vane_angleu))
    f.write(
        'surfaceTransformPoints -rollPitchYaw \'(0 0 %s)\' single_vanem.stl single_vanel.stl\n'
        % '{0:.3g}'.format(vane_anglel))
    f.write(
        'surfaceTransformPoints -translate \'(0 %s 0)\' single_vaneu.stl single_vaneu.stl\n'
        % '{0:.3g}'.format(wu))
    f.write(
        'surfaceTransformPoints -translate \'(0 %s 0)\' single_vanel.stl single_vanel.stl\n'
        % '{0:.3g}'.format(wl))
    #------------------
    # f.write(
        # 'surfaceTransformPoints -translate \'(%s 0 0)\' single_vaneu.stl single_vaneu.stl\n'
        # % '{0:.3g}'.format(wl))
    # f.write(
        # 'surfaceTransformPoints -translate \'(%s 0 0)\' single_vanel.stl single_vanel.stl\n'
        # % '{0:.3g}'.format(wl))
    # f.write(
        # 'surfaceTransformPoints -translate \'(%s 0 0)\' single_vanem.stl single_vanem.stl\n'
        # % '{0:.3g}'.format(wl))
    #------------------
    f.write('cd ..\n')
    f.write('cd ..\n')
