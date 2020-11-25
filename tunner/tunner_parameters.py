"""script for calculating diffuser geo parameters"""
import os

import numpy as np

w = 0.1
R = 0.15 * w
mesh_size = w / 120
#---------------------------------------------------
refledge = '2'
refl = '2'
reflcurvature = '2'
#----------------------------------------------------
D = 2 * R / 2**0.5
#---------------------------------------------------
N_vanes = int(np.ceil(1.414 * w / (D / 2))) - 3
# N_vanes = 3
#----------------------------------------------------
xin = 0
xout = 1.5 * w
yl = -0.7 * w
yu = 0.8 * w
hmesh_no = np.ceil((xout - xin) / mesh_size)
vmesh_no = np.ceil((yu - yl) / mesh_size)
#--------------------------------------------------
cwd = os.getcwd()
save_file_par = os.path.join(cwd, 'system', 'meshParameters')
save_file_sh = os.path.join(cwd, 'transform_stl.sh')
save_file_snappy_geo = os.path.join(cwd, 'system', 'snappy_geo')
save_file_snappy_feature = os.path.join(cwd, 'system', 'snappy_feature')
save_file_snappy_refSurf = os.path.join(cwd, 'system', 'snappy_refSurf')
save_file_sufExtract = os.path.join(cwd, 'system', 'surfExtract')
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

rota = -49
dh = w / (N_vanes - 1)
xy_vane = []
x0 = xin + 0.1 * w + (1 - 1 / 1.414) * (0.2 * w - R)
y0 = yl + 0.1 * w + (1 - 1 / 1.414) * (0.2 * w - R)
for i in range(1, N_vanes - 1):
    xy_vane.append([x0 + i * dh, y0 + i * dh])

with open(save_file_sh, 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('cd constant\n')
    f.write('cd triSurface\n')
    f.write(
        'surfaceTransformPoints -translate \'(0 -0.5 0)\' tunner_wall.stl twall.stl\n'
    )
    f.write(
        'surfaceTransformPoints -scale \'(%s %s 1)\' twall.stl twall.stl\n' %
        ('{0:.3g}'.format(w), '{0:.3g}'.format(w)))
    f.write(
        'surfaceTransformPoints -scale \'(%s %s 1)\' tunner_vane.stl vane0.stl\n'
        % ('{0:.3g}'.format(R), '{0:.3g}'.format(R)))
    #---------------
    f.write(
        'surfaceTransformPoints -rollPitchYaw \'(0 0 %s)\' vane0.stl vane0.stl\n'
        % '{0:.3g}'.format(rota))

    for i in range(len(xy_vane)):
        vname = 'vane' + str(i + 1)
        f.write(
            'surfaceTransformPoints -translate \'(%s 0 0)\' vane0.stl %s.stl\n'
            % ('{0:.3g}'.format(xy_vane[i][0]), vname))
        f.write(
            'surfaceTransformPoints -translate \'(0 %s 0)\' %s.stl %s.stl\n' %
            ('{0:.3g}'.format(xy_vane[i][1]), vname, vname))
    f.write('cd ..\n')
    f.write('cd ..\n')

with open(save_file_snappy_geo, 'w') as f:
    f.write(
        '%s\n' %
        '/*--------------------------------*- C++ -*----------------------------------*\\'
    )
    f.write(
        '%s\n' %
        r'\*---------------------------------------------------------------------------*/'
    )
    f.write('\"twall.stl\"\n')
    f.write('{\n')
    f.write('    type    triSurfaceMesh;\n')
    f.write('    name    twalls;\n')
    f.write('}\n')
    for i in range(len(xy_vane)):
        vname = 'vane' + str(i + 1)
        f.write('\"%s.stl\"\n' % vname)
        f.write('{\n')
        f.write('    type    triSurfaceMesh;\n')
        f.write('    name    twalls;\n')
        f.write('}\n')

with open(save_file_snappy_feature, 'w') as f:
    f.write(
        '%s\n' %
        '/*--------------------------------*- C++ -*----------------------------------*\\'
    )
    f.write(
        '%s\n' %
        r'\*---------------------------------------------------------------------------*/'
    )
    f.write('{\n')
    f.write('file "twall.eMesh";\n')
    f.write('level %s;\n' % refledge)
    f.write('}\n')
    for i in range(len(xy_vane)):
        vname = 'vane' + str(i + 1)
        f.write('{\n')
        f.write('file "%s.eMesh";\n' % vname)
        f.write('level %s;\n' % refledge)
        f.write('}\n')

with open(save_file_snappy_refSurf, 'w') as f:
    f.write(
        '%s\n' %
        '/*--------------------------------*- C++ -*----------------------------------*\\'
    )
    f.write(
        '%s\n' %
        r'\*---------------------------------------------------------------------------*/'
    )
    f.write('twalls\n')
    f.write('{\n')
    f.write('    level (%s %s);\n' % (refl, reflcurvature))
    f.write('}\n')

with open(save_file_sufExtract, 'w') as f:
    f.write(
        '%s\n' %
        '/*--------------------------------*- C++ -*----------------------------------*\\'
    )
    f.write(
        '%s\n' %
        r'\*---------------------------------------------------------------------------*/'
    )
    f.write('twall.stl\n')
    f.write('{\n')
    f.write('    extractionMethod    extractFromSurface;\n')
    f.write('    includedAngle       170;\n')
    f.write('}\n')
    for i in range(len(xy_vane)):
        vname = 'vane' + str(i + 1)
        f.write('%s.stl\n' % vname)
        f.write('{\n')
        f.write('    extractionMethod    extractFromSurface;\n')
        f.write('    includedAngle       170;\n')
        f.write('}\n')
