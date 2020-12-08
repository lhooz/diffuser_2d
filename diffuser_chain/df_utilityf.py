"""utility function for main script"""
import csv
import numpy as np


def cal_diffuser(df_loc, w, theta, l_w, orient, No_vanes):
    """function for calculation diffuser geometry"""
    vane_angles = np.linspace(-theta, theta, No_vanes)
    if No_vanes >= 3:
        vane_angles = vane_angles[1:-1]
    else:
        vane_angles = [0.0]

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
    vls = []
    for vane in vane_angles:
        vt = 0.03 * w
        gap = 2 * vt / np.cos(vane * np.pi / 180)
        gaps.append(gap)
        total_gap += gap

    gaps.append(0)
    wo = (totalw_out - total_gap) / (len(vane_angles) + 1)

    vu = -totalw_out / 2
    v_out = []
    w_out = []
    for i in range(len(vane_angles) + 1):
        vl_next = vu + wo
        vu_next = vu + wo + gaps[i]
        vi = 0.5 * (vu + vl_next)
        v_out.append(vi)
        vu = vu_next

        w_out.append(wo)

    if orient.startswith('from'):
        x_in = df_loc[0] - l
        y_in = df_loc[1]
        df_in = [x_in, y_in]

        x_out = df_loc[0]
        layer_ins_next = []
        for vo in v_out:
            layer_ins_next.append([x_out, y_in + vo])
    elif orient == 'goingDown':
        y_in = df_loc[1] + l
        x_in = df_loc[0]
        df_in = [x_in, y_in]

        y_out = df_loc[1]
        layer_ins_next = []
        for vo in v_out:
            layer_ins_next.append([x_in + vo, y_out])
    elif orient == 'goingUp':
        y_in = df_loc[1] - l
        x_in = df_loc[0]
        df_in = [x_in, y_in]

        y_out = df_loc[1]
        layer_ins_next = []
        for vo in v_out:
            layer_ins_next.append([x_in + vo, y_out])

    return df_in, w_out, layer_ins_next, l, totalw_out


def write_parameters(parameters, fileDir):
    """write parameters to file"""
    with open(fileDir, 'w') as f:
        for par in parameters:
            f.write('%s\n' % '{0:.10g}'.format(par))


def read_parameters(parameters):
    """read design parameters"""
    par_array = []
    with open(parameters) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0

        for row in csv_reader:
            par_array.append(row[0])
            line_count += 1

        print(f'Processed {line_count} lines in {parameters}')

    par_array = np.array(par_array)
    return par_array
