"""main script for organizing diffuser design"""
import os
import shutil

import numpy as np

diffusers = ['diffuser_25_2', 'diffuser_25_2']
inlet_w = 0.11
#---------------------------------------------------
layer_out = [[0.0, 0.0], [1.0, -1.0]]
layer_width = [0.0, 1.0]
layer_orientation = [-1, -90]
#---------------------------------------------------
refl = 1
#----------------------------------------------------
wall_layer_thickness = 1e-3
#----------------------------------------------------
refledge = refl
reflcurvature = refl
mesh_size = wall_layer_thickness * 2**refl
#----------------------------------------------------
cwd = os.getcwd()

output_folder = os.path.join(cwd, 'diffuser_design')
basic_df = os.path.join(cwd, 'basic_elements', 'vaned_diffuser')
basic_turnp = os.path.join(cwd, 'basic_elements', 'turnp')
basic_tube = os.path.join(cwd, 'basic_elements', 'tube')

if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.mkdir(output_folder)

w_in = [inlet_w]
layer_ins = [[-1.0, 1.0]]
for li in range(len(diffusers)):
    no_dfs = len(w_in)
    orientation = layer_orientation[li]
    if orientation in [1, -1]:
        h_dfs = np.zeros(no_dfs) + layer_out[li][0]
        v_dfs = np.linspace(layer_out[li][1],
                            layer_out[li][1] + layer_width[li], no_dfs)
    elif orientation in [90, -90]:
        h_dfs = np.linspace(layer_out[li][0],
                            layer_out[li][0] + layer_width[li], no_dfs)
        v_dfs = np.zeros(no_dfs) + layer_out[li][1]
    df_locs = [[x, y] for x, y in zip(h_dfs, v_dfs)]

    for dfi in range(no_dfs):
        theta = float(diffusers[li].split('_')[1])
        l_w = float(diffusers[li].split('_')[2])
        df_in, w_out, layer_ins_next, l = cal_diffuder(df_locs[dfi], w_in[dfi],
                                                       theta, l_w, orientation)
        #---------------------------------------------------------
        if li == 0:
            df_folder = os.path.join(output_folder, 'diffuser_main')
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
        #------------------------------------------------------------------

        if orientation == -1:
            ftb_l = -df_in[1] + layer_ins[dfi][1] - 0.7 * w_in[dfi]
            btb_l = df_in[0] - layer_ins[dfi][0] - 0.7 * w_in[dfi]
            ftb_in = layer_ins[dfi]
            turnp_in = [ftb_in[0], ftb_in[1] - ftb_l]
            btb_in = [
                turnp_in[0] + 0.7 * w_in[dfi], turnp_in[1] - 0.7 * w_in[dfi]
            ]
        elif orientation == 1:
            ftb_l = df_in[1] - layer_ins[dfi][1] - 0.7 * w_in[dfi]
            btb_l = df_in[0] - layer_ins[dfi][0] - 0.7 * w_in[dfi]
            ftb_in = layer_ins[dfi]
            turnp_in = [ftb_in[0], ftb_in[1] + ftb_l]
            btb_in = [
                turnp_in[0] + 0.7 * w_in[dfi], turnp_in[1] + 0.7 * w_in[dfi]
            ]
        elif orientation == -90:
            ftb_l = df_in[0] - layer_ins[dfi][0] - 0.7 * w_in[dfi]
            btb_l = -df_in[1] + layer_ins[dfi][1] - 0.7 * w_in[dfi]
            ftb_in = layer_ins[dfi]
            turnp_in = [ftb_in[0] + ftb_l, ftb_in[1]]
            btb_in = [
                turnp_in[0] + 0.7 * w_in[dfi], turnp_in[1] - 0.7 * w_in[dfi]
            ]
        elif orientation == 90:
            ftb_l = df_in[0] - layer_ins[dfi][0] - 0.7 * w_in[dfi]
            btb_l = df_in[1] - layer_ins[dfi][1] - 0.7 * w_in[dfi]
            ftb_in = layer_ins[dfi]
            turnp_in = [ftb_in[0] + ftb_l, ftb_in[1]]
            btb_in = [
                turnp_in[0] + 0.7 * w_in[dfi], turnp_in[1] + 0.7 * w_in[dfi]
            ]

        htb_parameters = [[dfi], w_in[dfi], htube_l, mesh_size, refl, refledge,
                          reflcurvature, 0.0]
        vtb_parameters = [
            w_in[dfi], vtube_l, mesh_size, refl, refledge, reflcurvature, -90.0
        ]
        shutil.copytree(basic_tube, htb_folder)
        shutil.copytree(basic_tube, vtb_folder)
        shutil.copytree(basic_turnp, turnp_folder)

        df_parameters = [
            coordinates_in[dfi], w_in[dfi], theta, l_w, mesh_size, refl,
            refledge, reflcurvature
        ]
        shutil.copytree(basic_df, df_folder)


def cal_diffuder(df_loc, w, theta, l_w, orientation):
    """function for calculation diffuser geometry"""
    l = l_w * w
    v1 = 0.03 * w
    vane_gap = v1 / np.cos(theta / 1.45 * np.pi / 180)
    v_uvane = np.tan(theta / 1.45 * np.pi / 180) * l
    v2 = v_uvane - vane_gap + 0.3 * w
    v3 = v_uvane + vane_gap + 0.6 * w
    v4 = 0.5 * w + np.sin(theta * np.pi / 180) * l
    vco1 = 0.5 * (v1 + v2)
    vco2 = 0.5 * (v3 + v4)
    w1 = v2 - v1
    w2 = v4 - v3
    w_end = 2 * v4
    wout = [w2, w1, w1, w2]

    if orientation in [1, -1]:
        x_in = df_loc[0] - l
        y_in = df_loc[1]
        x_out = df_loc[0]
        y1 = y_in - vco2
        y2 = y_in - vco1
        y3 = y_in + vco1
        y4 = y_in + vco2
        df_in = [x_in, y_in]
        layer_ins_next = [[x_out, y1], [x_out, y2], [x_out, y3], [x_out, y4]]
    elif orientation == -90:
        y_in = df_loc[1] + l
        x_in = df_loc[0]
        y_out = df_loc[1]
        x1 = x_in - vco2
        x2 = x_in - vco1
        x3 = x_in + vco1
        x4 = x_in + vco2
        df_in = [x_in, y_in]
        layer_ins_next = [[x1, y_out], [x2, y_out], [x3, y_out], [x4, y_out]]
    elif orientation == 90:
        y_in = df_loc[1] - l
        x_in = df_loc[0]
        y_out = df_loc[1]
        x1 = x_in - vco2
        x2 = x_in - vco1
        x3 = x_in + vco1
        x4 = x_in + vco2
        df_in = [x_in, y_in]
        layer_ins_next = [[x1, y_out], [x2, y_out], [x3, y_out], [x4, y_out]]

    return df_in, w_out, layer_ins_next, l
