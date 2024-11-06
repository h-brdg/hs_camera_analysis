#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from camera_reader_mt import camera_reader
import read_config_info
# import hampel_filter

import matplotlib.pyplot as plt

def calc_int(shot_no, line_ch, frame_tgt, num_frames):
    camera_dict_int = camera_reader(shot_no, line_ch, frame_tgt, num_frames, flg_rot=False)
    config_dict = read_config_info.read_config_info()
    
#%% Background
    # subtract the black level 128+64=192
    camera_dict_int['data'] = camera_dict_int['data']-(192*camera_dict_int['coeff'])
    
    max_int_value = None
    min_int_value = 1E-10
    
    np.clip(camera_dict_int['data'], min_int_value, max_int_value, out=camera_dict_int['data'])
        
    return camera_dict_int
    
#%% Test
if __name__ == "__main__":
    import time
    def plot_int_array_test(int_array, vmin=None, vmax=None):
        num_frames = int_array.shape[0]
        fig, axs = plt.subplots(1, num_frames, figsize=(15, 5))
        
        for i in range(num_frames):
            ax = axs[i] if num_frames > 1 else axs
            im = ax.imshow(int_array[i], cmap='viridis', vmin=vmin, vmax=vmax)
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
    line_ch_li = ['4', '2']
    for shot_no in shot_li:
        for line_ch in line_ch_li:
            camera_dict_int = calc_int(shot_no, line_ch, frame_tgt, num_frames)
            (vmin,vmax) = (0, np.max(camera_dict_int['data']))
            plot_int_array_test(camera_dict_int['data'], vmin, vmax)
    time_end = time.time()
    print('Time spent: ' + str(time_end-time_sta) + ' (s)')
    #print(camera_dict['frame_rate'])