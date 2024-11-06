#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from camera_reader_mt import camera_reader
# import hampel_filter

def calc_ratio(shot_no, line_ch_li, frame_tgt, num_frames):
    camera_dict_numer = camera_reader(shot_no, line_ch_li[0], frame_tgt, num_frames, flg_rot=True)
    camera_dict_denom = camera_reader(shot_no, line_ch_li[1], frame_tgt, num_frames, flg_rot=True)
    
#%% Background
    # subtract the black level 128+64=192
    camera_dict_numer['data'] = camera_dict_numer['data']-(192*camera_dict_numer['coeff'])
    camera_dict_denom['data'] = camera_dict_denom['data']-(192*camera_dict_denom['coeff'])
    
    max_int_value = None
    min_int_value = 1E-10
    
    np.clip(camera_dict_numer['data'], min_int_value, max_int_value, out=camera_dict_numer['data'])
    np.clip(camera_dict_denom['data'], min_int_value, max_int_value, out=camera_dict_denom['data'])
    
#%% Calc
    # Calculate the ratio for each frame
    
    estimated_size_gb = (camera_dict_numer['data'].size * 4) / (1024 ** 3)
    # print('Estimated size of the data: ' + str(estimated_size_gb) + 'GB')

    # if True:   # For testing
    if estimated_size_gb > int(camera_dict_numer['mem_limit_size']):
        memmap_filename = 'ratio_data.dat'
        trimmed_memmap = np.memmap(memmap_filename, dtype='float32', mode='w+', shape=camera_dict_numer['data'].shape)
        camera_ratio_data = trimmed_memmap
        print("Using memmap due to large data size")
    else:
        camera_ratio_data =  np.empty_like(camera_dict_numer['data'], dtype='float32')
        print("Using in-memory array")
        # print(camera_ratio_data.shape)
    
    for i in tqdm(range(camera_ratio_data.shape[0]), total=camera_ratio_data.shape[0], desc="Calculating ratios"):
        camera_ratio_data[i] = camera_dict_numer['data'][i] / camera_dict_denom['data'][i]
        
#%% Return the dict    
    
    # camera_dict_ratio = {key:value for key, value in camera_dict_numer.items() if not key == 'data'}
    # camera_dict_ratio['data'] = camera_ratio_data
    # exclude_key_list = ('data', 'top_frame', 'bottom_frame', 'module_dir', 'result_dir')
    # camera_dict_ratio.update({str(key + '_denom'): value for key, value in camera_dict_denom.items() if not key in exclude_key_list})

    camera_dict_ratio = {key:value for key, value in camera_dict_numer.items() if not key == 'data'}
    camera_dict_ratio.update({str(key + '_numer'): value for key, value in camera_dict_numer.items() if not key == 'data'})
    camera_dict_ratio.update({str(key + '_denom'): value for key, value in camera_dict_denom.items() if not key == 'data'})
    camera_dict_ratio['data'] = camera_ratio_data
    return camera_dict_ratio
    
#%% Test
if __name__ == "__main__":
    import time
    
    time_sta = time.time()
    shot_li = [256221]
    frame_tgt=11500
    num_frames=0
    line_ch_li = [('4', '2')]; (vmin,vmax) = (0,0.5)
    # line_ch_li = [('1', '2')]; (vmin,vmax) = (0,30)
    # line_ch_li = [('1', '4')]; (vmin,vmax) = (0,30)
    for shot_no in shot_li:
        for line_ch in line_ch_li:
            camera_dict_ratio = calc_ratio(shot_no, line_ch, frame_tgt, num_frames)
    time_end = time.time()
    print('Time spent: ' + str(time_end-time_sta) + ' (s)')
    #print(camera_dict['frame_rate'])