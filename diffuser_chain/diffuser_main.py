"""main script for organizing diffuser design"""
import os
import shutil

import numpy as np
from df_utilityf import cal_diffuser, write_parameters

diffusers = ['diffuser_25_2', 'diffuser_15_2']
inlet_w = 0.11
turnp_R = [0.3, 0.3]
#---------------------------------------------------
layer_out = [[0.0, 0.0], [0.1, -0.35]]
layer_width = [0.0, 0.52]
layer_orientation = ['fromUp', 'goingDown']
initial_pipe = 'straight'
#---------------------------------------------------
refl = 2
#----------------------------------------------------
wall_layer_thickness = 6e-4
#----------------------------------------------------
refledge = refl
reflcurvature = refl
mesh_size = wall_layer_thickness * 2**refl
#----------------------------------------------------
cwd = os.getcwd()

output_folder = os.path.join(cwd, 'diffuser_design')
basic_df = os.path.join(cwd, 'basic_elements', 'vane_diffuser')
basic_turnp = os.path.join(cwd, 'basic_elements', 'turnp')
basic_tube = os.path.join(cwd, 'basic_elements', 'tube')
config_control_file = os.path.join(output_folder, 'config_control.sh')

if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.mkdir(output_folder)
with open(config_control_file, 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions\n')

w_in = [inlet_w]
layer_ins = [[-0.7, 0.2]]
for li in range(len(diffusers)):
    #--------------
    # print(layer_ins)
    #--------------
    no_dfs = len(w_in)
    orientation = layer_orientation[li]
    if orientation.startswith('from'):
        h_dfs = np.zeros(no_dfs) + layer_out[li][0]
        v_dfs = np.linspace(layer_out[li][1],
                            layer_out[li][1] + layer_width[li], no_dfs)
    elif orientation.startswith('going'):
        h_dfs = np.linspace(layer_out[li][0],
                            layer_out[li][0] + layer_width[li], no_dfs)
        v_dfs = np.zeros(no_dfs) + layer_out[li][1]
    df_locs = [[x, y] for x, y in zip(h_dfs, v_dfs)]

    wOut_all = []
    layerNext_all = []
    for dfi in range(no_dfs):
        theta = float(diffusers[li].split('_')[1])
        l_w = float(diffusers[li].split('_')[2])
        #--------df no of vanes calculation---
        No_vanes = int(np.ceil(2 * theta / 8))
        #-------------------------------------
        df_in, w_out, layer_ins_next, l = cal_diffuser(df_locs[dfi], w_in[dfi],
                                                       theta, l_w, orientation,
                                                       No_vanes)
        wOut_all += w_out
        layerNext_all += layer_ins_next
        #------------------------------------------------------------------
        if orientation == 'fromUp':
            ftb_l = -df_in[1] + layer_ins[dfi][1] - 0.7 * w_in[dfi]
            btb_l = df_in[0] - layer_ins[dfi][0] - 0.7 * w_in[dfi]
            ftb_in = layer_ins[dfi]
            turnp_in = [ftb_in[0], ftb_in[1] - ftb_l]
            btb_in = [
                turnp_in[0] + 0.7 * w_in[dfi], turnp_in[1] - 0.7 * w_in[dfi]
            ]
            rot_chain = [-90, 90, 0, 0]
            turnp_yscale = -1
        elif orientation == 'fromDown':
            ftb_l = df_in[1] - layer_ins[dfi][1] - 0.7 * w_in[dfi]
            btb_l = df_in[0] - layer_ins[dfi][0] - 0.7 * w_in[dfi]
            ftb_in = layer_ins[dfi]
            turnp_in = [ftb_in[0], ftb_in[1] + ftb_l]
            btb_in = [
                turnp_in[0] + 0.7 * w_in[dfi], turnp_in[1] + 0.7 * w_in[dfi]
            ]
            rot_chain = [90, 90, 0, 0]
            turnp_yscale = 1
        elif orientation == 'goingDown':
            ftb_l = df_in[0] - layer_ins[dfi][0] - 0.7 * w_in[dfi]
            btb_l = -df_in[1] + layer_ins[dfi][1] - 0.7 * w_in[dfi]
            ftb_in = layer_ins[dfi]
            turnp_in = [ftb_in[0] + ftb_l, ftb_in[1]]
            btb_in = [
                turnp_in[0] + 0.7 * w_in[dfi], turnp_in[1] - 0.7 * w_in[dfi]
            ]
            rot_chain = [0, 0, -90, -90]
            turnp_yscale = 1
            # print(df_in[0], turnp_in[0] + 0.7 * w_in[dfi])
        elif orientation == 'goingUp':
            ftb_l = df_in[0] - layer_ins[dfi][0] - 0.7 * w_in[dfi]
            btb_l = df_in[1] - layer_ins[dfi][1] - 0.7 * w_in[dfi]
            ftb_in = layer_ins[dfi]
            turnp_in = [ftb_in[0] + ftb_l, ftb_in[1]]
            btb_in = [
                turnp_in[0] + 0.7 * w_in[dfi], turnp_in[1] + 0.7 * w_in[dfi]
            ]
            rot_chain = [0, 0, 90, 90]
            turnp_yscale = -1

        ftb_parameters = [
            ftb_in[0], ftb_in[1], w_in[dfi], ftb_l, mesh_size, refl, refledge,
            reflcurvature, rot_chain[0]
        ]
        turnp_parameters = [
            turnp_in[0], turnp_in[1], w_in[dfi], turnp_R[li], mesh_size, refl,
            refledge, reflcurvature, rot_chain[1], turnp_yscale
        ]
        btb_parameters = [
            btb_in[0], btb_in[1], w_in[dfi], btb_l, mesh_size, refl, refledge,
            reflcurvature, rot_chain[2]
        ]
        df_parameters = [
            df_in[0], df_in[1], w_in[dfi], theta, l_w, mesh_size, refl,
            refledge, reflcurvature, rot_chain[3], No_vanes
        ]

        #----------------
        print([ftb_l, btb_l])
        #---------------------------------------------------------
        if li == 0:
            df_folder = os.path.join(output_folder, '0_diffuser_main')
        else:
            df_folder = os.path.join(output_folder,
                                     'df_' + str(li) + '_' + str(dfi))
        ftb_folder = os.path.join(output_folder,
                                  'ftb_' + str(li) + '_' + str(dfi))
        btb_folder = os.path.join(output_folder,
                                  'btb_' + str(li) + '_' + str(dfi))
        turnp_folder = os.path.join(output_folder,
                                    'turnp_' + str(li) + '_' + str(dfi))
        df_file = os.path.join(df_folder, 'df_parameters')
        ftb_file = os.path.join(ftb_folder, 'tb_parameters')
        btb_file = os.path.join(btb_folder, 'tb_parameters')
        turnp_file = os.path.join(turnp_folder, 'turnp_parameters')
        #-----------------------------------------------
        shutil.copytree(basic_tube, ftb_folder)
        shutil.copytree(basic_turnp, turnp_folder)
        shutil.copytree(basic_tube, btb_folder)
        shutil.copytree(basic_df, df_folder)

        write_parameters(ftb_parameters, ftb_file)
        write_parameters(turnp_parameters, turnp_file)
        write_parameters(btb_parameters, btb_file)
        write_parameters(df_parameters, df_file)

        with open(config_control_file, 'a') as f:
            f.write('cd %s\n' % df_folder)
            f.write('sh run_mesh.sh\n')
            if not df_folder.endswith('diffuser_main'):
                f.write(
                    'runParallel mergeMeshes ../0_diffuser_main . -overwrite\n'
                )
            f.write('cd ..\n')

            if li == 0:
                if initial_pipe == 'all':
                    f.write('cd %s\n' % ftb_folder)
                    f.write('sh run_mesh.sh\n')
                    f.write(
                        'runParallel mergeMeshes ../0_diffuser_main . -overwrite\n'
                    )
                    f.write('cd ..\n')

                    f.write('cd %s\n' % turnp_folder)
                    f.write('sh run_mesh.sh\n')
                    f.write(
                        'runParallel mergeMeshes ../0_diffuser_main . -overwrite\n'
                    )
                    f.write('cd ..\n')

                    f.write('cd %s\n' % btb_folder)
                    f.write('sh run_mesh.sh\n')
                    f.write(
                        'runParallel mergeMeshes ../0_diffuser_main . -overwrite\n'
                    )
                    f.write('cd ..\n')
                elif initial_pipe == 'straight':
                    f.write('cd %s\n' % btb_folder)
                    f.write('sh run_mesh.sh\n')
                    f.write(
                        'runParallel mergeMeshes ../0_diffuser_main . -overwrite\n'
                    )
                    f.write('cd ..\n')
            else:
                f.write('cd %s\n' % ftb_folder)
                f.write('sh run_mesh.sh\n')
                f.write(
                    'runParallel mergeMeshes ../0_diffuser_main . -overwrite\n'
                )
                f.write('cd ..\n')

                f.write('cd %s\n' % turnp_folder)
                f.write('sh run_mesh.sh\n')
                f.write(
                    'runParallel mergeMeshes ../0_diffuser_main . -overwrite\n'
                )
                f.write('cd ..\n')

                f.write('cd %s\n' % btb_folder)
                f.write('sh run_mesh.sh\n')
                f.write(
                    'runParallel mergeMeshes ../0_diffuser_main . -overwrite\n'
                )
                f.write('cd ..\n')
        #----------------------------------
    w_in = wOut_all
    layer_ins = layerNext_all
