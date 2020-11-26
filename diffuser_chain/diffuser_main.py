"""main script for organizing diffuser design"""
import os
import shutil
import numpy as np

diffusers = ['diffuser_25_2', 'diffuser_25_2']
inlet_w = 0.11
#---------------------------------------------------
h_loc = [0.0, 1.0]
v_loc = [0.0, -1.0]
layer_width = [0.0, 1.0]
#---------------------------------------------------
refl = 3
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
basic_tunner = os.path.join(cwd, 'basic_elements', 'tunner')
basic_tube = os.path.join(cwd, 'basic_elements', 'tube')

if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.mkdir(output_folder)

w_in = [inlet_w]
coordinates_in = [[0, 0]]
for li in range(len(diffusers)):
    no_dfs = len(w_in)
    if li != 0:
        if li % 2 == 0:
            h_dfs = np.linspace(h_loc[li], h_loc[li] + layer_width[li], no_dfs)
            v_dfs = np.zeros(no_dfs) + v_loc[li]
        else:
            h_dfs = np.zeros(no_dfs) + h_loc[li]
            v_dfs = np.linspace(v_loc[li], v_loc[li] + layer_width[li], no_dfs)

    for dfi in range(no_dfs):
        theta = float(diffusers[li].split('_')[1])
        l_w = float(diffusers[li].split('_')[2])
        w_out, coordinates_out, l, w_end = cal_diffuder(
            coordinates_in[dfi], w_in[dfi], theta, l_w, li)
        if li == 0:
            shutil.copytree(basic_df,
                            os.path.join(output_folder, 'diffuser_main'))
        else:
            shutil.copytree(
                basic_df,
                os.path.join(output_folder, 'df_' + str(li) + '_' + str(dfi)))

        if li != 0:
            if li % 2 == 0:
                htube_l = h_dfs[dfi] - coordinates_in[dfi][
                    0] - 0.7 * w_in[dfi] - l
                vtube_l = v_dfs[dfi] - coordinates_in[dfi][1] - 0.7 * w_in[dfi]
                tunner_in = [
                    coordinates_in[dfi][0], coordinates_in[dfi][1] + vtube_l
                ]
                tunner_out = [
                    tunner_in[0] + 0.7 * w_in[dfi],
                    tunner_in[1] + 0.7 * w_in[dfi]
                ]
                tunner_rot = 90.0
                tube_rot = 90.0
            else:
                htube_l = h_dfs[dfi] - coordinates_in[dfi][0] - 0.7 * w_in[dfi]
                vtube_l = v_dfs[dfi] - coordinates_in[dfi][
                    1] - 0.7 * w_in[dfi] - l
                tunner_in = [
                    coordinates_in[dfi][0] + htube_l, coordinates_in[dfi][1]
                ]
                tunner_out = [
                    tunner_in[0] + 0.7 * w_in[dfi],
                    tunner_in[1] - 0.7 * w_in[dfi]
                ]
                tunner_rot = 0.0
                tube_rot = -90.0

            shutil.copytree(
                basic_tube,
                os.path.join(output_folder, 'htb_' + str(li) + '_' + str(dfi)))
            shutil.copytree(
                basic_tube,
                os.path.join(output_folder, 'vtb_' + str(li) + '_' + str(dfi)))
            shutil.copytree(
                basic_tunner,
                os.path.join(output_folder,
                             'tunner_' + str(li) + '_' + str(dfi)))


def cal_diffuder(xy, w, theta, l_w, i):
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

    if i % 2 == 0:
        x_out = xy[0] + l
        y1 = xy[1] - vco2
        y2 = xy[1] - vco1
        y3 = xy[1] + vco1
        y4 = xy[1] + vco2
        coordinates_out = [[x_out, y1], [x_out, y2], [x_out, y3], [x_out, y4]]
    else:
        y_out = xy[1] - l
        x1 = xy[0] - vco2
        x2 = xy[0] - vco1
        x3 = xy[0] + vco1
        x4 = xy[0] + vco2
        coordinates_out = [[x1, y_out], [x2, y_out], [x3, y_out], [x4, y_out]]

    return w_out, coordinates_out, l, w_end
