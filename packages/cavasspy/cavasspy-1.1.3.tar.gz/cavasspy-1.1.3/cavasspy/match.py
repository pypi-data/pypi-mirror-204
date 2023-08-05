import shutil

import numpy as np

from cavasspy.op import get_ct_resolution, read_cavass_file, save_cavass_file


def match_im0(im0_file, bim_file, output_file):
    shape_1 = get_ct_resolution(im0_file)
    shape_2 = get_ct_resolution(bim_file)
    if shape_1[2] == shape_2[2]:
        shutil.copy(bim_file, output_file)
    else:
        original_data = read_cavass_file(bim_file)
        data = np.zeros(shape_1, dtype=np.bool)
        data[..., :original_data.shape[2]] = original_data
        save_cavass_file(output_file, data, True, reference_file=im0_file)
