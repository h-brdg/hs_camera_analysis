#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from camera_reader_mt import camera_reader
# import hampel_filter

import matplotlib.pyplot as plt

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
    ratio_array = np.empty_like(camera_dict_numer['data']) 
    for i in tqdm(range(num_frames), desc="Calculating ratios"):
        ratio_array[i] = camera_dict_numer['data'][i] / camera_dict_denom['data'][i]
        
#%% Return the dict    
    
    # camera_dict_ratio = {key:value for key, value in camera_dict_numer.items() if not key == 'data'}
    # camera_dict_ratio['data'] = ratio_array
    # exclude_key_list = ('data', 'top_frame', 'bottom_frame', 'module_dir', 'result_dir')
    # camera_dict_ratio.update({str(key + '_denom'): value for key, value in camera_dict_denom.items() if not key in exclude_key_list})

    camera_dict_ratio = {key:value for key, value in camera_dict_numer.items() if not key == 'data'}
    camera_dict_ratio.update({str(key + '_numer'): value for key, value in camera_dict_numer.items() if not key == 'data'})
    camera_dict_ratio.update({str(key + '_denom'): value for key, value in camera_dict_denom.items() if not key == 'data'})
    camera_dict_ratio['data'] = ratio_array
    return camera_dict_ratio
    
#%% Test
if __name__ == "__main__":
    import time
    def plot_ratio_array_test(ratio_array, vmin=None, vmax=None):
        num_frames = ratio_array.shape[0]
        fig, axs = plt.subplots(1, num_frames, figsize=(15, 5))
        
        for i in range(num_frames):
            ax = axs[i] if num_frames > 1 else axs
            im = ax.imshow(ratio_array[i], cmap='viridis', vmin=vmin, vmax=vmax)
            ax.set_title(f"Frame {i+1}")
            ax.axis('off')
        
        # Add a colorbar to show the scale
        fig.colorbar(im, ax=axs, orientation='vertical', fraction=0.02, pad=0.04)
        plt.tight_layout()
        plt.show()
    
    
    time_sta = time.time()
    shot_li = [256221]
    frame_tgt=11000
    num_frames=1
    line_ch_li = [('4', '2')]; (vmin,vmax) = (0,0.5)
    # line_ch_li = [('1', '2')]; (vmin,vmax) = (0,30)
    # line_ch_li = [('1', '4')]; (vmin,vmax) = (0,30)
    for shot_no in shot_li:
        for line_ch in line_ch_li:
            camera_dict_ratio = calc_ratio(shot_no, line_ch, frame_tgt, num_frames)

            plot_ratio_array_test(camera_dict_ratio['data'], vmin, vmax)
    time_end = time.time()
    print('Time spent: ' + str(time_end-time_sta) + ' (s)')
    #print(camera_dict['frame_rate'])