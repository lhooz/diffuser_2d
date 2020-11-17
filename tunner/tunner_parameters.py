"""script for calculating diffuser geo parameters"""
import os

import numpy as np

w = 1.0
l1 = 1.0
l2 = 2.0
R = 0.2 * w
hmesh_no1 = 50
vmesh_no1 = 50
#----------------------------------------------------
D = 2 * R / 2**0.5
dh = l1 / hmesh_no1
dv = w / vmesh_no1
hmesh_no2 = np.round(l2 / dh)
hmesh_no3 = np.ceil(1.2 * D / dh)
vmesh_no2 = vmesh_no1
vmesh_no3 = vmesh_no1
#----------------------------------------------------
x1inl = 0
x1inu = 0
y1inl = -0.5 * w
y1inu = 0.5 * w
x1outl = l1
x1outu = l1 + w
y1outl = -0.5 * w
y1outu = 0.5 * w

x2inl = x1outl + R
x2inu = x2inl + w
y2inl = y1outl - R
y2inu = y2inl + w
x2outl = x2inl
x2outu = x2inu
y2outl = y2inl - l2
y2outu = y2outl

x3inl = x1outl
x3inu = x1outu
y3inl = y1outl
y3inu = y1outu
x3outl = x2inl
x3outu = x2inu
y3outl = y2inl
y3outu = y2inu

origin1x = x3inl
origin1y = y3outl
origin2x = x3inu
origin2y = y3outu
po1x = origin1x - 10 * R
po1y = origin1y - 10 * R
p1span = 20 * R
po2x = origin2x - 10 * R
po2y = origin2y - 10 * R
p2span = 20 * R
#--------------------------------------------------
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
    f.write('%s%s;\n' % (r'x1inl   ', '{0:.3g}'.format(x1inl)))
    f.write('%s%s;\n' % (r'x1inu   ', '{0:.3g}'.format(x1inu)))
    f.write('%s%s;\n' % (r'y1inl   ', '{0:.3g}'.format(y1inl)))
    f.write('%s%s;\n' % (r'y1inu   ', '{0:.3g}'.format(y1inu)))
    f.write('%s%s;\n' % (r'x1outl   ', '{0:.3g}'.format(x1outl)))
    f.write('%s%s;\n' % (r'x1outu   ', '{0:.3g}'.format(x1outu)))
    f.write('%s%s;\n' % (r'y1outl   ', '{0:.3g}'.format(y1outl)))
    f.write('%s%s;\n' % (r'y1outu   ', '{0:.3g}'.format(y1outu)))

    f.write('%s%s;\n' % (r'x2inl   ', '{0:.3g}'.format(x2inl)))
    f.write('%s%s;\n' % (r'x2inu   ', '{0:.3g}'.format(x2inu)))
    f.write('%s%s;\n' % (r'y2inl   ', '{0:.3g}'.format(y2inl)))
    f.write('%s%s;\n' % (r'y2inu   ', '{0:.3g}'.format(y2inu)))
    f.write('%s%s;\n' % (r'x2outl   ', '{0:.3g}'.format(x2outl)))
    f.write('%s%s;\n' % (r'x2outu   ', '{0:.3g}'.format(x2outu)))
    f.write('%s%s;\n' % (r'y2outl   ', '{0:.3g}'.format(y2outl)))
    f.write('%s%s;\n' % (r'y2outu   ', '{0:.3g}'.format(y2outu)))

    f.write('%s%s;\n' % (r'x3inl   ', '{0:.3g}'.format(x3inl)))
    f.write('%s%s;\n' % (r'x3inu   ', '{0:.3g}'.format(x3inu)))
    f.write('%s%s;\n' % (r'y3inl   ', '{0:.3g}'.format(y3inl)))
    f.write('%s%s;\n' % (r'y3inu   ', '{0:.3g}'.format(y3inu)))
    f.write('%s%s;\n' % (r'x3outl   ', '{0:.3g}'.format(x3outl)))
    f.write('%s%s;\n' % (r'x3outu   ', '{0:.3g}'.format(x3outu)))
    f.write('%s%s;\n' % (r'y3outl   ', '{0:.3g}'.format(y3outl)))
    f.write('%s%s;\n' % (r'y3outu   ', '{0:.3g}'.format(y3outu)))

    f.write('%s%s;\n' % (r'r   ', '{0:.3g}'.format(R)))
    f.write('%s%s;\n' % (r'o1x   ', '{0:.3g}'.format(origin1x)))
    f.write('%s%s;\n' % (r'o1y   ', '{0:.3g}'.format(origin1y)))
    f.write('%s%s;\n' % (r'o2x   ', '{0:.3g}'.format(origin2x)))
    f.write('%s%s;\n' % (r'o2y   ', '{0:.3g}'.format(origin2y)))
    f.write('%s%s;\n' % (r'po1x   ', '{0:.3g}'.format(po1x)))
    f.write('%s%s;\n' % (r'po1y   ', '{0:.3g}'.format(po1y)))
    f.write('%s%s;\n' % (r'p1span   ', '{0:.3g}'.format(p1span)))
    f.write('%s%s;\n' % (r'po2x   ', '{0:.3g}'.format(po2x)))
    f.write('%s%s;\n' % (r'po2y   ', '{0:.3g}'.format(po2y)))
    f.write('%s%s;\n' % (r'p2span   ', '{0:.3g}'.format(p2span)))

    f.write('%s%s;\n' % (r'hm1   ', '{0:.3g}'.format(hmesh_no1)))
    f.write('%s%s;\n' % (r'vm1   ', '{0:.3g}'.format(vmesh_no1)))
    f.write('%s%s;\n' % (r'hm2   ', '{0:.3g}'.format(hmesh_no2)))
    f.write('%s%s;\n' % (r'vm2   ', '{0:.3g}'.format(vmesh_no2)))
    f.write('%s%s;\n' % (r'hm3   ', '{0:.3g}'.format(hmesh_no3)))
    f.write('%s%s;\n' % (r'vm3   ', '{0:.3g}'.format(vmesh_no3)))

# with open(save_file_sh, 'w') as f:
# f.write('#!/bin/bash\n')
# f.write('cd constant\n')
# f.write('cd triSurface\n')
# f.write(
# 'surfaceTransformPoints -scale \'(%s %s 1)\' basic_vane.stl single_vanem.stl\n'
# % ('{0:.3g}'.format(w1), '{0:.3g}'.format(w1)))
# f.write(
# 'surfaceTransformPoints -rollPitchYaw \'(0 0 %s)\' single_vanem.stl single_vaneu.stl\n'
# % '{0:.3g}'.format(vane_angleu))
# f.write(
# 'surfaceTransformPoints -rollPitchYaw \'(0 0 %s)\' single_vanem.stl single_vanel.stl\n'
# % '{0:.3g}'.format(vane_anglel))
# f.write(
# 'surfaceTransformPoints -translate \'(0 %s 0)\' single_vaneu.stl single_vaneu.stl\n'
# % '{0:.3g}'.format(wu))
# f.write(
# 'surfaceTransformPoints -translate \'(0 %s 0)\' single_vanel.stl single_vanel.stl\n'
# % '{0:.3g}'.format(wl))
# f.write('cd ..\n')
# f.write('cd ..\n')
