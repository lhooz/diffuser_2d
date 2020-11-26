"""script for calculating diffuser geo parameters"""
import os

import numpy as np

w = 0.1
l = 0.5
mesh_size = w / 50
#---------------------------------------------------
refledge = 2
refl = 2
reflcurvature = 2
#----------------------------------------------------
wall_layer_thickness = 1e-4
#---------------------------------------------------
xin = 0
xout = l
yl = -0.7 * w
yu = 0.7 * w
hmesh_no = np.ceil((xout - xin) / mesh_size)
vmesh_no = np.ceil((yu - yl) / mesh_size)
#--------------------------------------------------
cwd = os.getcwd()
save_file_par = os.path.join(cwd, 'system', 'meshParameters')
save_file_sh = os.path.join(cwd, 'transform_stl.sh')
save_file_snappy_parameters = os.path.join(cwd, 'system', 'snappy_parameters')
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
    f.write('%s%s;\n' % (r'xout   ', '{0:.3g}'.format(xout)))
    f.write('%s%s;\n' % (r'yl   ', '{0:.3g}'.format(yl)))
    f.write('%s%s;\n' % (r'yu   ', '{0:.3g}'.format(yu)))

    f.write('%s%s;\n' % (r'hm   ', '{0:.3g}'.format(hmesh_no)))
    f.write('%s%s;\n' % (r'vm   ', '{0:.3g}'.format(vmesh_no)))

with open(save_file_sh, 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('cd constant\n')
    f.write('cd triSurface\n')
    f.write(
        'surfaceTransformPoints -scale \'(%s %s 1)\' tube_wall.stl tbwall.stl\n'
        % ('{0:.3g}'.format(l), '{0:.3g}'.format(w)))
    #---------------
    f.write('cd ..\n')
    f.write('cd ..\n')

with open(save_file_snappy_parameters, 'w') as f:
    f.write(
        '%s\n' %
        '/*--------------------------------*- C++ -*----------------------------------*\\'
    )
    f.write(
        '%s\n' %
        r'\*---------------------------------------------------------------------------*/'
    )
    f.write('%s%s;\n' % (r'refledge   ', '{0:.3g}'.format(refledge)))
    f.write('%s%s;\n' % (r'refl   ', '{0:.3g}'.format(refl)))
    f.write('%s%s;\n' % (r'reflcurvature   ', '{0:.3g}'.format(reflcurvature)))
    f.write('%s%s;\n' %
            (r'blthickness   ', '{0:.3g}'.format(wall_layer_thickness)))
