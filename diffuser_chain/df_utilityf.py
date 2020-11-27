"""utility function for main script"""
import numpy as np


def cal_diffuser(df_loc, w, theta, l_w, orient):
    """function for calculation diffuser geometry"""
    l = l_w * w
    v1 = 0.03 * w
    vane_gap = v1 / np.cos(theta / 1.45 * np.pi / 180)
    v_uvane = np.tan(theta / 1.45 * np.pi / 180) * l
    v2 = v_uvane - vane_gap + 0.3 * w
    v3 = v_uvane + vane_gap + 0.3 * w
    v4 = 0.5 * w + np.sin(theta * np.pi / 180) * l
    vco1 = 0.5 * (v1 + v2)
    vco2 = 0.5 * (v3 + v4)
    w1 = v2 - v1
    w2 = v4 - v3
    w_end = 2 * v4
    w_out = [w2, w1, w1, w2]

    if orient.startswith('from'):
        x_in = df_loc[0] - l
        y_in = df_loc[1]
        x_out = df_loc[0]
        y1 = y_in - vco2
        y2 = y_in - vco1
        y3 = y_in + vco1
        y4 = y_in + vco2
        df_in = [x_in, y_in]
        layer_ins_next = [[x_out, y1], [x_out, y2], [x_out, y3], [x_out, y4]]
    elif orient == 'goingDown':
        y_in = df_loc[1] + l
        x_in = df_loc[0]
        y_out = df_loc[1]
        x1 = x_in - vco2
        x2 = x_in - vco1
        x3 = x_in + vco1
        x4 = x_in + vco2
        df_in = [x_in, y_in]
        layer_ins_next = [[x1, y_out], [x2, y_out], [x3, y_out], [x4, y_out]]
    elif orient == 'goingUp':
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


def write_parameters(parameters, fileDir):
    """write parameters to file"""
    with open(fileDir, 'w') as f:
        for par in parameters:
            f.write('%s\n' % '{0:.3g}'.format(par))
