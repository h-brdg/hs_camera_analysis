#!/usr/bin/env python3

import numpy as np

from camera_reader_mt import camera_reader
# import hampel_filter

def calc_int(shot_no, line_ch, frame_tgt, num_frames):
    camera_dict_int = camera_reader(shot_no, line_ch, frame_tgt, num_frames, flg_rot=False)
    
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
    
    time_sta = time.time()
    shot_li = [256221]
    frame_tgt=0
    num_frames=0
    line_ch_li = ['4', '2', '1']
    for shot_no in shot_li:
        for line_ch in line_ch_li:
            camera_dict_int = calc_int(shot_no, line_ch, frame_tgt, num_frames)
            (vmin,vmax) = (0, np.max(camera_dict_int['data']))
    time_end = time.time()
    print('Time spent: ' + str(time_end-time_sta) + ' (s)')
    #print(camera_dict['frame_rate'])