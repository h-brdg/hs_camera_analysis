#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from camera_reader_mt import camera_reader

def calc_ratio(shot_no, line_ch_li, frame_tgt, num_frames):
    camera_dict_numer = camera_reader(shot_no, line_ch_li[0], frame_tgt, num_frames, flg_rot=True)
    camera_dict_denom = camera_reader(shot_no, line_ch_li[1], frame_tgt, num_frames, flg_rot=True)
    
    #%% Background
    # Subtract the black level 128 + 64 = 192
    camera_dict_numer['data'] = camera_dict_numer['data'] - (192 * camera_dict_numer['coeff'])
    camera_dict_denom['data'] = camera_dict_denom['data'] - (192 * camera_dict_denom['coeff'])
       
    max_int_value = None
    min_int_value = 1E-10
    
    # Mark invalid pixels with value below min_int_value
    camera_dict_numer['invalid_data'] = (
        (camera_dict_numer['data'] <= min_int_value) | (camera_dict_numer['data'] < 0)
    )

    # Avoid zero divider error
    np.clip(camera_dict_numer['data'], min_int_value, max_int_value, out=camera_dict_numer['data'])
    np.clip(camera_dict_denom['data'], min_int_value, max_int_value, out=camera_dict_denom['data'])
    
    #%% Calculate the ratio for each frame
    camera_ratio_data = np.empty_like(camera_dict_numer['data'], dtype='float32')
    print("Using in-memory array for the ratio data")
    
    for i in tqdm(range(camera_ratio_data.shape[0]), total=camera_ratio_data.shape[0], desc="Calculating ratios"):
        camera_ratio_data[i] = camera_dict_numer['data'][i] / camera_dict_denom['data'][i]
        
    #%% Prepare the dictionary to return
    camera_dict_ratio = {key: value for key, value in camera_dict_numer.items() if key != 'data'}
    camera_dict_ratio.update({f"{key}_numer": value for key, value in camera_dict_numer.items() if key != 'data'})
    camera_dict_ratio.update({f"{key}_denom": value for key, value in camera_dict_denom.items() if key != 'data'})
    camera_dict_ratio['data'] = camera_ratio_data
    
    # Apply NaN to invalid data points
    camera_dict_ratio['data'] = np.where(camera_dict_numer['invalid_data'], np.nan, camera_dict_ratio['data'])
    
    return camera_dict_ratio
    
#%% Test
if __name__ == "__main__":
    import time
    
    time_sta = time.time()
    shot_li = [256221]
    frame_tgt = 0
    num_frames = 0
    line_ch_li = [('4', '2')]
    
    for shot_no in shot_li:
        for line_ch in line_ch_li:
            camera_dict_ratio = calc_ratio(shot_no, line_ch, frame_tgt, num_frames)
    
    time_end = time.time()
    print('Time spent:', time_end - time_sta, '(s)')
