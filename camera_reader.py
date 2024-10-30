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
    conv_dict = read_conv_info.read_conv_info(shot_no, tiff_dir)
    
    if num_frames == 0:
        num_frames = int(conv_dict['bottom_frame']) - int(conv_dict['top_frame']) - frame_tgt  # Load all remaining frames
    
    # Initialize an empty array for the memmap
    first_frame = load_tiff.load_tiff(shot_no, tiff_dir, frame_tgt, 1)
    first_frame, tra_dict, coeff = transform_image.transform_image(shot_no, line_ch, tiff_dir, first_frame, flg_rot)
    
    memmap_shape = (num_frames,) + first_frame.shape
    memmap_filename = 'trimmed_image.dat'
    trimmed_memmap = np.memmap(memmap_filename, dtype='float32', mode='w+', shape=memmap_shape)
    
    # Process each frame
    for i in tqdm(range(frame_tgt, frame_tgt + num_frames), desc="Loading frames..."):
        try:
            img_array = load_tiff.load_tiff(shot_no, tiff_dir, i, 1)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None
        
        # Transform the image
        img_array, tra_dict, coeff = transform_image.transform_image(shot_no, line_ch, tiff_dir, img_array, flg_rot)
        
        # Save the trimmed image to the memmap
        trimmed_memmap[i - frame_tgt] = img_array

    # Create a dictionary with memmap file path
    camera_dict = {'memmap_file': memmap_filename, 'coeff': coeff, 'frame_start': frame_tgt}
    camera_dict.update(conv_dict)
    camera_dict.update(tra_dict)
    camera_dict.update(config_dict)
    
    camera_dict['data_size'] = (num_frames, *camera_dict['trimmed_size'])
    
    return camera_dict
    
#%% Test
if __name__ == "__main__":
    
    import time
    import matplotlib.pyplot as plt
    import numpy as np
    
    time_sta = time.time()
    shot_no = 256221
    frame_tgt=0
    num_frames=0
    flg_rot=False
    line_ch = '2' 
    camera_dict = camera_reader(shot_no, line_ch, frame_tgt, num_frames, flg_rot)
    
    # Load and display the saved memmap
    if camera_dict:
        memmap_file = camera_dict['memmap_file']
        shape=(camera_dict['data_size'])
        trimmed_memmap = np.memmap(memmap_file, dtype=np.float32, mode='r', shape=(camera_dict['data_size']))  # Adjust dtype and shape as per actual data
        plt.imshow(trimmed_memmap[0,:,:]) # [frame, x, z]
        plt.show()
    
    time_end = time.time()
    print('Time spent: ' + str(time_end-time_sta) + ' (s)')