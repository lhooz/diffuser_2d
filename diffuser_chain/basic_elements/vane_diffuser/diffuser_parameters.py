"""script for calculating diffuser geo parameters"""
import csv
import os

import numpy as np


def read_parameters(parameters):
    """read design parameters"""
    par_array = []
    with open(parameters) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0

        for row in csv_reader:
            par_array.append(float(row[0]))
            line_count += 1

        print(f'Processed {line_count} lines in {parameters}')

    par_array = np.array(par_array)
    return par_array


#---------------------------------------------------
cwd = os.getcwd()
df_parameters = read_parameters(os.path.join(cwd, 'df_parameters'))

df_inx = df_parameters[0]
df_iny = df_parameters[1]
w1 = df_parameters[2]
theta = df_parameters[3]
l_w1 = df_parameters[4]
mesh_size = df_parameters[5]
#---------------------------------------------------
refl = df_parameters[6]
refledge = df_parameters[7]
reflcurvature = df_parameters[8]
mesh_rot = df_parameters[9]
#--------------------------------------------------
wall_layer_thickness = 1e-4
#---------------------------------------------------
xin = 0
xout = l_w1 * w1
yu = 1.2 * (0.5 * w1 + np.sin(theta * np.pi / 180) * (xout - xin))
yl = -yu
#-----------------
hmesh_no = np.ceil((xout - xin) / mesh_size)
vmesh_no = np.ceil((yu - yl) / mesh_size)
loc_in_mesh = [0.01 * w1, 0.01 * w1]
#-------------------------------------------------
wall_angleu = theta
wall_anglel = -theta
vane_angleu = theta / 1.45
vane_anglel = -theta / 1.45
wu = 0.3 * w1
wl = -0.3 * w1
dwallu = (0.5 + 0.1 / 2) * w1
dwalll = -(0.5 + 0.1 / 2) * w1

save_file_par = os.path.join(cwd, 'system', 'meshParameters')
save_file_sh = os.path.join(cwd, 'transform_stl.sh')
save_file_mshsh = os.path.join(cwd, 'transform_mesh.sh')
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
    f.write('%s%s;\n' % (r'xin   ', '{0:.10g}'.format(xin)))
    f.write('%s%s;\n' % (r'xout   ', '{0:.10g}'.format(xout)))
    f.write('%s%s;\n' % (r'yu   ', '{0:.10g}'.format(yu)))
    f.write('%s%s;\n' % (r'yl   ', '{0:.10g}'.format(yl)))
    f.write('%s%s;\n' % (r'hm   ', '{0:.0f}'.format(hmesh_no)))
    f.write('%s%s;\n' % (r'vm   ', '{0:.0f}'.format(vmesh_no)))

with open(save_file_sh, 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('cd constant\n')
    f.write('cd triSurface\n')
    f.write(
        'surfaceTransformPoints -scale \'(%s %s 1)\' basic_vane.stl single_vanem.stl\n'
        % ('{0:.10g}'.format(w1), '{0:.10g}'.format(w1)))
    f.write(
        'surfaceTransformPoints -scale \'(%s %s 1)\' diffuser_wall.stl dwall.stl\n'
        % ('{0:.10g}'.format(w1), '{0:.10g}'.format(w1)))
    #--------------
    f.write(
        'surfaceTransformPoints -rollPitchYaw \'(0 0 %s)\' single_vanem.stl single_vaneu.stl\n'
        % '{0:.10g}'.format(vane_angleu))
    f.write(
        'surfaceTransformPoints -rollPitchYaw \'(0 0 %s)\' single_vanem.stl single_vanel.stl\n'
        % '{0:.10g}'.format(vane_anglel))
    f.write(
        'surfaceTransformPoints -rollPitchYaw \'(0 0 %s)\' dwall.stl dwallu.stl\n'
        % '{0:.10g}'.format(wall_angleu))
    f.write(
        'surfaceTransformPoints -rollPitchYaw \'(0 0 %s)\' dwall.stl dwalll.stl\n'
        % '{0:.10g}'.format(wall_anglel))
    #--------------
    f.write(
        'surfaceTransformPoints -translate \'(0 %s 0)\' single_vaneu.stl single_vaneu.stl\n'
        % '{0:.10g}'.format(wu))
    f.write(
        'surfaceTransformPoints -translate \'(0 %s 0)\' single_vanel.stl single_vanel.stl\n'
        % '{0:.10g}'.format(wl))
    f.write(
        'surfaceTransformPoints -translate \'(0 %s 0)\' dwallu.stl dwallu.stl\n'
        % '{0:.10g}'.format(dwallu))
    f.write(
        'surfaceTransformPoints -translate \'(0 %s 0)\' dwalll.stl dwalll.stl\n'
        % '{0:.10g}'.format(dwalll))
    #------------------
    # f.write(
    # 'surfaceTransformPoints -translate \'(%s 0 0)\' single_vaneu.stl single_vaneu.stl\n'
    # % '{0:.10g}'.format(wl))
    # f.write(
    # 'surfaceTransformPoints -translate \'(%s 0 0)\' single_vanel.stl single_vanel.stl\n'
    # % '{0:.10g}'.format(wl))
    # f.write(
    # 'surfaceTransformPoints -translate \'(%s 0 0)\' single_vanem.stl single_vanem.stl\n'
    # % '{0:.10g}'.format(wl))
    #------------------
    f.write('cd ..\n')
    f.write('cd ..\n')

with open(save_file_mshsh, 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions\n')
    f.write('runParallel transformPoints -rollPitchYaw \'(0 0 %s)\'\n' %
            '{0:.10g}'.format(mesh_rot))
    f.write('rm log.transformPoints\n')
    f.write('runParallel transformPoints -translate \'(%s %s 0)\'\n' %
            ('{0:.10g}'.format(df_inx), '{0:.10g}'.format(df_iny)))

with open(save_file_snappy_parameters, 'w') as f:
    f.write(
        '%s\n' %
        '/*--------------------------------*- C++ -*----------------------------------*\\'
    )
    f.write(
        '%s\n' %
        r'\*---------------------------------------------------------------------------*/'
    )
    f.write('%s%s;\n' % (r'refledge   ', '{0:.0f}'.format(refledge)))
    f.write('%s%s;\n' % (r'refl   ', '{0:.0f}'.format(refl)))
    f.write('%s%s;\n' % (r'reflcurvature   ', '{0:.0f}'.format(reflcurvature)))
    f.write('%s%s;\n' % (r'locInMeshx   ', '{0:.10g}'.format(loc_in_mesh[0])))
    f.write('%s%s;\n' % (r'locInMeshy   ', '{0:.10g}'.format(loc_in_mesh[1])))
    f.write('%s%s;\n' %
            (r'blthickness   ', '{0:.10g}'.format(wall_layer_thickness)))
