#!/usr/bin/env python3

import load_tiff
import read_conv_info
import transform_image 
import read_path_info
import numpy as np
from tqdm import tqdm

def camera_reader(shot_no, line_ch, frame_tgt=0, num_frames=0, flg_rot=False):
    """
    Reads and processes images from the camera.

    Parameters:
    shot_no (int): Shot number.
    line_ch (str): Line channel '1' - '4' and 'all'.
    frame_tgt (int): Target frame number. Default is 0: the initial frame.
    num_frames (int): Number of frames to read. Default is 0: everything.
    flg_rot (bool): Flag to indicate if rotation is needed. Default is False.

    Returns:
    dict: A dictionary containing processed image data and metadata.
    """
    # config and paths
    config_dict = read_path_info.read_path_info()
    tiff_dir = config_dict['tiff_dir']
    
    # read tiff and convert info
    try:
        conv_dict = read_conv_info.read_conv_info(shot_no, tiff_dir)
        frame_size_x = int(conv_dict['frame_size_x'])
        frame_size_y = int(conv_dict['frame_size_y'])
        dtype = np.uint16  # Assuming 16-bit TIFF images; modify if different
        if num_frames == 0:
            num_frames = int(conv_dict['bottom_frame']) - int(conv_dict['top_frame']) - frame_tgt  # Load all remaining frames
        img_array = np.memmap('img_array.dat', dtype=dtype, mode='w+', shape=(num_frames, frame_size_y, frame_size_x))
        
        for i in tqdm(range(frame_tgt, frame_tgt + num_frames), desc="Loading frames..."):
            img_array[i - frame_tgt] = load_tiff.load_tiff(shot_no, tiff_dir, i, 1)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None

    # process raw image
    img_array, tra_dict, coeff = transform_image.transform_image(shot_no, line_ch, tiff_dir, img_array, flg_rot)
    
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
    shot_no = 256221
    frame_tgt = 0
    num_frames = 0
    flg_rot = False
    line_ch = '2'
    
    camera_dict = camera_reader(shot_no, line_ch, frame_tgt, num_frames, flg_rot)
    camera_dict['imgs'][0,30,25] = np.max(camera_dict['imgs'])
    plt.imshow(camera_dict['imgs'][0,:,:]) # [frame, x, z]
    time_end = time.time()
    print('Time spent: ' + str(time_end-time_sta) + ' (s)')