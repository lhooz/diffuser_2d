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
turnp_parameters = read_parameters(os.path.join(cwd, 'turnp_parameters'))

turnp_inx = turnp_parameters[0]
turnp_iny = turnp_parameters[1]
w = turnp_parameters[2]
R = turnp_parameters[3] * w
mesh_size = turnp_parameters[4]
#---------------------------------------------------
refl = turnp_parameters[5]
refledge = turnp_parameters[6]
reflcurvature = turnp_parameters[7]
mesh_rot = turnp_parameters[8]
mesh_yscale = turnp_parameters[9]
layer_no = turnp_parameters[10]
component_no = turnp_parameters[11]
component_type = turnp_parameters[12]
#----------------------------------------------------
wall_layer_thickness = 1e-4
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
loc_in_mesh = [0.01 * w, 0.01 * w]
#--------------------------------------------------
save_file_par = os.path.join(cwd, 'system', 'meshParameters')
save_file_sh = os.path.join(cwd, 'transform_stl.sh')
save_file_mshsh = os.path.join(cwd, 'transform_mesh.sh')
save_file_snappy_geo = os.path.join(cwd, 'system', 'snappy_geo')
save_file_snappy_feature = os.path.join(cwd, 'system', 'snappy_feature')
save_file_snappy_parameters = os.path.join(cwd, 'system', 'snappy_parameters')
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
    f.write('%s%s;\n' % (r'xin   ', '{0:.10g}'.format(xin)))
    f.write('%s%s;\n' % (r'xout   ', '{0:.10g}'.format(xout)))
    f.write('%s%s;\n' % (r'yl   ', '{0:.10g}'.format(yl)))
    f.write('%s%s;\n' % (r'yu   ', '{0:.10g}'.format(yu)))

    f.write('%s%s;\n' % (r'hm   ', '{0:.0f}'.format(hmesh_no)))
    f.write('%s%s;\n' % (r'vm   ', '{0:.0f}'.format(vmesh_no)))
    if component_type == 0:
        f.write('inName   inlet;\n')
        f.write('outName   amiOut_l%s_c%s;\n' %
                ('{0:.0f}'.format(layer_no), '{0:.0f}'.format(component_no)))
    elif component_type == 1:
        f.write('inName   amiIn_l%s_c%s;\n' %
                ('{0:.0f}'.format(layer_no), '{0:.0f}'.format(component_no)))
        f.write('outName   amiOut_l%s_c%s;\n' %
                ('{0:.0f}'.format(layer_no), '{0:.0f}'.format(component_no)))
    elif component_type == 2:
        f.write('inName   amiIn_l%s_c%s;\n' %
                ('{0:.0f}'.format(layer_no), '{0:.0f}'.format(component_no)))
        f.write('outName   outlet;\n')

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
        ('{0:.10g}'.format(w), '{0:.10g}'.format(w)))
    f.write(
        'surfaceTransformPoints -scale \'(%s %s 1)\' tunner_vane.stl vane0.stl\n'
        % ('{0:.10g}'.format(R), '{0:.10g}'.format(R)))
    #---------------
    f.write(
        'surfaceTransformPoints -rollPitchYaw \'(0 0 %s)\' vane0.stl vane0.stl\n'
        % '{0:.10g}'.format(rota))

    for i in range(len(xy_vane)):
        vname = 'vane' + str(i + 1)
        f.write(
            'surfaceTransformPoints -translate \'(%s 0 0)\' vane0.stl %s.stl\n'
            % ('{0:.10g}'.format(xy_vane[i][0]), vname))
        f.write(
            'surfaceTransformPoints -translate \'(0 %s 0)\' %s.stl %s.stl\n' %
            ('{0:.10g}'.format(xy_vane[i][1]), vname, vname))
    f.write('cd ..\n')
    f.write('cd ..\n')

with open(save_file_mshsh, 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions\n')
    f.write('runParallel transformPoints -rollPitchYaw \'(0 0 %s)\'\n' %
            '{0:.10g}'.format(mesh_rot))
    f.write('rm log.transformPoints\n')
    f.write('runParallel transformPoints -scale \'(1 %s 1)\'\n' %
            '{0:.10g}'.format(mesh_yscale))
    f.write('rm log.transformPoints\n')
    f.write('runParallel transformPoints -translate \'(%s %s 0)\'\n' %
            ('{0:.10g}'.format(turnp_inx), '{0:.10g}'.format(turnp_iny)))

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
    f.write('    name    walls;\n')
    f.write('}\n')
    for i in range(len(xy_vane)):
        vname = 'vane' + str(i + 1)
        f.write('\"%s.stl\"\n' % vname)
        f.write('{\n')
        f.write('    type    triSurfaceMesh;\n')
        f.write('    name    walls;\n')
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
    f.write('level %s;\n' % '{0:.0f}'.format(refledge))
    f.write('}\n')
    for i in range(len(xy_vane)):
        vname = 'vane' + str(i + 1)
        f.write('{\n')
        f.write('file "%s.eMesh";\n' % vname)
        f.write('level %s;\n' % '{0:.0f}'.format(refledge))
        f.write('}\n')

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
