#!/usr/bin/env python3

import load_tiff
import read_conv_info
import transform_image 
import read_path_info

def camera_reader(shot_no, line_ch, frame_tgt=0, num_frames=0, flg_rot=False):
    # config and paths
    config_dict = read_path_info.read_path_info()
    tiff_dir = config_dict['tiff_dir']
    
    # read tiff and convert info
    img_array = load_tiff.load_tiff(shot_no, tiff_dir, frame_tgt, num_frames)
    conv_dict = read_conv_info.read_conv_info(shot_no, tiff_dir)
    
    # process raw image
    img_array, tra_dict, coeff = transform_image.transform_image(shot_no, line_ch, tiff_dir, img_array, flg_rot)
    
    #print(img_array.shape)
    
    camera_dict = {'imgs': img_array, 'coeff': coeff, 'frame_start': frame_tgt}
    camera_dict.update(conv_dict)
    camera_dict.update(tra_dict)
    camera_dict.update(config_dict)
    
    return camera_dict
    
#%% Test
if __name__ == "__main__":
    
    import time
    import matplotlib.pyplot as plt
    import numpy as np
    
    time_sta = time.time()
    # shot_no = 255144
    shot_no = 255817
    # shot_no = 255820
    frame_tgt=3000
    num_frames=2
    flg_rot=False
    # flg_rot=True
    line_ch = '2' 
    #line_ch = 'n2_1ps'
    camera_dict = camera_reader(shot_no, line_ch, frame_tgt, num_frames, flg_rot)
    camera_dict['imgs'][0,30,25] = np.max(camera_dict['imgs'])
    plt.imshow(camera_dict['imgs'][0,:,:]) # [frame, x, z]
    # plt.plot(camera_dict['imgs'][:,55,130])
    plt.show
    # print(camera_dict['imgs'].shape)
    # print(camera_dict['imgs'][2])
    time_end = time.time()
    print('Time spent: ' + str(time_end-time_sta) + ' (s)')
    #print(camera_dict['frame_rate'])
