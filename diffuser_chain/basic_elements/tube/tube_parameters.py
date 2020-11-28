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
tube_parameters = read_parameters(os.path.join(cwd, 'tb_parameters'))

tube_inx = tube_parameters[0]
tube_iny = tube_parameters[1]
w = tube_parameters[2]
l = tube_parameters[3]
mesh_size = tube_parameters[4]
#---------------------------------------------------
refl = tube_parameters[5]
refledge = tube_parameters[6]
reflcurvature = tube_parameters[7]
mesh_rot = tube_parameters[8]
#----------------------------------------------------
wall_layer_thickness = 1e-4
#---------------------------------------------------
xin = 0
xout = l
yl = -0.7 * w
yu = 0.7 * w
hmesh_no = np.ceil((xout - xin) / mesh_size)
vmesh_no = np.ceil((yu - yl) / mesh_size)
loc_in_mesh = [0.01 * w, 0.01 * w]
#--------------------------------------------------
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
    f.write('%s%s;\n' % (r'yl   ', '{0:.10g}'.format(yl)))
    f.write('%s%s;\n' % (r'yu   ', '{0:.10g}'.format(yu)))

    f.write('%s%s;\n' % (r'hm   ', '{0:.0f}'.format(hmesh_no)))
    f.write('%s%s;\n' % (r'vm   ', '{0:.0f}'.format(vmesh_no)))

with open(save_file_sh, 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('cd constant\n')
    f.write('cd triSurface\n')
    f.write(
        'surfaceTransformPoints -scale \'(%s %s 1)\' tube_wall.stl tbwall.stl\n'
        % ('{0:.10g}'.format(l), '{0:.10g}'.format(w)))
    #---------------
    f.write('cd ..\n')
    f.write('cd ..\n')

with open(save_file_mshsh, 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions\n')
    f.write('runParallel transformPoints -rollPitchYaw \'(0 0 %s)\'\n' %
            '{0:.10g}'.format(mesh_rot))
    f.write('rm log.transformPoints\n')
    f.write('runParallel transformPoints -translate \'(%s %s 0)\'\n' %
            ('{0:.10g}'.format(tube_inx), '{0:.10g}'.format(tube_iny)))

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
