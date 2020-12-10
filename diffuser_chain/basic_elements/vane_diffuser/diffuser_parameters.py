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


def cal_diffuser(w, theta, l_w, vane_angles):
    """function for calculation diffuser geometry"""
    l = l_w * w
    totalw_out = 2 * (0.5 * w + np.tan(theta * np.pi / 180) * l)
    #------update vane_angles for equal spacing at inlet-----
    singlew_out = totalw_out / (len(vane_angles) + 1)
    singlew_in = w / (len(vane_angles) + 1)

    line_co = []
    ycoin = -0.5 * w
    ycoout = -0.5 * totalw_out
    for i in range(len(vane_angles)):
        ycoin += singlew_in
        ycoout += singlew_out
        line_co.append([ycoin, ycoout])

    vane_angles = []
    for line in line_co:
        anglei = np.arctan((line[1] - line[0]) / l) * 180 / np.pi
        vane_angles.append(anglei)
    #--------------------------------------------------------

    total_gap = 0
    gaps = []
    vus = []
    for vane in vane_angles:
        vt = 0.015 * w
        gap = 2 * vt / np.cos(vane * np.pi / 180)
        gaps.append(gap)
        total_gap += gap

        vm = np.tan(vane * np.pi / 180) * l
        vu = vm + gap / 2
        vus.append(vu)

    wo = (totalw_out - total_gap) / (len(vane_angles) + 1)
    v_shift = []
    desired_vu = -totalw_out / 2
    for vi in range(len(vus)):
        desired_vu += wo + gaps[vi]
        shift = desired_vu - vus[vi]
        v_shift.append(shift)

    return v_shift, vane_angles


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
No_vanes = int(df_parameters[10])
component_type = df_parameters[11]
#--------------------------------------------------
wall_layer_thickness = 1e-4
#---------------------------------------------------
xin = 0
xout = l_w1 * w1
yu = 1.2 * (0.5 * w1 + np.tan(theta * np.pi / 180) * (xout - xin))
yl = -yu
#-----------------
hmesh_no = np.ceil((xout - xin) / mesh_size)
vmesh_no = np.ceil((yu - yl) / mesh_size)
loc_in_mesh = [0.01 * w1, 0.01 * w1]
#-------------------------------------------------
wall_angleu = theta
wall_anglel = -theta
wallthicku = 0.1 / 2 * w1
wallthickl = -0.1 / 2 * w1
dwallu = 0.5 * w1
dwalll = -0.5 * w1
#------------------------------------------------
vane_angles = np.linspace(-theta, theta, No_vanes)
if No_vanes >= 3:
    vane_angles = vane_angles[1:-1]
else:
    vane_angles = [0.0]

v_shift, vane_angles = cal_diffuser(w1, theta, l_w1, vane_angles)

save_file_par = os.path.join(cwd, 'system', 'meshParameters')
save_file_sh = os.path.join(cwd, 'transform_stl.sh')
save_file_mshsh = os.path.join(cwd, 'transform_mesh.sh')
save_file_snappy_parameters = os.path.join(cwd, 'system', 'snappy_parameters')
save_file_snappy_geo = os.path.join(cwd, 'system', 'snappy_geo')
save_file_snappy_feature = os.path.join(cwd, 'system', 'snappy_feature')
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
    f.write('%s%s;\n' % (r'yu   ', '{0:.10g}'.format(yu)))
    f.write('%s%s;\n' % (r'yl   ', '{0:.10g}'.format(yl)))
    f.write('%s%s;\n' % (r'hm   ', '{0:.0f}'.format(hmesh_no)))
    f.write('%s%s;\n' % (r'vm   ', '{0:.0f}'.format(vmesh_no)))
    if component_type == 0:
        f.write('inName   inlet;\n')
        f.write('outName   amiOut;\n')
    elif component_type == 1:
        f.write('inName   amiIn;\n')
        f.write('outName   amiOut;\n')
    elif component_type == 2:
        f.write('inName   amiIn;\n')
        f.write('outName   outlet;\n')

with open(save_file_sh, 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('cd constant\n')
    f.write('cd triSurface\n')
    f.write(
        'surfaceTransformPoints -scale \'(%s %s 1)\' diffuser_wall.stl dwall.stl\n'
        % ('{0:.10g}'.format(w1), '{0:.10g}'.format(w1)))
    f.write(
        'surfaceTransformPoints -translate \'(0 %s 0)\' dwall.stl dwallu.stl\n'
        % '{0:.10g}'.format(wallthicku))
    f.write(
        'surfaceTransformPoints -translate \'(0 %s 0)\' dwall.stl dwalll.stl\n'
        % '{0:.10g}'.format(wallthickl))
    f.write(
        'surfaceTransformPoints -rollPitchYaw \'(0 0 %s)\' dwallu.stl dwallu.stl\n'
        % '{0:.10g}'.format(wall_angleu))
    f.write(
        'surfaceTransformPoints -rollPitchYaw \'(0 0 %s)\' dwalll.stl dwalll.stl\n'
        % '{0:.10g}'.format(wall_anglel))
    f.write(
        'surfaceTransformPoints -translate \'(0 %s 0)\' dwallu.stl dwallu.stl\n'
        % '{0:.10g}'.format(dwallu))
    f.write(
        'surfaceTransformPoints -translate \'(0 %s 0)\' dwalll.stl dwalll.stl\n'
        % '{0:.10g}'.format(dwalll))
    #--------------
    f.write(
        'surfaceTransformPoints -scale \'(%s %s 1)\' basic_vane.stl single_vanem.stl\n'
        % ('{0:.10g}'.format(w1), '{0:.10g}'.format(w1)))
    for i in range(len(vane_angles)):
        vname = 'vane' + str(i + 1)
        f.write(
            'surfaceTransformPoints -rollPitchYaw \'(0 0 %s)\' single_vanem.stl %s.stl\n'
            % ('{0:.10g}'.format(vane_angles[i]), vname))
        f.write(
            'surfaceTransformPoints -translate \'(0 %s 0)\' %s.stl %s.stl\n' %
            ('{0:.10g}'.format(v_shift[i]), vname, vname))
    #------------------
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
    f.write('\"dwallu.stl\"\n')
    f.write('{\n')
    f.write('    type    triSurfaceMesh;\n')
    f.write('    name    walls;\n')
    f.write('}\n')
    f.write('\"dwalll.stl\"\n')
    f.write('{\n')
    f.write('    type    triSurfaceMesh;\n')
    f.write('    name    walls;\n')
    f.write('}\n')
    for i in range(len(vane_angles)):
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
    f.write('file "dwallu.eMesh";\n')
    f.write('level %s;\n' % '{0:.0f}'.format(refledge))
    f.write('}\n')
    f.write('{\n')
    f.write('file "dwalll.eMesh";\n')
    f.write('level %s;\n' % '{0:.0f}'.format(refledge))
    f.write('}\n')
    for i in range(len(vane_angles)):
        vname = 'vane' + str(i + 1)
        f.write('{\n')
        f.write('file "%s.eMesh";\n' % vname)
        f.write('level %s;\n' % '{0:.0f}'.format(refledge))
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
    f.write('dwallu.stl\n')
    f.write('{\n')
    f.write('    extractionMethod    extractFromSurface;\n')
    f.write('    includedAngle       170;\n')
    f.write('}\n')
    f.write('dwalll.stl\n')
    f.write('{\n')
    f.write('    extractionMethod    extractFromSurface;\n')
    f.write('    includedAngle       170;\n')
    f.write('}\n')
    for i in range(len(vane_angles)):
        vname = 'vane' + str(i + 1)
        f.write('%s.stl\n' % vname)
        f.write('{\n')
        f.write('    extractionMethod    extractFromSurface;\n')
        f.write('    includedAngle       170;\n')
        f.write('}\n')

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
