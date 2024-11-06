import load_tiff
import read_conv_info
import transform_image 
import read_config_info
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
    # Config and paths
    config_dict = read_config_info.read_config_info()
    tiff_dir = config_dict['tiff_dir']
    conv_dict = read_conv_info.read_conv_info(shot_no, tiff_dir)
    
    if num_frames == 0:
        num_frames = int(conv_dict['bottom_frame']) - (int(conv_dict['top_frame']) + frame_tgt)  # Load all remaining frames
    
    # Load the first frame to determine the shape
    first_frame = load_tiff.load_tiff(shot_no, tiff_dir, frame_tgt, 1)
    first_frame, tra_dict, coeff = transform_image.transform_image(shot_no, line_ch, tiff_dir, first_frame, flg_rot)
    
    # Determine the shape and estimated memory usage
    frame_shape = first_frame[0].shape
    estimated_size_gb = (num_frames * frame_shape[0] * frame_shape[1] * 4) / (1024 ** 3)  # 4 bytes per float32 pixel

    # Initialize data storage based on estimated size
    # if True:   # For testing
    if estimated_size_gb > int(config_dict['mem_limit_size']):
        memmap_filename = 'trimmed_image.dat'
        trimmed_memmap = np.memmap(memmap_filename, dtype='float32', mode='w+', shape=(num_frames,) + frame_shape)
        camera_data = trimmed_memmap
        print("Using memmap due to large data size")
    else:
        camera_data = np.empty((num_frames,) + frame_shape, dtype='float32')
        print("Using in-memory array")

    # Process each frame
    for i in tqdm(range(frame_tgt, frame_tgt + num_frames), desc="Loading frames..."):
        try:
            img_array = load_tiff.load_tiff(shot_no, tiff_dir, i, 1)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None
        
        # Transform the image
        img_array, tra_dict, coeff = transform_image.transform_image(shot_no, line_ch, tiff_dir, img_array, flg_rot)
        
        # Save the trimmed image to the appropriate storage (memmap or in-memory array)
        camera_data[i - frame_tgt] = img_array

    # Create a dictionary with the data storage type
    camera_dict = {'data': camera_data, 'coeff': coeff, 'frame_start': int(conv_dict['top_frame']) + frame_tgt}
    camera_dict.update(conv_dict)
    camera_dict.update(tra_dict)
    camera_dict.update(config_dict)
    
    camera_dict['data_size'] = (num_frames, *camera_dict['trimmed_size'])

    return camera_dict

#%% Test
if __name__ == "__main__":
    
    import time
    import matplotlib.pyplot as plt
    
    time_sta = time.time()
    shot_no = 256221
    frame_tgt = 0
    num_frames = 1000
    flg_rot = False
    line_ch = '2' 
    camera_dict = camera_reader(shot_no, line_ch, frame_tgt, num_frames, flg_rot)
    
    # Display the first frame
    # if camera_dict and isinstance(camera_dict['data'], np.memmap):
    #     trimmed_memmap = camera_dict['data']
    #     plt.imshow(trimmed_memmap[0, :, :])  # [frame, x, z]
    #     plt.show()
    # elif camera_dict:
    #     plt.imshow(camera_dict['data'][0, :, :])
    #     plt.show()
    if camera_dict:
        plt.imshow(camera_dict['data'][0, :, :])
        plt.show()
    
    time_end = time.time()
    print('Time spent: ' + str(time_end - time_sta) + ' (s)')
